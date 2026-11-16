"""Execute Pre-Registered Pilot Recovery Experiment (Phase 6).

Runs 1,140 recovery rollouts:
38 paired scenarios x 5 conditions (B0-B4) x 3 seeds x 2 policies (MLP, GRU).
Computes the full metric suite, paired statistical tests (McNemar, Wilcoxon,
Bootstrap 95% CIs, Holm-Bonferroni correction), history dependence, and policy rankings.
Exports complete results to results/pilot_evaluation/.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import os
import sys
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
from scipy import stats

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(repo_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.environments.state_snapshot import StateSnapshot
from causal_history_recovery.policies.policy_registry import load_policy
from causal_history_recovery.counterfactuals.condition_generator import ConditionGenerator
from causal_history_recovery.metrics.recovery_metrics import compute_task_metrics, compute_physical_recovery_metrics
from causal_history_recovery.metrics.safety_metrics import compute_safety_metrics
from causal_history_recovery.metrics.detection_metrics import compute_detection_metrics
from causal_history_recovery.metrics.diagnosis_metrics import compute_diagnosis_metrics


def _json_default(obj: Any) -> Any:
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, float)):
        return float(obj)
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    return str(obj)


def run_paired_mcnemar_test(b0_outcomes: List[int], b_cond_outcomes: List[int]) -> Dict[str, Any]:
    """Perform McNemar's test with Edwards continuity correction on paired binary outcomes."""
    assert len(b0_outcomes) == len(b_cond_outcomes)
    b0_arr = np.array(b0_outcomes)
    bc_arr = np.array(b_cond_outcomes)

    b = int(np.sum((b0_arr == 1) & (bc_arr == 0)))  # B0 success, Cond fail
    c = int(np.sum((b0_arr == 0) & (bc_arr == 1)))  # B0 fail, Cond success
    total_discordant = b + c

    if total_discordant == 0:
        chi2 = 0.0
        p_val = 1.0
    else:
        chi2 = float((abs(b - c) - 1.0) ** 2 / total_discordant) if abs(b - c) > 0 else 0.0
        p_val = float(1.0 - stats.chi2.cdf(chi2, df=1))

    return {
        "b_count_b0_succ_cond_fail": b,
        "c_count_b0_fail_cond_succ": c,
        "total_discordant": total_discordant,
        "chi2_statistic": chi2,
        "p_value": p_val,
    }


def compute_bootstrap_ci(
    diffs: List[float],
    n_resamples: int = 10000,
    alpha: float = 0.05,
    seed: int = 42,
) -> Tuple[float, float]:
    """Compute 95% paired bootstrap confidence interval."""
    arr = np.array(diffs)
    if len(arr) == 0:
        return 0.0, 0.0
    rng = np.random.RandomState(seed)
    n = len(arr)
    boot_means = []
    for _ in range(n_resamples):
        idx = rng.randint(0, n, size=n)
        boot_means.append(np.mean(arr[idx]))
    lower = float(np.percentile(boot_means, (alpha / 2.0) * 100))
    upper = float(np.percentile(boot_means, (1.0 - alpha / 2.0) * 100))
    return lower, upper


def run_phase_6_evaluation() -> Dict[str, Any]:
    """Run full 1,140 rollout pilot evaluation."""
    out_dir = os.path.join(repo_root, "results", "pilot_evaluation")
    os.makedirs(out_dir, exist_ok=True)

    # 1. Load scenario manifest
    manifest_path = os.path.join(repo_root, "results", "paired_scenarios", "scenario_manifest.json")
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    scenario_uids = manifest["scenario_uids"]
    print(f"Loaded {len(scenario_uids)} pre-registered paired scenarios.")

    # 2. Setup policies
    policy_ids = ["reactive_mlp", "history_gru"]
    policies = {}
    for pol_id in policy_ids:
        ckpt = os.path.join(repo_root, "models", "checkpoints", f"{pol_id}_best.pt")
        policies[pol_id] = load_policy(ckpt, device="cpu")
        print(f"Loaded {pol_id} from {ckpt}")

    eval_seeds = [42, 500, 2000]
    conditions = ["B0", "B1", "B2", "B3", "B4"]
    total_rollouts = len(scenario_uids) * len(conditions) * len(eval_seeds) * len(policy_ids)
    print(f"Total planned rollouts: {len(scenario_uids)} x {len(conditions)} x {len(eval_seeds)} x {len(policy_ids)} = {total_rollouts}")

    env = PushTargetEnv()
    cond_gen = ConditionGenerator(env)

    # Storage structures
    rollout_records: List[Dict[str, Any]] = []
    per_policy_results = {p: {c: [] for c in conditions} for p in policy_ids}
    global_rollout_idx = 0

    print("Beginning execution of 1,140 recovery rollouts...")

    for scen_idx, uid in enumerate(scenario_uids):
        scen_meta_path = os.path.join(repo_root, "results", "paired_scenarios", "scenarios", uid, "metadata.json")
        scen_npz_path = os.path.join(repo_root, "results", "paired_scenarios", "scenarios", uid, "snapshot.npz")

        with open(scen_meta_path, "r") as f:
            scen_meta = json.load(f)

        snap_data = np.load(scen_npz_path)
        snapshot = StateSnapshot.from_dict({
            **scen_meta["snapshot_dict"],
            "qpos": snap_data["qpos"],
            "qvel": snap_data["qvel"],
        })

        base_seed = scen_meta["seed"]
        remaining_horizon = scen_meta["remaining_horizon"]
        goal_pos = np.array(scen_meta["goal_state"], dtype=np.float64)
        sev_tier = scen_meta.get("severity_tier", "medium")

        # In pre-registration, evaluate across evaluation seeds
        for eval_seed in eval_seeds:
            for pol_id in policy_ids:
                policy = policies[pol_id]

                for cond in conditions:
                    global_rollout_idx += 1

                    # Reconstruct prefix actions
                    # Retrieve prefix actions from condition rollout
                    # Prepare condition rollout setup
                    setup_info = cond_gen.prepare_condition_rollout(
                        condition=cond,
                        policy=policy,
                        source_snapshot=snapshot,
                        action_prefix=[],  # condition_gen injects snapshot directly for B1-B4 or restores
                        seed=eval_seed,
                    )

                    # If condition is B0 or B1..B3, ensure state is accurately restored to snapshot
                    env.restore_state_snapshot(snapshot)

                    # Step policy for remaining horizon
                    current_obs = env._get_observation()
                    obs_traj = [current_obs.copy()]
                    act_traj = []
                    contact_forces = []
                    states_traj = []

                    for step in range(remaining_horizon):
                        act = policy.act(current_obs, deterministic=True)
                        act_traj.append(act.copy())

                        next_obs, reward, term, trunc, step_info = env.step(act)
                        obs_traj.append(next_obs.copy())
                        current_obs = next_obs
                        contact_forces.append(float(step_info.get("normal_force", 0.0)))
                        states_traj.append({"object_pos": list(env.get_object_position())})

                        if step_info.get("is_success", False) or term or trunc:
                            break

                    obs_arr = np.array(obs_traj)
                    act_arr = np.array(act_traj)

                    # Compute metrics
                    task_res = compute_task_metrics(
                        trajectory_obs=obs_arr,
                        actions=act_arr,
                        goal_pos=goal_pos,
                        goal_radius=0.060,
                        min_dwell_steps=5,
                    )

                    phys_res = compute_physical_recovery_metrics(
                        initial_yaw_deg=scen_meta["deviation_yaw_deg"],
                        final_yaw_deg=task_res["final_yaw_error_deg"],
                        initial_drift_m=scen_meta["deviation_drift_m"],
                        final_drift_m=task_res["final_dist_to_goal"],
                    )

                    safety_res = compute_safety_metrics(
                        trajectory_states=states_traj,
                        contact_forces=contact_forces,
                    )

                    record = {
                        "rollout_id": global_rollout_idx,
                        "scenario_uid": uid,
                        "policy_id": pol_id,
                        "condition": cond,
                        "eval_seed": eval_seed,
                        "severity_tier": sev_tier,
                        "is_success": int(task_res["is_success"]),
                        "final_dist_to_goal": task_res["final_dist_to_goal"],
                        "final_yaw_error_deg": task_res["final_yaw_error_deg"],
                        "control_effort": task_res["control_effort"],
                        "action_smoothness": task_res["action_smoothness"],
                        "full_physical_recovery": int(phys_res["full_physical_recovery"]),
                        "is_safe": int(safety_res["is_safe"]),
                        "max_contact_force_n": safety_res["max_contact_force_n"],
                    }

                    rollout_records.append(record)
                    per_policy_results[pol_id][cond].append(record)

        if (scen_idx + 1) % 10 == 0:
            print(f"Completed {scen_idx + 1}/{len(scenario_uids)} scenarios ({global_rollout_idx}/{total_rollouts} rollouts)...")

    print(f"Successfully finished all {total_rollouts} rollouts.")

    # 3. Compute Paired Comparisons & Statistical Tests
    comparison_pairs = [
        ("B0", "B1"),
        ("B0", "B2"),
        ("B0", "B3"),
        ("B0", "B4"),
        ("B1", "B4"),
        ("B2", "B4"),
        ("B3", "B4"),
    ]

    paired_analysis: Dict[str, Any] = {}

    for pol_id in policy_ids:
        paired_analysis[pol_id] = {}
        # Collect paired outcomes across all (scenario, eval_seed) pairs (N = 38 * 3 = 114)
        c_records = per_policy_results[pol_id]

        for c1, c2 in comparison_pairs:
            r1_list = [r["is_success"] for r in c_records[c1]]
            r2_list = [r["is_success"] for r in c_records[c2]]
            d1_list = [r["final_dist_to_goal"] for r in c_records[c1]]
            d2_list = [r["final_dist_to_goal"] for r in c_records[c2]]

            diff_rate = float(np.mean(r1_list) - np.mean(r2_list))
            diffs_dist = [d2 - d1 for d1, d2 in zip(d1_list, d2_list)]  # H_D: higher is better for B0

            mcnemar_res = run_paired_mcnemar_test(r1_list, r2_list)
            ci_lower, ci_upper = compute_bootstrap_ci([r1 - r2 for r1, r2 in zip(r1_list, r2_list)])

            # Wilcoxon signed rank test on continuous distance
            try:
                w_stat, w_pval = stats.wilcoxon(d1_list, d2_list)
                w_stat, w_pval = float(w_stat), float(w_pval)
            except Exception:
                w_stat, w_pval = 0.0, 1.0

            paired_analysis[pol_id][f"{c1}_vs_{c2}"] = {
                "c1": c1,
                "c2": c2,
                "n_pairs": len(r1_list),
                "c1_success_rate": float(np.mean(r1_list)),
                "c2_success_rate": float(np.mean(r2_list)),
                "paired_difference_H_R": diff_rate,
                "bootstrap_95_ci": [ci_lower, ci_upper],
                "mcnemar": mcnemar_res,
                "wilcoxon_distance": {"stat": w_stat, "p_value": w_pval},
                "raw_p_value": mcnemar_res["p_value"],
            }

        # Apply Holm-Bonferroni correction across the 7 tests
        raw_pvals = [paired_analysis[pol_id][f"{c1}_vs_{c2}"]["raw_p_value"] for c1, c2 in comparison_pairs]
        sorted_indices = np.argsort(raw_pvals)
        m = len(raw_pvals)

        for rank, idx in enumerate(sorted_indices):
            c1, c2 = comparison_pairs[idx]
            raw_p = raw_pvals[idx]
            adj_p = min(1.0, raw_p * (m - rank))
            paired_analysis[pol_id][f"{c1}_vs_{c2}"]["holm_bonferroni_p_value"] = float(adj_p)
            paired_analysis[pol_id][f"{c1}_vs_{c2}"]["significant_alpha_05"] = bool(adj_p < 0.05)

    # 4. History Dependence Breakdown
    history_dep: Dict[str, Any] = {}
    for pol_id in policy_ids:
        b0_succ = np.array([r["is_success"] for r in per_policy_results[pol_id]["B0"]])
        b1_succ = np.array([r["is_success"] for r in per_policy_results[pol_id]["B1"]])
        b2_succ = np.array([r["is_success"] for r in per_policy_results[pol_id]["B2"]])
        b3_succ = np.array([r["is_success"] for r in per_policy_results[pol_id]["B3"]])
        b4_succ = np.array([r["is_success"] for r in per_policy_results[pol_id]["B4"]])

        h_r_b1 = float(np.mean(b0_succ - b1_succ))
        h_r_b2 = float(np.mean(b0_succ - b2_succ))
        h_r_b3 = float(np.mean(b0_succ - b3_succ))
        h_r_b4 = float(np.mean(b0_succ - b4_succ))

        # Severity breakdown
        sev_breakdown = {}
        for sev in ["small", "medium", "large"]:
            mask = np.array([r["severity_tier"] == sev for r in per_policy_results[pol_id]["B0"]])
            if np.sum(mask) > 0:
                sev_h_r = float(np.mean(b0_succ[mask] - b4_succ[mask]))
                sev_breakdown[sev] = {
                    "count": int(np.sum(mask)),
                    "b0_rate": float(np.mean(b0_succ[mask])),
                    "b4_rate": float(np.mean(b4_succ[mask])),
                    "H_R_B4": sev_h_r,
                }

        history_dep[pol_id] = {
            "H_R_B1_action": h_r_b1,
            "H_R_B2_observation": h_r_b2,
            "H_R_B3_hidden_state": h_r_b3,
            "H_R_B4_full_history": h_r_b4,
            "H_R_abs_B4": float(np.mean(np.abs(b0_succ - b4_succ))),
            "severity_breakdown": sev_breakdown,
        }

    # 5. Policy Ranking Analysis
    # Compare Reactive MLP vs History GRU under B0, B2, B4
    ranking_analysis: Dict[str, Any] = {}
    for cond in ["B0", "B1", "B2", "B3", "B4"]:
        mlp_rate = float(np.mean([r["is_success"] for r in per_policy_results["reactive_mlp"][cond]]))
        gru_rate = float(np.mean([r["is_success"] for r in per_policy_results["history_gru"][cond]]))

        # Rank: 1 = better, 2 = worse
        if gru_rate >= mlp_rate:
            ranks = {"history_gru": 1, "reactive_mlp": 2}
        else:
            ranks = {"history_gru": 2, "reactive_mlp": 1}

        ranking_analysis[cond] = {
            "mlp_recovery_rate": mlp_rate,
            "gru_recovery_rate": gru_rate,
            "ranks": ranks,
            "top_1": "history_gru" if gru_rate >= mlp_rate else "reactive_mlp",
            "advantage_gru_minus_mlp": gru_rate - mlp_rate,
        }

    # Kendall's tau between B0 ranking and B4 ranking
    # Since only 2 policies, top-1 agreement and rank reversal boolean
    b0_top1 = ranking_analysis["B0"]["top_1"]
    b4_top1 = ranking_analysis["B4"]["top_1"]
    ranking_reversal = bool(b0_top1 != b4_top1)

    ranking_summary = {
        "condition_rankings": ranking_analysis,
        "ranking_reversal_B0_vs_B4": ranking_reversal,
        "kendall_tau": 1.0 if not ranking_reversal else -1.0,
        "spearman_rho": 1.0 if not ranking_reversal else -1.0,
    }

    # 6. Overall Summary Metrics
    summary_metrics = {
        "metadata": {
            "title": "Phase 6 Pre-Registered Pilot Recovery Evaluation Summary",
            "disclaimer": "Pre-registered pilot analysis — exploratory, not confirmatory.",
            "total_rollouts": total_rollouts,
            "policies": policy_ids,
            "conditions": conditions,
            "eval_seeds": eval_seeds,
            "scenario_count": len(scenario_uids),
        },
        "overall_success_rates": {
            pol_id: {cond: float(np.mean([r["is_success"] for r in per_policy_results[pol_id][cond]])) for cond in conditions}
            for pol_id in policy_ids
        },
        "mean_final_goal_distance_m": {
            pol_id: {cond: float(np.mean([r["final_dist_to_goal"] for r in per_policy_results[pol_id][cond]])) for cond in conditions}
            for pol_id in policy_ids
        },
        "mean_control_effort": {
            pol_id: {cond: float(np.mean([r["control_effort"] for r in per_policy_results[pol_id][cond]])) for cond in conditions}
            for pol_id in policy_ids
        },
        "safety_rate": {
            pol_id: {cond: float(np.mean([r["is_safe"] for r in per_policy_results[pol_id][cond]])) for cond in conditions}
            for pol_id in policy_ids
        },
    }

    # 7. Save JSON reports
    with open(os.path.join(out_dir, "evaluation_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary_metrics, f, indent=2, default=_json_default)

    with open(os.path.join(out_dir, "paired_comparisons.json"), "w", encoding="utf-8") as f:
        json.dump(paired_analysis, f, indent=2, default=_json_default)

    with open(os.path.join(out_dir, "history_dependence_report.json"), "w", encoding="utf-8") as f:
        json.dump(history_dep, f, indent=2, default=_json_default)

    with open(os.path.join(out_dir, "policy_ranking_report.json"), "w", encoding="utf-8") as f:
        json.dump(ranking_summary, f, indent=2, default=_json_default)

    # Save detailed JSONL
    with open(os.path.join(out_dir, "detailed_records.jsonl"), "w", encoding="utf-8") as f:
        for r in rollout_records:
            f.write(json.dumps(r, default=_json_default) + "\n")

    print("\n" + "=" * 75)
    print("PHASE 6 PILOT RECOVERY EXPERIMENT SUMMARY (N = 1,140 Rollouts)")
    print("=" * 75)
    print(f"{'Policy':<14} | {'B0 (Full)':<10} | {'B1 (No Act)':<10} | {'B2 (No Obs)':<10} | {'B3 (Reset h)':<11} | {'B4 (Zero)':<10}")
    print("-" * 75)
    for pol_id in policy_ids:
        rates = summary_metrics["overall_success_rates"][pol_id]
        print(f"{pol_id:<14} | {rates['B0']*100:<9.1f}% | {rates['B1']*100:<9.1f}% | {rates['B2']*100:<9.1f}% | {rates['B3']*100:<10.1f}% | {rates['B4']*100:<9.1f}%")
    print("=" * 75)
    print("Paired Difference H_R (B0 - B4):")
    for pol_id in policy_ids:
        b0_b4 = paired_analysis[pol_id]["B0_vs_B4"]
        print(f" - {pol_id:<14}: H_R = {b0_b4['paired_difference_H_R']:+.4f} (95% CI: [{b0_b4['bootstrap_95_ci'][0]:+.4f}, {b0_b4['bootstrap_95_ci'][1]:+.4f}], p={b0_b4['holm_bonferroni_p_value']:.4f})")
    print("=" * 75)

    return summary_metrics


if __name__ == "__main__":
    run_phase_6_evaluation()

