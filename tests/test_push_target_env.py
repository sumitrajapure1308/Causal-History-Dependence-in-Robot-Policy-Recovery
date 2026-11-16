"""Unit Tests for PushTargetEnv Custom Environment.

Validates determinism, snapshotting, contact extraction, kinematics, and injection.
"""

import sys
import os
import numpy as np
import pytest

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.push_target_env import PushTargetEnv


def test_push_target_reset_determinism():
    """Verify identical seeds produce bitwise identical initial configurations."""
    env1 = PushTargetEnv()
    env2 = PushTargetEnv()

    obs1, info1 = env1.reset(seed=42)
    obs2, info2 = env2.reset(seed=42)

    assert np.allclose(obs1, obs2, atol=1e-10)
    assert np.allclose(env1.data.qpos, env2.data.qpos, atol=1e-10)
    assert np.allclose(env1.data.qvel, env2.data.qvel, atol=1e-10)
    assert info1["remaining_horizon"] == info2["remaining_horizon"] == 150


def test_push_target_stepping_determinism():
    """Verify stepping identical action sequence yields 0.0 divergence."""
    env1 = PushTargetEnv()
    env2 = PushTargetEnv()

    env1.reset(seed=1337)
    env2.reset(seed=1337)

    rng = np.random.RandomState(999)
    actions = [rng.uniform(-0.01, 0.01, size=(3,)) for _ in range(25)]

    for idx, a in enumerate(actions):
        o1, r1, t1, tr1, _ = env1.step(a)
        o2, r2, t2, tr2, _ = env2.step(a)

        assert np.allclose(o1, o2, atol=1e-10), f"Observation diverged at step {idx}"
        assert np.isclose(r1, r2, atol=1e-10)
        assert np.allclose(env1.data.qpos, env2.data.qpos, atol=1e-10)


def test_push_target_snapshot_and_restore():
    """Verify state snapshot and restore reproduce exact state."""
    env = PushTargetEnv()
    env.reset(seed=77)

    # Step forward 15 steps
    for _ in range(15):
        env.step(np.array([0.005, 0.001, 0.0]))

    snap = env.get_state_snapshot()

    # Step forward further to perturb
    for _ in range(10):
        env.step(np.array([0.002, -0.003, 0.0]))

    # Restore snapshot
    env.restore_state_snapshot(snap)

    assert np.allclose(env.data.qpos, snap.qpos, atol=1e-10)
    assert np.allclose(env.data.qvel, snap.qvel, atol=1e-10)
    assert np.isclose(env.data.time, snap.time, atol=1e-12)
    assert env.step_count == snap.step_count == 15
    assert env.remaining_horizon == snap.remaining_horizon == 135


def test_push_target_prefix_replay():
    """Verify prefix replay reproduces candidate state with bounded error."""
    env = PushTargetEnv()
    seed = 101
    env.reset(seed=seed)

    actions = [np.array([0.005, 0.002, 0.0]) for _ in range(12)]
    for a in actions:
        env.step(a)
    snap_orig = env.get_state_snapshot()

    snap_replayed, obs_replayed = env.replay_action_prefix(seed, actions)

    assert np.allclose(snap_orig.qpos, snap_replayed.qpos, atol=1e-10)
    assert np.allclose(snap_orig.qvel, snap_replayed.qvel, atol=1e-10)
    assert snap_orig.step_count == snap_replayed.step_count == 12


def test_push_target_direct_state_injection():
    """Verify direct state injection preserves goal and remaining horizon."""
    env = PushTargetEnv()
    env.reset(seed=42)

    for _ in range(20):
        env.step(np.array([0.004, 0.0, 0.0]))
    snap = env.get_state_snapshot()

    fresh_env = PushTargetEnv()
    fresh_env.reset(seed=999)

    obs_injected = fresh_env.inject_matched_state(snap, preserve_horizon=True)

    assert fresh_env.step_count == 20
    assert fresh_env.remaining_horizon == 130
    assert np.allclose(fresh_env.get_task_goal(), snap.task_goal, atol=1e-10)
    assert np.allclose(fresh_env.data.qpos, snap.qpos, atol=1e-10)


def test_push_target_kinematics_and_yaw_extraction():
    """Verify yaw and angular velocity extraction."""
    env = PushTargetEnv()
    env.reset(seed=42)

    yaw = env.get_object_yaw()
    assert -np.pi <= yaw <= np.pi
    assert np.isclose(yaw, 0.0, atol=0.05)

    lin_vel = env.get_object_linear_velocity()
    ang_vel = env.get_object_angular_velocity()
    assert lin_vel.shape == (3,)
    assert ang_vel.shape == (3,)
    assert np.allclose(lin_vel, 0.0, atol=1e-4)


def test_push_target_restore_no_accumulated_drift():
    """Verify restore-and-step cycles do not accumulate hidden drift."""
    env = PushTargetEnv()
    env.reset(seed=55)

    prefix = [np.array([0.004, 0.001, 0.0]) for _ in range(10)]
    continuation = [np.array([0.003, -0.002, 0.0]) for _ in range(10)]

    for a in prefix:
        env.step(a)
    snap = env.get_state_snapshot()

    # Branch 1
    obs_b1 = []
    for a in continuation:
        obs, _, _, _, _ = env.step(a)
        obs_b1.append(obs)

    # Restore and Branch 2
    env.restore_state_snapshot(snap)
    obs_b2 = []
    for a in continuation:
        obs, _, _, _, _ = env.step(a)
        obs_b2.append(obs)

    for idx, (o1, o2) in enumerate(zip(obs_b1, obs_b2)):
        diff = np.max(np.abs(o1 - o2))
        assert diff < 1e-10, f"Branch divergence at step {idx}: diff={diff}"

