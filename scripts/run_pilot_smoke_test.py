"""Pilot Diagnostic Smoke Test Script.

Executes a small, bounded technical validation run on PushTargetEnv:
- 1 random seed (seed 42).
- 10 diagnostic test episodes.
- Simple scripted probing policy.
- Outputs pilot_manifest.json and pilot_metrics.json in results/pilot/.

DISCLAIMER:
This script produces technical diagnostic smoke test data to verify pipeline
execution integrity only. It does NOT generate official benchmark results,
experimental policy comparisons, or paper statistics.
"""

from __future__ import annotations

import json
import os
import sys
import time
import numpy as np

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.push_target_env import PushTargetEnv


def run_pilot_smoke_test():
    """Run 10 diagnostic smoke test episodes under seed 42."""
    seed = 42
    num_episodes = 10
    max_horizon = 150
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results", "pilot"))
    os.makedirs(output_dir, exist_ok=True)

    env = PushTargetEnv(max_horizon=max_horizon)
    episodes_data = []

    start_time = time.time()

    for ep_idx in range(num_episodes):
        ep_seed = seed + ep_idx * 100
        obs, info = env.reset(seed=ep_seed)
        obj_init = env.get_object_position().copy()

        ep_steps = 0
        ep_contacts = 0
        ep_success = False
        deviation_detected = False
        yaw_max = 0.0
        drift_max = 0.0

        # Scripted probing policy: alternating straight and slight lateral probe
        # to test contact generation, slip mechanics, and horizon termination
        probe_mode = ep_idx % 3  # 0: straight push, 1: positive lateral offset, 2: negative lateral offset

        for step in range(max_horizon):
            if step < 5:
                # Approach phase
                if probe_mode == 1:
                    act = np.array([0.002, 0.003, 0.0])
                elif probe_mode == 2:
                    act = np.array([0.002, -0.003, 0.0])
                else:
                    act = np.array([0.004, 0.0, 0.0])
            else:
                # Push phase
                act = np.array([0.004, 0.0, 0.0])

            obs, reward, terminated, truncated, step_info = env.step(act)
            ep_steps += 1

            if step_info["has_pusher_contact"]:
                ep_contacts += 1

            cur_yaw_deg = abs(np.degrees(step_info["object_yaw_rad"]))
            cur_drift_m = abs(step_info["object_pos"][1] - obj_init[1])
            yaw_max = max(yaw_max, cur_yaw_deg)
            drift_max = max(drift_max, cur_drift_m)

            if cur_yaw_deg >= 15.0 and cur_drift_m >= 0.020:
                deviation_detected = True

            if step_info["is_success"]:
                ep_success = True
                break

            if terminated or truncated:
                break

        ep_record = {
            "episode_index": ep_idx,
            "seed": ep_seed,
            "probe_mode": probe_mode,
            "steps_executed": ep_steps,
            "success": ep_success,
            "dwell_count": step_info.get("dwell_count", 0),
            "final_dist_to_goal": float(step_info.get("dist_to_goal", 0.0)),
            "peak_yaw_deg": float(yaw_max),
            "peak_lateral_drift_m": float(drift_max),
            "deviation_detected": bool(deviation_detected),
            "contact_steps": ep_contacts,
            "termination_reason": "success" if ep_success else ("terminated" if terminated else "truncated"),
        }
        episodes_data.append(ep_record)

    total_duration = time.time() - start_time

    # Manifest file
    manifest = {
        "manifest_type": "diagnostic_smoke_test_manifest",
        "verification_status": "validated_diagnostic_smoke_test",
        "official_experimental_result": False,
        "disclaimer": "DIAGNOSTIC SMOKE TEST ONLY. STRICTLY NOT AN OFFICIAL EXPERIMENT OR BENCHMARK RESULT.",
        "environment": "planned_custom_push_target_env",
        "base_seed": seed,
        "episodes_planned": num_episodes,
        "episodes_executed": len(episodes_data),
        "total_runtime_seconds": float(total_duration),
        "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "output_files": [
            "results/pilot/pilot_manifest.json",
            "results/pilot/pilot_metrics.json",
        ],
        "configuration": {
            "task_yaml": "configs/tasks/push_target.yaml",
            "determinism_yaml": "configs/matching/determinism.yaml",
            "max_horizon": max_horizon,
        },
    }

    # Summary metrics file
    metrics = {
        "metadata": {
            "status": "validated_diagnostic_smoke_test",
            "official_experimental_result": False,
            "disclaimer": "TECHNICAL SANITY CHECK ONLY. NOT A SCIENTIFIC FINDING.",
            "total_episodes": len(episodes_data),
            "base_seed": seed,
        },
        "diagnostic_summary": {
            "total_episodes": len(episodes_data),
            "successful_episodes": sum(1 for e in episodes_data if e["success"]),
            "deviation_episodes": sum(1 for e in episodes_data if e["deviation_detected"]),
            "mean_steps_per_episode": float(np.mean([e["steps_executed"] for e in episodes_data])),
            "mean_contacts_per_episode": float(np.mean([e["contact_steps"] for e in episodes_data])),
            "mean_final_dist_to_goal_m": float(np.mean([e["final_dist_to_goal"] for e in episodes_data])),
            "mean_peak_yaw_deg": float(np.mean([e["peak_yaw_deg"] for e in episodes_data])),
            "mean_peak_drift_m": float(np.mean([e["peak_lateral_drift_m"] for e in episodes_data])),
        },
        "episodes": episodes_data,
    }

    manifest_path = os.path.join(output_dir, "pilot_manifest.json")
    metrics_path = os.path.join(output_dir, "pilot_metrics.json")

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"Pilot smoke test finished successfully in {total_duration:.2f}s.")
    print(f"Saved manifest: {manifest_path}")
    print(f"Saved metrics: {metrics_path}")


if __name__ == "__main__":
    run_pilot_smoke_test()

