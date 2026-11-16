"""State Snapshot and Serialization Unit Tests.

Validates that state snapshot capture, disk serialization, and restoration are
lossless and eliminate hidden numerical drift.
"""

import sys
import os
import tempfile
import numpy as np
import pytest

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.mujoco_wrapper import MuJoCoWrapperEnv
from causal_history_recovery.environments.state_snapshot import StateSnapshot


def test_snapshot_restore_exactness():
    """Verify that capturing a snapshot and restoring it recreates exact state."""
    env = MuJoCoWrapperEnv("Pusher-v5")
    env.reset(seed=42)

    # Step forward 10 steps
    rng = np.random.RandomState(42)
    for _ in range(10):
        env.step(rng.uniform(-0.5, 0.5, size=env.action_space.shape))

    snapshot = env.get_state_snapshot()

    # Step forward another 10 steps to perturb state
    for _ in range(10):
        env.step(rng.uniform(-0.5, 0.5, size=env.action_space.shape))

    # Restore snapshot
    env.restore_state_snapshot(snapshot)

    assert np.allclose(env.data.qpos, snapshot.qpos, atol=1e-10)
    assert np.allclose(env.data.qvel, snapshot.qvel, atol=1e-10)
    assert np.isclose(env.data.time, snapshot.time, atol=1e-12)
    assert env.step_count == snapshot.step_count == 10
    assert env.remaining_horizon == snapshot.remaining_horizon == 90


def test_serialization_roundtrip_npz():
    """Verify that saving to compressed npz and loading preserves all fields."""
    env = MuJoCoWrapperEnv("Pusher-v5")
    env.reset(seed=77)
    for _ in range(5):
        env.step(np.zeros(env.action_space.shape))

    snapshot_orig = env.get_state_snapshot()

    with tempfile.NamedTemporaryFile(suffix=".npz", delete=False) as f:
        temp_path = f.name

    try:
        snapshot_orig.save(temp_path)
        snapshot_loaded = StateSnapshot.load(temp_path)

        assert np.allclose(snapshot_orig.qpos, snapshot_loaded.qpos, atol=1e-10)
        assert np.allclose(snapshot_orig.qvel, snapshot_loaded.qvel, atol=1e-10)
        assert np.isclose(snapshot_orig.time, snapshot_loaded.time, atol=1e-12)
        assert snapshot_orig.step_count == snapshot_loaded.step_count
        assert snapshot_orig.remaining_horizon == snapshot_loaded.remaining_horizon
        assert snapshot_orig.active_contacts_count == snapshot_loaded.active_contacts_count
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_restore_and_step_no_accumulated_drift():
    """Verify that repeated restore-and-step cycles do not accumulate hidden drift."""
    env = MuJoCoWrapperEnv("Pusher-v5")
    env.reset(seed=123)

    rng = np.random.RandomState(456)
    prefix_actions = [rng.uniform(-0.5, 0.5, size=env.action_space.shape) for _ in range(12)]
    continuation_actions = [rng.uniform(-0.5, 0.5, size=env.action_space.shape) for _ in range(10)]

    for a in prefix_actions:
        env.step(a)

    snapshot = env.get_state_snapshot()

    # Rollout Branch A
    obs_branch_a = []
    for a in continuation_actions:
        obs, _, _, _, _ = env.step(a)
        obs_branch_a.append(obs)

    # Restore snapshot and rollout Branch B
    env.restore_state_snapshot(snapshot)
    obs_branch_b = []
    for a in continuation_actions:
        obs, _, _, _, _ = env.step(a)
        obs_branch_b.append(obs)

    # Compare Branch A and Branch B
    for idx, (oa, ob) in enumerate(zip(obs_branch_a, obs_branch_b)):
        diff = np.max(np.abs(oa - ob))
        assert diff < 1e-9, f"Restore-and-step divergence at continuation step {idx}: diff={diff}"


def test_state_distance_metric_consistency():
    """Verify distance metric properties: identity, non-negativity, symmetry."""
    env = MuJoCoWrapperEnv("Pusher-v5")
    env.reset(seed=1)
    snap1 = env.get_state_snapshot()

    env.step(np.ones(env.action_space.shape) * 0.5)
    snap2 = env.get_state_snapshot()

    # Identity
    assert snap1.compute_distance(snap1) == 0.0

    # Non-negativity
    d12 = snap1.compute_distance(snap2)
    assert d12 > 0.0

    # Symmetry
    d21 = snap2.compute_distance(snap1)
    assert np.isclose(d12, d21, atol=1e-8)

