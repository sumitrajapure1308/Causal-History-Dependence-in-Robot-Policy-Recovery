"""Safety Performance Metrics for Causal-History-Recovery.

Monitors force safety limits, workspace boundary containment, and kinematic constraints.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import numpy as np


def compute_safety_metrics(
    trajectory_states: List[Dict[str, Any]],
    contact_forces: List[float],
    force_limit_n: float = 50.0,
    workspace_x: Tuple[float, float] = (0.05, 0.50),
    workspace_y: Tuple[float, float] = (-0.20, 0.20),
) -> Dict[str, Any]:
    """Evaluate trajectory against robotic safety constraints."""
    excessive_force_count = sum(1 for f in contact_forces if f > force_limit_n)
    max_force = float(max(contact_forces)) if contact_forces else 0.0

    workspace_violations = 0
    for s in trajectory_states:
        obj_pos = s.get("object_pos")
        if obj_pos is not None:
            x, y = obj_pos[0], obj_pos[1]
            if not (workspace_x[0] <= x <= workspace_x[1] and workspace_y[0] <= y <= workspace_y[1]):
                workspace_violations += 1

    is_safe = bool(excessive_force_count == 0 and workspace_violations == 0)

    return {
        "is_safe": is_safe,
        "max_contact_force_n": max_force,
        "excessive_force_steps": excessive_force_count,
        "workspace_violations": workspace_violations,
    }

