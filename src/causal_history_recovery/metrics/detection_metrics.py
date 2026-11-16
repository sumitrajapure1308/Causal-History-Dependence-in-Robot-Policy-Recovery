"""Detection Performance Metrics for Causal-History-Recovery.

Computes failure detection delay, detection rate, false positives, and calibration.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import numpy as np


def compute_detection_metrics(
    perturb_step: int,
    detected_step: Optional[int],
    is_perturbed: bool = True,
    confidence: float = 1.0,
) -> Dict[str, Any]:
    """Compute detection latency, accuracy, and confidence metrics."""
    if not is_perturbed:
        # Nominal rollout
        false_positive = detected_step is not None
        return {
            "is_perturbed": False,
            "detected": false_positive,
            "false_positive": false_positive,
            "false_negative": False,
            "detection_delay": None,
            "confidence": confidence,
        }

    # Perturbed rollout
    if detected_step is not None:
        delay = max(0, detected_step - perturb_step)
        detected = True
        false_negative = False
    else:
        delay = None
        detected = False
        false_negative = True

    return {
        "is_perturbed": True,
        "detected": detected,
        "false_positive": False,
        "false_negative": false_negative,
        "detection_delay": delay,
        "confidence": confidence,
    }


def aggregate_detection_stats(detection_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate detection metrics across a cohort of rollouts."""
    if not detection_records:
        return {"detection_rate": 0.0, "mean_delay": 0.0, "fp_rate": 0.0}

    perturbed = [r for r in detection_records if r.get("is_perturbed", True)]
    delays = [r["detection_delay"] for r in perturbed if r.get("detection_delay") is not None]
    det_count = sum(1 for r in perturbed if r.get("detected", False))

    det_rate = float(det_count / len(perturbed)) if perturbed else 0.0
    mean_delay = float(np.mean(delays)) if delays else 0.0

    return {
        "total_perturbed": len(perturbed),
        "detected_count": det_count,
        "detection_rate": det_rate,
        "mean_detection_delay_steps": mean_delay,
    }

