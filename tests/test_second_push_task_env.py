"""Unit and Integration Tests for SecondPushTaskEnv (Phase 10).

Validates:
1. Environment instantiation and distinct physical attributes (cylinder geom, mass 0.15, mu 0.35).
2. Reset and stepping determinism.
3. Bitwise deterministic state snapshotting and restoration.
4. Binary task success requiring dwell time in diagonal offset target.
5. Contrast with primary PushTargetEnv (confirming non-identical dynamics).
"""

from __future__ import annotations

import os
import sys
import numpy as np
import pytest

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(repo_root, "src"))

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.environments.second_push_task_env import SecondPushTaskEnv


def test_second_push_task_env_initialization():
    env = SecondPushTaskEnv()
    obs, info = env.reset(seed=42)
    assert obs.shape == (20,)
    assert info["step_count"] == 0
    assert info["is_success"] is False
    assert env.get_object_position().shape == (3,)
    assert np.allclose(env.get_task_goal(), [0.20, 0.08, 0.020])


def test_second_push_task_env_physical_contrast():
    """Verify Task 2 is physically distinct from Task 1 (geometry, mass, friction, goal)."""
    env1 = PushTargetEnv()
    env2 = SecondPushTaskEnv()

    # Geometry check: Task 1 object is box (type 6 in MuJoCo), Task 2 is cylinder (type 5)
    geom1_type = env1.model.geom("object_geom").type[0]
    geom2_type = env2.model.geom("object_geom").type[0]
    assert geom1_type != geom2_type, "Task 2 must have distinct geom type from Task 1"

    # Mass check: Task 1 is 0.10 kg, Task 2 is 0.15 kg
    mass1 = env1.model.body("target_object").mass[0]
    mass2 = env2.model.body("target_object").mass[0]
    assert abs(mass2 - 1.5 * mass1) < 1e-4, "Task 2 object mass must be 0.15 kg (50% heavier)"

    # Friction check: Task 1 table friction is 0.50, Task 2 is 0.35
    fric1 = env1.model.geom("table").friction[0]
    fric2 = env2.model.geom("table").friction[0]
    assert fric2 < fric1, "Task 2 table friction must be lower (0.35 vs 0.50)"

    # Goal check: Task 1 is straight [0.25, 0.0, 0.025], Task 2 is diagonal [0.20, 0.08, 0.020]
    goal1 = env1.get_task_goal()
    goal2 = env2.get_task_goal()
    assert not np.allclose(goal1, goal2), "Task 2 goal must be diagonally offset"


def test_second_push_task_determinism():
    """Verify bitwise stepping determinism for identical seeds and actions."""
    env1 = SecondPushTaskEnv()
    env2 = SecondPushTaskEnv()

    obs1, _ = env1.reset(seed=999)
    obs2, _ = env2.reset(seed=999)
    assert np.array_equal(obs1, obs2)

    action = np.array([0.015, 0.005, 0.0], dtype=np.float32)
    for _ in range(10):
        o1, r1, d1, t1, _ = env1.step(action)
        o2, r2, d2, t2, _ = env2.step(action)
        assert np.array_equal(o1, o2)
        assert r1 == r2


def test_second_push_task_snapshot_restore():
    """Verify bitwise exact snapshotting and restoration."""
    env = SecondPushTaskEnv()
    env.reset(seed=777)

    # Step forward 15 steps
    for _ in range(15):
        env.step(np.array([0.01, 0.004, 0.0], dtype=np.float32))

    snapshot = env.get_state_snapshot()
    qpos_saved = snapshot.qpos.copy()
    qvel_saved = snapshot.qvel.copy()

    # Step more to diverge
    for _ in range(10):
        env.step(np.array([-0.01, 0.01, 0.0], dtype=np.float32))

    # Restore snapshot
    env.restore_state_snapshot(snapshot)
    assert np.array_equal(env.data.qpos, qpos_saved)
    assert np.array_equal(env.data.qvel, qvel_saved)
    assert env.step_count == snapshot.step_count


def test_second_push_task_success_dwell():
    """Verify task success requires dwelling in diagonal target."""
    env = SecondPushTaskEnv()
    env.reset(seed=123)

    # Teleport to goal for unit testing the dwell detector
    env.data.qpos[3:6] = [0.20, 0.08, 0.020]
    env.data.qpos[6:10] = [1.0, 0.0, 0.0, 0.0]
    env.data.qvel[:] = 0.0

    # Step stationary
    zero_act = np.zeros(3, dtype=np.float32)
    for step_idx in range(4):
        _, _, _, _, info = env.step(zero_act)
        assert info["dwell_count"] == step_idx + 1
        assert info["is_success"] is False

    # 5th dwell step triggers success
    _, _, _, _, info5 = env.step(zero_act)
    assert info5["dwell_count"] >= 5
    assert info5["is_success"] is True

