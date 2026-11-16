"""State Matching and Distance Measurement Module.

Computes multi-dimensional physical state distances between StateSnapshot pairs:
- Component distances across joint positions, velocities, end-effector pose,
  object 6D pose, and contact topology.
- Hard rejection filters enforcing exact horizon and goal equality.
- Tiered matching classification (strict, moderate, loose, rejected).
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import yaml

from causal_history_recovery.environments.state_snapshot import StateSnapshot


class StateMatcher:
    """Evaluates physical equivalence between two simulation state snapshots."""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            config_path = os.path.join(repo_root, "configs", "matching", "weights.yaml")

        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        self.weights = self.config.get("weights", {})
        self.tiers = self.config.get("tolerance_tiers", {})
        self.hard_constraints = self.config.get("hard_constraints", {})

    def compute_component_distances(
        self,
        snap1: StateSnapshot,
        snap2: StateSnapshot,
    ) -> Dict[str, float]:
        """Compute individual physical distance metrics between two snapshots."""
        d_qpos = float(np.linalg.norm(snap1.qpos - snap2.qpos))
        d_qvel = float(np.linalg.norm(snap1.qvel - snap2.qvel))

        d_ee = float(np.linalg.norm(snap1.end_effector_pos - snap2.end_effector_pos))

        d_obj_pos = float(np.linalg.norm(snap1.object_pos[:3] - snap2.object_pos[:3]))

        # Geodesic angular distance on quaternion 3-sphere: 2 * arccos(|<q1, q2>|)
        q1 = snap1.object_rot / np.linalg.norm(snap1.object_rot)
        q2 = snap2.object_rot / np.linalg.norm(snap2.object_rot)
        inner = float(np.clip(abs(np.dot(q1, q2)), 0.0, 1.0))
        d_obj_rot = float(2.0 * np.arccos(inner))

        d_contact = float(abs(snap1.active_contacts_count - snap2.active_contacts_count))

        d_goal = 0.0
        if snap1.task_goal is not None and snap2.task_goal is not None:
            d_goal = float(np.linalg.norm(snap1.task_goal - snap2.task_goal))

        horizon_diff = abs(snap1.remaining_horizon - snap2.remaining_horizon)

        return {
            "d_qpos": d_qpos,
            "d_qvel": d_qvel,
            "d_ee_pos": d_ee,
            "d_obj_pos": d_obj_pos,
            "d_obj_rot_rad": d_obj_rot,
            "d_contact_count": d_contact,
            "d_goal": d_goal,
            "horizon_diff": float(horizon_diff),
        }

    def compute_composite_distance(
        self,
        snap1: StateSnapshot,
        snap2: StateSnapshot,
    ) -> Tuple[float, Dict[str, float]]:
        """Calculate weighted composite physical distance."""
        comps = self.compute_component_distances(snap1, snap2)

        composite = (
            self.weights.get("joint_positions", 0.15) * comps["d_qpos"]
            + self.weights.get("joint_velocities", 0.10) * comps["d_qvel"]
            + self.weights.get("end_effector_position", 0.20) * comps["d_ee_pos"]
            + self.weights.get("object_position", 0.20) * comps["d_obj_pos"]
            + self.weights.get("object_orientation", 0.10) * comps["d_obj_rot_rad"]
            + self.weights.get("contact_graph", 0.05) * comps["d_contact_count"]
        )

        return float(composite), comps

    def evaluate_match(
        self,
        snap1: StateSnapshot,
        snap2: StateSnapshot,
    ) -> Dict[str, Any]:
        """Check hard constraints and classify match tier."""
        comp_dist, comps = self.compute_composite_distance(snap1, snap2)

        # Check hard constraints
        passed_hard = True
        rejection_reasons = []

        if self.hard_constraints.get("require_identical_goal", True) and comps["d_goal"] > 1e-6:
            passed_hard = False
            rejection_reasons.append("goal_mismatch")

        if self.hard_constraints.get("require_identical_horizon", True) and comps["horizon_diff"] > 0:
            passed_hard = False
            rejection_reasons.append("horizon_mismatch")

        if self.hard_constraints.get("require_contact_indicator_match", True) and comps["d_contact_count"] > 0:
            passed_hard = False
            rejection_reasons.append("contact_count_mismatch")

        # Determine tier
        tier = "rejected"
        if passed_hard:
            strict_eps = self.tiers.get("strict", {}).get("composite_epsilon", 0.010)
            mod_eps = self.tiers.get("moderate", {}).get("composite_epsilon", 0.030)
            loose_eps = self.tiers.get("loose", {}).get("composite_epsilon", 0.075)

            if comp_dist <= strict_eps:
                tier = "strict"
            elif comp_dist <= mod_eps:
                tier = "moderate"
            elif comp_dist <= loose_eps:
                tier = "loose"
            else:
                rejection_reasons.append("composite_distance_exceeded_loose_bound")

        return {
            "matched": bool(tier in ["strict", "moderate", "loose"]),
            "tier": tier,
            "composite_distance": comp_dist,
            "components": comps,
            "passed_hard_constraints": passed_hard,
            "rejection_reasons": rejection_reasons,
        }

    def find_best_match(
        self,
        target_snap: StateSnapshot,
        candidate_pool: List[StateSnapshot],
    ) -> Optional[Tuple[int, Dict[str, Any]]]:
        """Find the closest valid matching state from a candidate pool."""
        best_idx = None
        best_eval = None
        min_dist = float("inf")

        for idx, candidate in enumerate(candidate_pool):
            eval_res = self.evaluate_match(target_snap, candidate)
            if eval_res["matched"] and eval_res["composite_distance"] < min_dist:
                min_dist = eval_res["composite_distance"]
                best_idx = idx
                best_eval = eval_res

        if best_idx is not None:
            return best_idx, best_eval
        return None

