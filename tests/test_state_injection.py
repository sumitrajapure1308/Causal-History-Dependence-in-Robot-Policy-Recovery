"""State Injection Unit Tests for Causal-History-Recovery.

Validates that direct matched-state injection reproduces the physical state
without corrupting remaining horizon, task goals, or introducing solver artifacts.
"""

import sys
import os
import numpy as np
import pytest

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.mujoco_wrapper import MuJoCoWrapperEnv


def test_state_injection_goal_preservation():
    """Verify that direct state injection preserves the task goal configuration."""
    env = MuJoCoWrapperEnv("Pusher-v5")
    env.reset(seed=42)

    rng = np.random.RandomState(42)
    for _ in range(10):
        env.step(rng.uniform(-0.5, 0.5, size=env.action_space.shape))

    target_snap = env.get_state_snapshot()
    # Explicitly set a non-zero custom target goal in the snapshot to test preservation
    custom_goal_xy = np.array([0.15, -0.20])
    target_snap.qpos[-2:] = custom_goal_xy
    target_snap.task_goal = np.array([custom_goal_xy[1], custom_goal_xy[0], 0.0])

    # Reset environment to standard zero state
    env.reset(seed=999)
    assert not np.allclose(env.get_task_goal()[:2], target_snap.task_goal[:2])

    # Inject matched state
    obs_injected = env.inject_matched_state(target_snap, preserve_horizon=True)
    injected_goal = env.get_task_goal()

    assert np.allclose(injected_goal, target_snap.task_goal, atol=1e-12), "Direct state injection altered task goal!"


def test_state_injection_horizon_preservation():
    """Verify that direct state injection preserves remaining horizon when requested."""
    env = MuJoCoWrapperEnv("Pusher-v5")
    env.reset(seed=42)

    rng = np.random.RandomState(42)
    for _ in range(18):
        env.step(rng.uniform(-0.5, 0.5, size=env.action_space.shape))

    snap = env.get_state_snapshot()
    assert snap.step_count == 18
    assert snap.remaining_horizon == 82

    # Reset to blank state
    env.reset(seed=12)
    assert env.step_count == 0
    assert env.remaining_horizon == 100

    # Inject with horizon preservation
    env.inject_matched_state(snap, preserve_horizon=True)
    assert env.step_count == 18, "Step count was corrupted during injection!"
    assert env.remaining_horizon == 82, "Remaining horizon was corrupted during injection!"


def test_state_injection_observation_consistency():
    """Verify that observation immediately after injection matches the replayed observation."""
    env = MuJoCoWrapperEnv("Pusher-v5")
    env.reset(seed=42)

    rng = np.random.RandomState(42)
    actions = [rng.uniform(-0.5, 0.5, size=env.action_space.shape) for _ in range(14)]
    for a in actions:
        obs_replayed, _, _, _, _ = env.step(a)

    replayed_snap = env.get_state_snapshot()

    # Create new fresh environment instance
    fresh_env = MuJoCoWrapperEnv("Pusher-v5")
    fresh_env.reset(seed=999)

    # Inject replayed state
    obs_injected = fresh_env.inject_matched_state(replayed_snap, preserve_horizon=True)

    diff = np.max(np.abs(obs_replayed - obs_injected))
    assert diff < 1e-8, f"Injected observation diverges from replayed observation! diff={diff}"
