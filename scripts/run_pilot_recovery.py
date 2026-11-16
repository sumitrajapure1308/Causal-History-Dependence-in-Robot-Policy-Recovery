"""Master Pilot Recovery Rollout Pipeline.

Orchestrates the complete Phase 3 pilot recovery rollout:
- 1 seed (seed 42).
- 20 episodes per policy (Reactive MLP and History-aware GRU).
- Evaluates nominal execution and off-center slip deviation.
- Evaluates counterfactual conditions (B0, B2, B4) filtered by the privileged oracle.
- Evaluates state matching diagnostics between candidate snapshots.
- Outputs complete manifest, metrics, and condition reports to results/pilot_recovery/.
"""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Any, Dict, List
import numpy as np

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.policies.policy_registry import load_policy
from causal_history_recovery.rollout.episode_logger import EpisodeLogger
from causal_history_recovery.rollout.rollout_collector import RolloutCollector
from causal_history_recovery.controllers.privileged_oracle import PrivilegedOracleController
from causal_history_recovery.counterfactuals.condition_generator import ConditionGenerator
from causal_history_recovery.matching.state_matcher import StateMatcher


def execute_full_pilot():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(repo_root, "results", "pilot_recovery")
    ep_dir = os.path.join(out_dir, "episodes")
    os.makedirs(ep_dir, exist_ok=True)

    base_seed = 42
    episodes_per_policy = 20
    policies_to_test = ["reactive_mlp", "history_gru"]
    conditions_to_test = ["B0", "B2", "B4"]

    start_total_time = time.time()
    env = PushTargetEnv(max_horizon=150)
    logger = EpisodeLogger(ep_dir)
    oracle = PrivilegedOracleController()
    cond_gen = ConditionGenerator(env)
    matcher = StateMatcher()

    summary_metrics = {
        "metadata": {
            "status": "validated_pilot_rollout",
            "official_experimental_result": False,
            "disclaimer": "PHASE 3 PILOT VALIDATION ONLY. NOT AN OFFICIAL BENCHMARK RESULT.",
            "base_seed": base_seed,
            "episodes_per_policy": episodes_per_policy,
            "policies": policies_to_test,
            "conditions": conditions_to_test,
        },
        "nominal_evaluation": {},
        "deviation_evaluation": {},
        "recovery_evaluation": {},
    }

    all_candidate_snapshots = []
    condition_reports_by_policy = {}

    for pol_name in policies_to_test:
        ckpt_path = os.path.join(repo_root, "models", "checkpoints", f"{pol_name}_best.pt")
        policy = load_policy(ckpt_path, device="cpu")
        collector = RolloutCollector(env, logger, checkpoint_path=ckpt_path)

        # 1. Nominal Evaluation
        print(f"\n--- Running 20 Nominal Episodes for {pol_name} ---")
        nominal_successes = 0
        nominal_steps_list = []
        nominal_dist_list = []

        for idx in range(episodes_per_policy):
            seed = base_seed + idx * 7
            res = collector.run_nominal_rollout(policy, seed=seed, policy_id=pol_name, condition="nominal")
            if res["is_success"]:
                nominal_successes += 1
            nominal_steps_list.append(res["steps"])
            nominal_dist_list.append(res["final_dist_to_goal"])

        summary_metrics["nominal_evaluation"][pol_name] = {
            "success_rate": float(nominal_successes / episodes_per_policy),
            "success_count": nominal_successes,
            "total": episodes_per_policy,
            "mean_steps": float(np.mean(nominal_steps_list)),
            "mean_final_dist_to_goal_m": float(np.mean(nominal_dist_list)),
        }
        print(f"Nominal {pol_name}: {nominal_successes}/{episodes_per_policy} successful ({nominal_successes/episodes_per_policy*100:.1f}%)")

        # 2. Induced Deviation & Recovery Condition Evaluation
        print(f"--- Running 20 Induced Deviation Episodes for {pol_name} ---")
        dev_count = 0
        yaw_list = []
        drift_list = []
        admitted_scenarios = []

        cond_success = {c: 0 for c in conditions_to_test}

        for idx in range(episodes_per_policy):
            seed = base_seed + idx * 7

            # Rollout with perturbation to induce slip
            obs, info = env.reset(seed=seed)
            policy.reset(obs)
            obj_init = env.get_object_position().copy()

            action_prefix = []
            dev_detected = False
            dev_time = None
            snap_cand = None

            for step in range(150):
                if step == 25:
                    act = np.array([0.0, 0.016, 0.0], dtype=np.float32)
                else:
                    act = policy.act(obs, deterministic=True)

                action_prefix.append(act.copy())
                obs, r, term, trunc, step_info = env.step(act)

                yaw_deg = abs(np.degrees(env.get_object_yaw()))
                drift_m = abs(env.get_object_position()[1] - obj_init[1])

                if step >= 25 and not dev_detected:
                    if yaw_deg >= 15.0 and drift_m >= 0.020:
                        dev_detected = True
                        dev_time = step
                        snap_cand = env.get_state_snapshot()
                        yaw_list.append(yaw_deg)
                        drift_list.append(drift_m)
                        break

                if term or trunc:
                    break

            if dev_detected and snap_cand is not None:
                dev_count += 1
                all_candidate_snapshots.append(snap_cand)

                # Query oracle filter
                admitted, oracle_audit = oracle.verify_scenario_recoverability(env, snap_cand)
                if admitted:
                    scenario_res = {"episode_idx": idx, "seed": seed, "dev_time": dev_time, "conditions": {}}

                    for cond in conditions_to_test:
                        prep = cond_gen.prepare_condition_rollout(
                            condition=cond,
                            policy=policy,
                            source_snapshot=snap_cand,
                            action_prefix=action_prefix,
                            seed=seed,
                        )

                        cur_obs = prep["current_observation"]
                        rem_h = prep["remaining_horizon"]
                        succ = False

                        for t in range(rem_h):
                            act = policy.act(cur_obs, deterministic=True)
                            cur_obs, r, term, trunc, s_info = env.step(act)
                            if s_info["is_success"]:
                                succ = True
                                break
                            if term or trunc:
                                break

                        if succ:
                            cond_success[cond] += 1
                        scenario_res["conditions"][cond] = {
                            "success": succ,
                            "error": prep["state_matching_error"],
                        }

                    admitted_scenarios.append(scenario_res)

        summary_metrics["deviation_evaluation"][pol_name] = {
            "deviations_detected": dev_count,
            "detection_rate": float(dev_count / episodes_per_policy),
            "mean_yaw_deg": float(np.mean(yaw_list)) if yaw_list else 0.0,
            "mean_drift_m": float(np.mean(drift_list)) if drift_list else 0.0,
            "oracle_admitted_count": len(admitted_scenarios),
        }

        summary_metrics["recovery_evaluation"][pol_name] = {
            "admitted_scenarios": len(admitted_scenarios),
            "condition_success_counts": cond_success,
            "condition_recovery_rates": {
                c: float(cond_success[c] / len(admitted_scenarios)) if admitted_scenarios else 0.0
                for c in conditions_to_test
            },
            "scenarios": admitted_scenarios,
        }

        print(f"Deviation {pol_name}: {dev_count}/{episodes_per_policy} deviations detected | Oracle admitted: {len(admitted_scenarios)}")
        print(f"Recovery Rates {pol_name}: {summary_metrics['recovery_evaluation'][pol_name]['condition_recovery_rates']}")

    # 3. State Matching Diagnostics across candidate snapshots
    print("\n--- Running State Matching Diagnostics ---")
    pair_records = []
    tier_counts = {"strict": 0, "moderate": 0, "loose": 0, "rejected": 0}
    matching_errors = []

    # Compare snapshots pairwise
    for i in range(min(len(all_candidate_snapshots), 10)):
        for j in range(i + 1, min(len(all_candidate_snapshots), 10)):
            snap_i = all_candidate_snapshots[i]
            snap_j = all_candidate_snapshots[j]
            eval_res = matcher.evaluate_match(snap_i, snap_j)
            tier = eval_res["tier"]
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
            matching_errors.append(eval_res["composite_distance"])

            pair_records.append({
                "pair_id": f"pair_{i}_{j}",
                "tier": tier,
                "composite_distance": eval_res["composite_distance"],
                "passed_hard": eval_res["passed_hard_constraints"],
                "reasons": eval_res["rejection_reasons"],
            })

    matching_report = {
        "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_pairs_tested": len(pair_records),
        "tier_distribution": tier_counts,
        "mean_composite_distance": float(np.mean(matching_errors)) if matching_errors else 0.0,
        "pairs": pair_records,
    }

    matching_path = os.path.join(out_dir, "matching_report.json")
    with open(matching_path, "w", encoding="utf-8") as f:
        json.dump(matching_report, f, indent=2)

    condition_path = os.path.join(out_dir, "condition_report.json")
    with open(condition_path, "w", encoding="utf-8") as f:
        json.dump(summary_metrics["recovery_evaluation"], f, indent=2)

    metrics_path = os.path.join(out_dir, "rollout_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(summary_metrics, f, indent=2)

    total_duration = time.time() - start_total_time

    manifest = {
        "manifest_type": "pilot_recovery_rollout_manifest",
        "verification_status": "validated_pilot_rollout",
        "official_experimental_result": False,
        "disclaimer": "PHASE 3 PILOT ROLLOUT ONLY. STRICTLY NOT AN OFFICIAL EXPERIMENTAL BENCHMARK RESULT.",
        "environment": "planned_custom_push_target_env",
        "base_seed": base_seed,
        "episodes_per_policy": episodes_per_policy,
        "total_episodes_executed": episodes_per_policy * len(policies_to_test) * 2,
        "total_runtime_seconds": float(total_duration),
        "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "output_files": [
            "results/pilot_recovery/rollout_manifest.json",
            "results/pilot_recovery/rollout_metrics.json",
            "results/pilot_recovery/matching_report.json",
            "results/pilot_recovery/condition_report.json",
            "results/pilot_recovery/episodes/",
        ],
        "policies_tested": policies_to_test,
        "conditions_tested": conditions_to_test,
    }

    manifest_path = os.path.join(out_dir, "rollout_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nPilot Recovery Pipeline completed successfully in {total_duration:.2f}s.")
    print(f"Saved manifest: {manifest_path}")
    print(f"Saved metrics: {metrics_path}")
    print(f"Saved matching report: {matching_path}")
    print(f"Saved condition report: {condition_path}")


if __name__ == "__main__":
    execute_full_pilot()

