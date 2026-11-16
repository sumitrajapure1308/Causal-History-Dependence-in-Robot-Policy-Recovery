"""Unit Tests for Off-Center Slip Failure Mode.

Validates:
1. Centered pushing maintains low yaw (< 5 deg) and low lateral drift (< 1 cm).
2. Off-center pushing induces physical rotational slip (yaw >= 15 deg, drift >= 2 cm).
3. Contact force and manifold criteria (duration >= 5 steps, F_normal >= 0.05 N).
4. Physical continuity and stability (no teleportation, stable height on table).
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


def test_centered_push_low_deviation():
    """Verify nominal centered pushing produces minimal yaw and lateral drift."""
    env = PushTargetEnv()
    obs, info = env.reset(seed=42)
    obj_init = env.get_object_position().copy()

    # Align pusher laterally with object
    delta_y = obj_init[1] - env.get_end_effector_position()[1]
    env.step(np.array([0.0, delta_y, 0.0]))

    # Push forward along +X
    for _ in range(35):
        env.step(np.array([0.005, 0.0, 0.0]))

    obj_final = env.get_object_position()
    yaw_deg = abs(np.degrees(env.get_object_yaw()))
    lateral_drift_m = abs(obj_final[1] - obj_init[1])

    # Assert bounded yaw deflection and minimal lateral drift
    assert yaw_deg < 5.0, f"Centered push yaw {yaw_deg:.2f} deg exceeded 5.0 deg threshold"
    assert lateral_drift_m < 0.01, f"Centered push drift {lateral_drift_m*100:.2f} cm exceeded 1.0 cm threshold"


def test_off_center_push_induces_slip_deviation():
    """Verify off-center pushing induces rotational slip exceeding failure thresholds."""
    env = PushTargetEnv()
    obs, info = env.reset(seed=42)
    obj_init = env.get_object_position().copy()

    # Apply 18 mm lateral offset from object centerline
    offset = 0.018
    delta_y = (obj_init[1] + offset) - env.get_end_effector_position()[1]
    env.step(np.array([0.0, delta_y, 0.0]))

    # Step forward along +X
    for _ in range(40):
        env.step(np.array([0.005, 0.0, 0.0]))

    obj_final = env.get_object_position()
    yaw_deg = abs(np.degrees(env.get_object_yaw()))
    lateral_drift_m = abs(obj_final[1] - obj_init[1])

    # Assert failure thresholds from failure_mode_specification.md
    assert yaw_deg >= 15.0, f"Yaw deflection {yaw_deg:.2f} deg did not exceed 15.0 deg threshold"
    assert lateral_drift_m >= 0.02, f"Lateral drift {lateral_drift_m*100:.2f} cm did not exceed 2.0 cm threshold"


def test_contact_forces_and_manifold():
    """Verify contact duration >= 5 steps and normal force >= 0.05 N during push."""
    env = PushTargetEnv()
    env.reset(seed=42)
    obj_init = env.get_object_position().copy()

    offset = 0.018
    delta_y = (obj_init[1] + offset) - env.get_end_effector_position()[1]
    env.step(np.array([0.0, delta_y, 0.0]))

    contact_steps = 0
    max_normal_force = 0.0

    for _ in range(40):
        obs, r, term, trunc, info = env.step(np.array([0.005, 0.0, 0.0]))
        if info["has_pusher_contact"]:
            contact_steps += 1
            contacts = env.get_contacts()
            pc = env.contact_extractor.filter_contacts(contacts, "pusher_z_link", "target_object")
            if pc:
                max_normal_force = max(max_normal_force, pc[0].force_magnitude)

    assert contact_steps >= 5, f"Contact duration {contact_steps} steps was under 5-step requirement"
    assert max_normal_force >= 0.05, f"Peak contact force {max_normal_force:.3f} N was under 0.05 N requirement"


def test_physical_continuity_no_teleportation():
    """Verify object remains physically bounded on the table without discontinuities."""
    env = PushTargetEnv()
    env.reset(seed=42)
    obj_init = env.get_object_position().copy()

    offset = 0.018
    delta_y = (obj_init[1] + offset) - env.get_end_effector_position()[1]
    env.step(np.array([0.0, delta_y, 0.0]))

    prev_pos = obj_init.copy()
    for step in range(35):
        env.step(np.array([0.005, 0.0, 0.0]))
        cur_pos = env.get_object_position()
        
        # Verify object does not penetrate table or tumble off
        assert 0.015 <= cur_pos[2] <= 0.050, f"Object z {cur_pos[2]:.4f} outside stable table bounds"
        
        # Verify step-to-step position delta is physically bounded
        step_delta = np.linalg.norm(cur_pos - prev_pos)
        assert step_delta < 0.05, f"Step {step} position delta {step_delta:.4f} indicates non-physical jump"
        prev_pos = cur_pos.copy()

