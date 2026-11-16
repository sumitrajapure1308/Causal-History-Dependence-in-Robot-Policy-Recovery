"""Unit and Integration Tests for Contact-Loss Failure Mode (Phase 10).

Validates:
1. Physical generation of contact loss without teleportation.
2. Distinction from off-center slip (zero contact, low yaw).
3. Automated detection via ContactLossDetector.
4. Privileged oracle recovery solving the failure state.
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
from causal_history_recovery.environments.contact_loss_failure import (
    ContactLossDetector,
    ContactLossOracleController,
    generate_contact_loss_trajectory,
)


def test_contact_loss_physical_generation_no_teleportation():
    """Verify contact loss is induced physically via forward integration without coordinate jumps."""
    env = PushTargetEnv()
    snap, act_pref, obs_pref, meta = generate_contact_loss_trajectory(
        env, seed=555, perturb_step=20, decel_steps=3, decel_magnitude=-0.015
    )

    assert meta["failure_detected"] is True, "Contact loss must be detected"
    assert snap is not None
    assert len(act_pref) == meta["deviation_step"]

    # Check coordinate continuity across steps (no jump > action limit + small physics integration)
    obs_arr = np.array(obs_pref)
    ee_diffs = np.linalg.norm(np.diff(obs_arr[:, :3], axis=0), axis=1)
    assert np.all(ee_diffs <= 0.025), "Manipulator motion must be physically continuous"


def test_contact_loss_distinct_from_slip():
    """Verify contact loss features zero contact and minimal yaw, distinct from rotational slip."""
    env = PushTargetEnv()
    snap, act_pref, obs_pref, meta = generate_contact_loss_trajectory(
        env, seed=888, perturb_step=20, decel_steps=3, decel_magnitude=-0.018
    )
    assert snap is not None
    env.restore_state_snapshot(snap)

    # 1. Contacts between pusher and object must be 0
    contacts = env.get_contacts()
    pusher_obj_contacts = [
        c for c in contacts
        if (c.geom1_id == env.pusher_geom_id and c.geom2_id == env.object_geom_id) or
           (c.geom1_id == env.object_geom_id and c.geom2_id == env.pusher_geom_id)
    ]
    assert len(pusher_obj_contacts) == 0, "Contact loss state must have 0 active contacts"

    # 2. Object yaw deflection must be small (< 10 degrees = 0.175 rad)
    yaw = env.get_object_yaw()
    assert abs(yaw) < 0.175, f"Yaw deflection in contact loss should be minimal, got {yaw:.4f} rad"

    # 3. Air gap must be positive (> 0.015 m)
    ee_pos = env.get_end_effector_position()
    obj_pos = env.get_object_position()
    gap = np.linalg.norm(ee_pos[:2] - obj_pos[:2]) - 0.045
    assert gap >= 0.015, f"Expected air gap >= 0.015 m, got {gap:.4f} m"


def test_contact_loss_oracle_recovery():
    """Verify privileged oracle can solve the contact loss failure state."""
    env = PushTargetEnv()
    snap, _, _, meta = generate_contact_loss_trajectory(
        env, seed=1234, perturb_step=20, decel_steps=3, decel_magnitude=-0.018
    )
    assert snap is not None
    env.restore_state_snapshot(snap)

    oracle = ContactLossOracleController()
    rem_h = env.remaining_horizon
    solved = False

    for _ in range(rem_h):
        act = oracle.act(env)
        _, _, term, trunc, info = env.step(act)
        if info.get("is_success", False):
            solved = True
            break
        if term or trunc:
            break

    assert solved is True, "Privileged oracle must successfully recover from contact loss failure"

