"""Prefix Replay Unit Tests for Causal-History-Recovery.

Validates that replaying an action prefix reproduces the candidate failure state
and observation trajectory with zero divergence.
"""

import sys
import os
import numpy as np
import pytest

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.mujoco_wrapper import MuJoCoWrapperEnv


def test_prefix_replay_bounded_error():
    """Verify that replaying a prefix reproduces identical state at deviation time td."""
    env = MuJoCoWrapperEnv("Pusher-v5")
    seed = 42
    env.reset(seed=seed)

    rng = np.random.RandomState(seed)
    action_prefix = [rng.uniform(-0.5, 0.5, size=env.action_space.shape) for _ in range(15)]

    # 1. Original rollout
    original_obs = []
    for a in action_prefix:
        obs, _, _, _, _ = env.step(a)
        original_obs.append(obs)
    original_snap = env.get_state_snapshot()

    # 2. Replay prefix via replay_action_prefix
    replay_snap, replay_obs = env.replay_action_prefix(seed, action_prefix)

    # 3. Verify state fidelity
    assert np.allclose(original_snap.qpos, replay_snap.qpos, atol=1e-10)
    assert np.allclose(original_snap.qvel, replay_snap.qvel, atol=1e-10)
    assert np.isclose(original_snap.time, replay_snap.time, atol=1e-12)
    assert original_snap.step_count == replay_snap.step_count == 15
    assert original_snap.remaining_horizon == replay_snap.remaining_horizon == 85

    # 4. Verify observation trajectory matching
    for idx, (orig_o, repl_o) in enumerate(zip(original_obs, replay_obs)):
        assert np.allclose(orig_o, repl_o, atol=1e-10), f"Observation mismatch at replay step {idx}!"


def test_prefix_replay_goal_preservation():
    """Verify that the task goal is preserved identically across prefix replay."""
    env = MuJoCoWrapperEnv("Pusher-v5")
    seed = 888
    env.reset(seed=seed)
    goal_initial = env.get_task_goal().copy()

    rng = np.random.RandomState(seed)
    prefix = [rng.uniform(-0.3, 0.3, size=env.action_space.shape) for _ in range(10)]

    snap, _ = env.replay_action_prefix(seed, prefix)
    goal_after_replay = snap.task_goal

    assert np.allclose(goal_initial, goal_after_replay, atol=1e-12), "Task goal mutated during replay!"

