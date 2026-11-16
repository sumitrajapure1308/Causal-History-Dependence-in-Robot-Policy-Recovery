"""Unit Tests for Task Success Specification.

Validates:
1. Binary task success criteria: position within 6 cm, yaw within 0.35 rad, dwell >= 5 steps.
2. Dwell counter resets to 0 if object exits target zone before 5 steps.
3. Severe yaw misalignment (> 0.35 rad) suppresses dwell accumulation.
4. Dense distance reward is distinct from binary success flag.
5. Out of bounds and table departure terminate episode as failure.
"""

from __future__ import annotations

import os
import sys
import numpy as np
import pytest

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.push_target_env import PushTargetEnv


def test_binary_success_all_criteria_met():
    """Verify success flag triggers if and only if position, yaw, and dwell criteria are satisfied."""
    env = PushTargetEnv()
    env.reset(seed=42)

    # Place object stably inside target zone with 0 yaw
    target_pos = env.get_task_goal()
    snap = env.get_state_snapshot()
    snap.qpos[3:6] = target_pos  # exactly at target
    snap.qpos[6:10] = [1.0, 0.0, 0.0, 0.0]  # zero yaw
    snap.qvel[:] = 0.0
    env.restore_state_snapshot(snap)

    # Step environment 5 times with zero control action
    for step in range(4):
        obs, r, term, trunc, info = env.step(np.zeros(3))
        assert not info["is_success"], f"Premature success at step {step} with dwell {info['dwell_count']}"
        assert info["dwell_count"] == step + 1

    # 5th step satisfies dwell threshold
    obs, r, term, trunc, info = env.step(np.zeros(3))
    assert info["is_success"] is True
    assert info["dwell_count"] >= 5


def test_dwell_resets_on_exit():
    """Verify dwell counter resets to 0 if the object exits the target zone prematurely."""
    env = PushTargetEnv()
    env.reset(seed=42)

    target_pos = env.get_task_goal()
    snap = env.get_state_snapshot()
    snap.qpos[3:6] = target_pos
    snap.qpos[6:10] = [1.0, 0.0, 0.0, 0.0]
    snap.qvel[:] = 0.0
    env.restore_state_snapshot(snap)

    # Dwell for 3 steps
    for _ in range(3):
        env.step(np.zeros(3))
    assert env._dwell_count == 3

    # Move object outside target zone
    snap_mid = env.get_state_snapshot()
    snap_mid.qpos[3:6] = [0.0, 0.0, 0.025]  # far from target
    snap_mid.qvel[:] = 0.0
    env.restore_state_snapshot(snap_mid)

    obs, r, term, trunc, info = env.step(np.zeros(3))
    assert info["dwell_count"] == 0
    assert info["is_success"] is False


def test_misaligned_yaw_blocks_success():
    """Verify yaw deflection > 0.35 rad (20 deg) prevents dwell accumulation even inside target."""
    env = PushTargetEnv()
    env.reset(seed=42)

    target_pos = env.get_task_goal()
    snap = env.get_state_snapshot()
    snap.qpos[3:6] = target_pos
    # Set yaw to 30 degrees (0.5236 rad > 0.35 rad tolerance)
    # Quaternion for yaw theta: [cos(theta/2), 0, 0, sin(theta/2)]
    theta = 0.5236
    snap.qpos[6:10] = [np.cos(theta / 2), 0.0, 0.0, np.sin(theta / 2)]
    snap.qvel[:] = 0.0
    env.restore_state_snapshot(snap)

    for _ in range(6):
        obs, r, term, trunc, info = env.step(np.zeros(3))
        assert info["dwell_count"] == 0
        assert info["is_success"] is False


def test_dense_reward_not_treated_as_success():
    """Verify high dense proximity reward does not trigger binary success."""
    env = PushTargetEnv()
    env.reset(seed=42)

    # Place object just outside target radius (dist = 0.065 m, radius = 0.060 m)
    snap = env.get_state_snapshot()
    snap.qpos[3:6] = [0.25, 0.065, 0.025]
    snap.qpos[6:10] = [1.0, 0.0, 0.0, 0.0]
    snap.qvel[:] = 0.0
    env.restore_state_snapshot(snap)

    obs, r, term, trunc, info = env.step(np.zeros(3))
    # Dense reward is -0.065, relatively high, but task is not successful
    assert info["is_success"] is False
    assert info["dist_to_goal"] > env._target_radius


def test_out_of_bounds_and_falling_terminates():
    """Verify table departure or perimeter escape immediately terminates episode."""
    env = PushTargetEnv()
    env.reset(seed=42)

    # 1. Test table departure (z < 0.01 m)
    snap = env.get_state_snapshot()
    snap.qpos[5] = -0.05  # below table
    env.restore_state_snapshot(snap)
    obs, r, term, trunc, info = env.step(np.zeros(3))
    assert term is True
    assert info["fallen"] is True
    assert info["is_success"] is False

    # 2. Test workspace escape (|x| > 0.45 m)
    env.reset(seed=42)
    snap = env.get_state_snapshot()
    snap.qpos[3] = 0.50  # beyond workspace
    env.restore_state_snapshot(snap)
    obs, r, term, trunc, info = env.step(np.zeros(3))
    assert term is True
    assert info["out_of_bounds"] is True
    assert info["is_success"] is False

