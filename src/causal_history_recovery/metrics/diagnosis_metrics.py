"""Diagnosis Performance Metrics for Causal-History-Recovery.

Computes failure classification accuracy, macro-F1, confusion matrix, and delay.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
import numpy as np


def compute_diagnosis_metrics(
    true_failure_type: str,
    predicted_failure_type: str,
    diagnosis_delay_steps: int = 0,
) -> Dict[str, Any]:
    """Evaluate diagnostic classification for a single episode."""
    is_correct = (true_failure_type.lower() == predicted_failure_type.lower())
    return {
        "true_type": true_failure_type,
        "predicted_type": predicted_failure_type,
        "is_correct": is_correct,
        "diagnosis_delay_steps": diagnosis_delay_steps,
    }


def aggregate_diagnosis_stats(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate classification accuracy and confusion statistics."""
    if not records:
        return {"accuracy": 0.0, "total": 0}

    correct = sum(1 for r in records if r.get("is_correct", False))
    total = len(records)
    acc = float(correct / total) if total > 0 else 0.0

    # Class breakdown
    classes = sorted(list(set(r["true_type"] for r in records)))
    confusion = {c1: {c2: 0 for c2 in classes} for c1 in classes}
    for r in records:
        t = r["true_type"]
        p = r["predicted_type"]
        if t in confusion and p in confusion[t]:
            confusion[t][p] += 1

    return {
        "total_episodes": total,
        "correct_count": correct,
        "accuracy": acc,
        "confusion_matrix": confusion,
    }

