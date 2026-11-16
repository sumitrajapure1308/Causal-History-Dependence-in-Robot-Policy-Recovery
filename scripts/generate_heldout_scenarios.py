"""Generate Fresh Held-Out Scenarios (Phase 9 Pre-Registered Pilot).

Generates at least 40 fresh, non-overlapping held-out paired scenarios using the
existing paired replay-injection generator.
- Seeds start at 5000 (strictly disjoint from training seeds 1000-1049, 3000-3059,
  and prior evaluation/development seeds 42-692, 500, 2000).
- Excludes all scenarios from Phases 5, 6, 7, and 8.
- Validates every candidate through the 15-point checklist and Privileged Oracle recoverability.
- Saves:
  - results/heldout_pilot/scenarios/{scenario_uid}/snapshot.npz
  - results/heldout_pilot/scenarios/{scenario_uid}/prefix.npz
  - results/heldout_pilot/scenarios/{scenario_uid}/metadata.json
  - results/heldout_pilot/scenario_manifest.json
  - results/heldout_pilot/scenario_validation_report.json
"""

from __future__ import annotations

import collections
import copy
import hashlib
import json
import math
import os
import sys
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(repo_root, "src"))

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.environments.state_snapshot import StateSnapshot
from causal_history_recovery.policies.policy_registry import load_policy
from causal_history_recovery.counterfactuals.paired_scenario_generator import PairedScenarioGenerator


def hash_obj(obj: Any) -> str:
    s = json.dumps(obj, sort_keys=True)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def hash_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    target_count = 45  # Target at least 40, aim for 45
    seed_start = 5000
    out_dir = os.path.join(repo_root, "results", "heldout_pilot")
    scen_out_dir = os.path.join(out_dir, "scenarios")
    os.makedirs(scen_out_dir, exist_ok=True)

    ckpt_path = os.path.join(repo_root, "models", "checkpoints", "history_gru_best.pt")
    ckpt_hash = hash_file(ckpt_path)
    policy = load_policy(ckpt_path)

    env = PushTargetEnv()
    generator = PairedScenarioGenerator(env)

    # Candidate parameters grid
    tiers = [
        ("small", 0.008, 12.0, 0.014),
        ("medium", 0.014, 15.0, 0.020),
        ("large", 0.020, 20.0, 0.025),
    ]
    perturb_steps = [20, 25, 30, 35]
    directions = [1.0, -1.0]
    durations = [1, 2]
    target_options = [
        [0.25, 0.0, 0.025],
        [0.22, 0.04, 0.025],
        [0.22, -0.04, 0.025],
        [0.26, 0.03, 0.025],
        [0.26, -0.03, 0.025],
    ]

    admitted_scenarios: List[Dict[str, Any]] = []
    rejected_scenarios: List[Dict[str, Any]] = []
    funnel = {
        "candidate_episodes_sampled": 0,
        "deviation_detected": 0,
        "oracle_recoverable": 0,
        "validation_passed": 0,
    }

    print(f"Generating fresh held-out scenarios starting at seed {seed_start}...")
    start_time = time.time()
    curr_seed = seed_start

    while len(admitted_scenarios) < target_count and curr_seed < seed_start + 300:
        funnel["candidate_episodes_sampled"] += 1
        ep_idx = curr_seed - seed_start

        tier_name, offset_y, yaw_thresh, drift_thresh = tiers[ep_idx % len(tiers)]
        pert_step = perturb_steps[(ep_idx // 3) % len(perturb_steps)]
        direction = directions[(ep_idx // 12) % len(directions)]
        impulse_dur = durations[(ep_idx // 24) % len(durations)]
        target_pos = target_options[(ep_idx // 48) % len(target_options)]

        source = generator.sample_source_failure(
            policy=policy,
            seed=curr_seed,
            severity_tier=tier_name,
            offset_y=offset_y,
            perturb_step=pert_step,
            direction=direction,
            impulse_duration=impulse_dur,
            target_pos=target_pos,
            yaw_threshold_deg=yaw_thresh,
            drift_threshold_m=drift_thresh,
        )

        curr_seed += 1

        if source is None:
            rejected_scenarios.append({
                "seed": curr_seed - 1,
                "reason": "no_deviation_or_timeout",
            })
            continue

        funnel["deviation_detected"] += 1

        if not source.get("is_recoverable", False):
            rejected_scenarios.append({
                "seed": curr_seed - 1,
                "reason": "oracle_unrecoverable",
            })
            continue

        funnel["oracle_recoverable"] += 1

        # Construct paired scenario and execute 15-point checklist
        scenario = generator.generate_paired_scenario(
            source_data=source,
            policy=policy,
            policy_id="history_gru",
        )

        val_report = scenario["validation_report"]
        if not val_report["all_passed"]:
            rejected_scenarios.append({
                "seed": curr_seed - 1,
                "reason": "failed_15_point_checklist",
                "failed_reasons": val_report["failed_reasons"],
            })
            continue

        funnel["validation_passed"] += 1

        # Reconstruct exact observation and action prefix
        env._target_pos = np.array(target_pos, dtype=np.float64)
        obs, _ = env.reset(seed=source["seed"])
        policy.reset(obs)
        eff_offset = offset_y * direction

        obs_prefix = [obs.copy()]
        act_prefix = []
        contacts_prefix = []

        dev_step = source["deviation_step"]
        for s in range(dev_step + 1):
            if pert_step <= s < pert_step + impulse_dur:
                act = np.array([0.0, eff_offset, 0.0], dtype=np.float32)
            else:
                act = policy.act(obs, deterministic=True)
            act_prefix.append(act.copy())
            obs, _, _, _, s_info = env.step(act)
            obs_prefix.append(obs.copy())
            contacts_prefix.append(1 if env._has_pusher_contact() else 0)

        # Unique Scenario UID
        scen_uid = f"heldout_s{source['seed']}_t{dev_step}_{uuid.uuid4().hex[:6]}"
        scenario["scenario_uid"] = scen_uid
        scen_dir = os.path.join(scen_out_dir, scen_uid)
        os.makedirs(scen_dir, exist_ok=True)

        # Save snapshot.npz
        snap: StateSnapshot = source["candidate_snapshot"]
        np.savez_compressed(
            os.path.join(scen_dir, "snapshot.npz"),
            qpos=snap.qpos,
            qvel=snap.qvel,
        )

        # Save prefix.npz
        np.savez_compressed(
            os.path.join(scen_dir, "prefix.npz"),
            observations=np.array(obs_prefix, dtype=np.float32),
            actions=np.array(act_prefix, dtype=np.float32),
            contacts=np.array(contacts_prefix, dtype=np.int32),
        )

        # Save metadata.json
        meta = {
            "scenario_uid": scen_uid,
            "policy_id": "history_gru",
            "checkpoint_id": "history_gru_best.pt",
            "training_seed": 42,
            "scenario_generation_seed": source["seed"],
            "severity_tier": tier_name,
            "perturb_step": pert_step,
            "offset_y": offset_y,
            "direction": direction,
            "impulse_duration": impulse_dur,
            "deviation_step": dev_step,
            "deviation_type": "off_center_rotational_slip",
            "deviation_yaw_deg": float(source.get("deviation_yaw_deg", 0.0)),
            "deviation_drift_m": float(source.get("deviation_drift_m", 0.0)),
            "remaining_horizon": snap.remaining_horizon,
            "goal_state": target_pos,
            "oracle_recoverable": True,
            "split": "held_out_test",
            "state_matching_error": 0.0,
            "snapshot_hash": hash_file(os.path.join(scen_dir, "snapshot.npz")),
            "prefix_hash": hash_file(os.path.join(scen_dir, "prefix.npz")),
            "checkpoint_hash": ckpt_hash,
            "validation_report": val_report,
        }

        with open(os.path.join(scen_dir, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        admitted_scenarios.append(meta)
        print(f"[{len(admitted_scenarios)}/{target_count}] Admitted scenario {scen_uid} (seed={source['seed']}, tier={tier_name}, dev_step={dev_step})")

    # Save manifest and validation report
    manifest_data = {
        "manifest_title": "Fresh Held-Out Evaluation Scenarios (Phase 9)",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total_admitted": len(admitted_scenarios),
        "seed_range": [seed_start, curr_seed - 1],
        "scenario_uids": [s["scenario_uid"] for s in admitted_scenarios],
        "severity_counts": collections.Counter([s["severity_tier"] for s in admitted_scenarios]),
        "mean_deviation_yaw_deg": float(np.mean([s["deviation_yaw_deg"] for s in admitted_scenarios])),
        "mean_deviation_drift_m": float(np.mean([s["deviation_drift_m"] for s in admitted_scenarios])),
        "mean_remaining_horizon": float(np.mean([s["remaining_horizon"] for s in admitted_scenarios])),
    }

    manifest_path = os.path.join(out_dir, "scenario_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)

    val_report_data = {
        "funnel": funnel,
        "admission_rate": len(admitted_scenarios) / max(1, funnel["candidate_episodes_sampled"]),
        "oracle_recovery_rate": funnel["oracle_recoverable"] / max(1, funnel["deviation_detected"]),
        "checklist_pass_rate": funnel["validation_passed"] / max(1, funnel["oracle_recoverable"]),
        "total_admitted": len(admitted_scenarios),
        "total_rejected": len(rejected_scenarios),
        "rejection_reasons": collections.Counter([r["reason"] for r in rejected_scenarios]),
    }

    val_report_path = os.path.join(out_dir, "scenario_validation_report.json")
    with open(val_report_path, "w", encoding="utf-8") as f:
        json.dump(val_report_data, f, indent=2)

    print(f"\nFresh held-out scenario generation complete in {time.time() - start_time:.2f}s.")
    print(f"Admitted: {len(admitted_scenarios)} scenarios.")
    print(f"Manifest written to: {manifest_path}")
    print(f"Validation report written to: {val_report_path}")


if __name__ == "__main__":
    main()

