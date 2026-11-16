"""Recovery and Task Performance Metrics for Causal-History-Recovery.

Computes task success, goal distance, orientation error, episode returns,
physical state recovery, and control effort.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import numpy as np


def compute_task_metrics(
    trajectory_obs: np.ndarray,
    actions: np.ndarray,
    goal_pos: np.ndarray,
    goal_radius: float = 0.060,
    min_dwell_steps: int = 5,
    max_yaw_tolerance_rad: float = 0.35,
) -> Dict[str, Any]:
    """Compute comprehensive task performance and completion metrics."""
    T = len(trajectory_obs)
    if T == 0:
        return {
            "is_success": False,
            "final_dist_to_goal": 1.0,
            "final_yaw_error_deg": 180.0,
            "completion_steps": 0,
            "dwell_count": 0,
            "episode_return": 0.0,
        }

    # Extract object positions from observations (indices 6:9 in obs_dim=20)
    # Obs schema: pusher_pos (0:3), pusher_vel (3:6), obj_pos (6:9), cos_yaw (9), sin_yaw (10), obj_lin_vel (11:14), obj_ang_vel (14:17), goal_pos (17:20)
    final_obs = trajectory_obs[-1]
    final_obj_pos = final_obs[6:9]
    final_cos_yaw = final_obs[9]
    final_sin_yaw = final_obs[10]

    final_dist = float(np.linalg.norm(final_obj_pos[:2] - goal_pos[:2]))
    final_yaw_rad = abs(float(np.arctan2(final_sin_yaw, final_cos_yaw)))
    final_yaw_deg = float(np.degrees(final_yaw_rad))

    # Track dwell time across trajectory
    dwell_count = 0
    max_dwell = 0
    is_success = False

    for t in range(T):
        obs_t = trajectory_obs[t]
        pos_t = obs_t[6:9]
        dist_t = np.linalg.norm(pos_t[:2] - goal_pos[:2])
        cos_t = obs_t[9]
        sin_t = obs_t[10]
        yaw_t = abs(np.arctan2(sin_t, cos_t))

        if dist_t <= goal_radius and yaw_t <= max_yaw_tolerance_rad:
            dwell_count += 1
            if dwell_count > max_dwell:
                max_dwell = dwell_count
            if dwell_count >= min_dwell_steps:
                is_success = True
        else:
            dwell_count = 0

    # Control effort and smoothness
    effort = float(np.sum(np.square(actions)))
    if len(actions) > 1:
        diffs = actions[1:] - actions[:-1]
        smoothness = float(np.sum(np.square(diffs)))
    else:
        smoothness = 0.0

    return {
        "is_success": is_success,
        "final_dist_to_goal": final_dist,
        "final_yaw_error_deg": final_yaw_deg,
        "completion_steps": T,
        "max_dwell_steps": max_dwell,
        "control_effort": effort,
        "action_smoothness": smoothness,
    }


def compute_physical_recovery_metrics(
    initial_yaw_deg: float,
    final_yaw_deg: float,
    initial_drift_m: float,
    final_drift_m: float,
) -> Dict[str, Any]:
    """Measure physical deviation reduction during recovery."""
    yaw_reduction = float(initial_yaw_deg - final_yaw_deg)
    drift_reduction = float(initial_drift_m - final_drift_m)

    yaw_recovered = bool(final_yaw_deg <= 10.0)
    drift_recovered = bool(final_drift_m <= 0.015)
    full_physical_recovery = bool(yaw_recovered and drift_recovered)

    return {
        "yaw_reduction_deg": yaw_reduction,
        "drift_reduction_m": drift_reduction,
        "yaw_recovered": yaw_recovered,
        "drift_recovered": drift_recovered,
        "full_physical_recovery": full_physical_recovery,
    }

