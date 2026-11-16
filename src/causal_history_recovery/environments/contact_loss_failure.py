"""Contact-Loss and Premature Push Termination Failure Mode (Failure Mode 2).

Implements:
1. ContactLossDetector: Automated detector for premature push disengagement.
2. ContactLossFailureGenerator: Generates physically continuous contact loss via transient deceleration.
3. ContactLossOracleController: Privileged geometric oracle to prove recoverability.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from causal_history_recovery.environments.base_env import BaseRoboticEnv
from causal_history_recovery.environments.state_snapshot import StateSnapshot


class ContactLossDetector:
    """Detects premature contact loss without goal achievement."""

    def __init__(
        self,
        min_air_gap_m: float = 0.020,
        min_dist_to_goal_m: float = 0.080,
        max_object_speed_mps: float = 0.015,
        min_loss_duration_steps: int = 3,
    ):
        self.min_air_gap = min_air_gap_m
        self.min_dist_to_goal = min_dist_to_goal_m
        self.max_object_speed = max_object_speed_mps
        self.min_loss_duration = min_loss_duration_steps
        self._consecutive_loss_steps = 0

    def reset(self) -> None:
        self._consecutive_loss_steps = 0

    def check_failure(
        self,
        env: BaseRoboticEnv,
    ) -> Tuple[bool, Dict[str, Any]]:
        ee_pos = env.get_end_effector_position()
        obj_pos = env.get_object_position()
        goal_pos = env.get_task_goal()
        obj_vel = env.get_object_velocity() if hasattr(env, "get_object_velocity") else np.zeros(3)

        contacts = env.get_contacts()
        has_contact = any(
            (c.geom1_id == getattr(env, "pusher_geom_id", -1) and c.geom2_id == getattr(env, "object_geom_id", -2)) or
            (c.geom1_id == getattr(env, "object_geom_id", -2) and c.geom2_id == getattr(env, "pusher_geom_id", -1))
            for c in contacts
        )

        air_gap = float(np.linalg.norm(ee_pos[:2] - obj_pos[:2]) - 0.045)  # effective surface gap
        dist_to_goal = float(np.linalg.norm(obj_pos[:2] - goal_pos[:2]))
        speed = float(np.linalg.norm(obj_vel[:2]))

        if not has_contact and air_gap >= self.min_air_gap and dist_to_goal >= self.min_dist_to_goal and speed <= self.max_object_speed:
            self._consecutive_loss_steps += 1
        else:
            self._consecutive_loss_steps = 0

        is_failure = bool(self._consecutive_loss_steps >= self.min_loss_duration)

        info = {
            "has_contact": has_contact,
            "air_gap": air_gap,
            "dist_to_goal": dist_to_goal,
            "object_speed": speed,
            "consecutive_loss_steps": self._consecutive_loss_steps,
            "is_failure": is_failure,
        }
        return is_failure, info


class ContactLossOracleController:
    """Privileged geometric oracle that re-acquires contact and pushes to goal."""

    def __init__(self, action_limit: float = 0.02):
        self.action_limit = action_limit

    def act(self, env: BaseRoboticEnv) -> np.ndarray:
        ee_pos = env.get_end_effector_position()
        obj_pos = env.get_object_position()
        goal_pos = env.get_task_goal()

        # Vector from object to goal
        obj_to_goal = goal_pos[:2] - obj_pos[:2]
        dist_goal = float(np.linalg.norm(obj_to_goal))
        if dist_goal > 1e-6:
            push_dir = obj_to_goal / dist_goal
        else:
            push_dir = np.array([1.0, 0.0])

        # Stand-off position behind object along push direction
        standoff_dist = 0.055  # pusher radius + object margin
        target_ee = np.array([
            obj_pos[0] - push_dir[0] * standoff_dist,
            obj_pos[1] - push_dir[1] * standoff_dist,
            0.0,
        ])

        diff_to_standoff = target_ee[:2] - ee_pos[:2]
        dist_standoff = float(np.linalg.norm(diff_to_standoff))

        if dist_standoff > 0.015:
            # Phase 1: Re-align behind object
            move_dir = diff_to_standoff / dist_standoff
            action_xy = move_dir * min(self.action_limit, dist_standoff)
        else:
            # Phase 2: Push through object toward goal
            action_xy = push_dir * min(self.action_limit, dist_goal + 0.02)

        action = np.array([action_xy[0], action_xy[1], 0.0], dtype=np.float32)
        return np.clip(action, -self.action_limit, self.action_limit)


def generate_contact_loss_trajectory(
    env: BaseRoboticEnv,
    seed: int,
    perturb_step: int = 25,
    decel_steps: int = 3,
    decel_magnitude: float = -0.018,
) -> Tuple[Optional[StateSnapshot], List[np.ndarray], List[np.ndarray], Dict[str, Any]]:
    """Physically induce contact loss via transient deceleration without teleportation."""
    obs, _ = env.reset(seed=seed)
    detector = ContactLossDetector()

    action_prefix: List[np.ndarray] = []
    obs_prefix: List[np.ndarray] = [obs]

    # Nominal forward push vector
    goal_pos = env.get_task_goal()
    obj_pos = env.get_object_position()
    push_vec = goal_pos[:2] - obj_pos[:2]
    push_norm = float(np.linalg.norm(push_vec))
    nominal_step = (push_vec / push_norm) * 0.010 if push_norm > 0 else np.array([0.01, 0.0])
    nom_act = np.array([nominal_step[0], nominal_step[1], 0.0], dtype=np.float32)

    failure_detected = False
    snapshot_at_dev: Optional[StateSnapshot] = None
    dev_step = -1

    for t in range(env.max_horizon):
        if t < perturb_step:
            act = nom_act.copy()
        elif t < perturb_step + decel_steps:
            # Transient deceleration/retraction pulse
            act = np.array([decel_magnitude, 0.0, 0.0], dtype=np.float32)
        else:
            # Hold stationary to let object settle
            act = np.zeros(3, dtype=np.float32)

        action_prefix.append(act)
        obs, _, term, trunc, info = env.step(act)
        obs_prefix.append(obs)

        is_loss, loss_info = detector.check_failure(env)
        if is_loss and not failure_detected:
            failure_detected = True
            dev_step = t + 1
            snapshot_at_dev = env.get_state_snapshot()
            break

        if term or trunc:
            break

    metadata = {
        "seed": seed,
        "perturb_step": perturb_step,
        "decel_steps": decel_steps,
        "decel_magnitude": decel_magnitude,
        "failure_detected": failure_detected,
        "deviation_step": dev_step,
        "remaining_horizon": env.remaining_horizon if failure_detected else 0,
    }
    return snapshot_at_dev, action_prefix, obs_prefix, metadata

