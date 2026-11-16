"""State Matching Build & Diagnostic Script.

Loads collected candidate failure snapshots and evaluates pairwise physical equivalence:
- Computes component-wise distances and composite matching distance.
- Applies hard rejection filters (horizon, goal, contact count).
- Classifies match tiers (strict, moderate, loose, rejected).
- Saves matching diagnostics to results/pilot_recovery/matching_report.json.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List
import numpy as np

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.state_snapshot import StateSnapshot
from causal_history_recovery.matching.state_matcher import StateMatcher


def build_matches_report(
    snapshot_pairs: List[Dict[str, Any]],
    output_path: str,
) -> Dict[str, Any]:
    """Evaluate candidate snapshot pairs and write matching report."""
    matcher = StateMatcher()

    report_records = []
    tier_counts = {"strict": 0, "moderate": 0, "loose": 0, "rejected": 0}

    for item in snapshot_pairs:
        pair_id = item.get("pair_id", f"pair_{len(report_records)}")
        snap_a = item["snapshot_a"]
        snap_b = item["snapshot_b"]

        eval_res = matcher.evaluate_match(snap_a, snap_b)
        tier = eval_res["tier"]
        tier_counts[tier] = tier_counts.get(tier, 0) + 1

        record = {
            "pair_id": pair_id,
            "source_id": item.get("source_id", "source"),
            "target_id": item.get("target_id", "target"),
            "matched": eval_res["matched"],
            "tier": tier,
            "composite_distance": eval_res["composite_distance"],
            "passed_hard_constraints": eval_res["passed_hard_constraints"],
            "rejection_reasons": eval_res["rejection_reasons"],
            "components": eval_res["components"],
        }
        report_records.append(record)

    summary = {
        "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_pairs_evaluated": len(report_records),
        "tier_distribution": tier_counts,
        "mean_composite_distance": float(
            np.mean([r["composite_distance"] for r in report_records])
        ) if report_records else 0.0,
        "pairs": report_records,
    }

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default="results/pilot_recovery/matching_report.json")
    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_file = os.path.join(repo_root, args.output)
    print(f"State matcher ready. Output target: {out_file}")

