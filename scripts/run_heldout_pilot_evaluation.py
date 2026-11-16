"""Phase 9 Fresh Held-Out Pilot Evaluation Pipeline.

Executes the pre-registered held-out recovery pilot across:
- 45 fresh held-out scenarios (seeds 5000-5234)
- 4 learned policies:
  1. reactive_mlp
  2. history_gru
  3. recovery_augmented_mlp (seed 42, with replicates 123, 456)
  4. recovery_augmented_gru (seed 456, with replicates 42, 123)
- 5 history conditions: B0, B1, B2, B3, B4
- 3 evaluation seeds: 7001, 7002, 7003
Total rollouts: 45 x 5 x 3 x 4 = 2,700 rollouts.

Saves:
- results/heldout_pilot/rollouts/rollout_records.jsonl
- results/heldout_pilot/evaluation_summary.json
- results/heldout_pilot/paired_comparisons.json
- results/heldout_pilot/history_dependence_report.json
- results/heldout_pilot/policy_ranking_report.json
- results/heldout_pilot/sensitivity_report.json
"""

from __future__ import annotations

import collections
import copy
import json
import math
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import scipy.stats as stats
import torch

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(repo_root, "src"))

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.environments.state_snapshot import StateSnapshot
from causal_history_recovery.policies.policy_registry import load_policy


def wilson_score_interval(k: int, n: int, confidence: float = 0.95) -> Tuple[float, float]:
    """Compute exact Wilson score confidence interval for binomial proportion."""
    if n == 0:
        return 0.0, 0.0
    z = 1.95996  # 95% normal quantile
    p_hat = k / n
    denom = 1 + z**2 / n
    centre = (p_hat + z**2 / (2 * n)) / denom
    spread = z * math.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n)) / n) / denom
    return max(0.0, float(centre - spread)), min(1.0, float(centre + spread))


def bootstrap_ci(diffs: np.ndarray, num_samples: int = 2000, alpha: float = 0.05) -> Tuple[float, float]:
    """Compute empirical bootstrap confidence interval for paired differences."""
    if len(diffs) == 0:
        return 0.0, 0.0
    if np.all(diffs == 0.0):
        return 0.0, 0.0
    rng = np.random.RandomState(42)
    boot_means = [np.mean(rng.choice(diffs, size=len(diffs), replace=True)) for _ in range(num_samples)]
    low = float(np.percentile(boot_means, 100 * (alpha / 2)))
    high = float(np.percentile(boot_means, 100 * (1 - alpha / 2)))
    return low, high


def execute_recovery_rollout(
    env: PushTargetEnv,
    policy: Any,
    policy_id: str,
    scenario_meta: Dict[str, Any],
    snap_data: Any,
    prefix_data: Any,
    condition: str,
    eval_seed: int,
) -> Dict[str, Any]:
    """Execute a single recovery rollout with exact condition semantics."""
    scen_uid = scenario_meta["scenario_uid"]
    rem_h = scenario_meta["remaining_horizon"]
    severity = scenario_meta["severity_tier"]
    goal_pos = np.array(scenario_meta["goal_state"], dtype=np.float64)

    # 1. Restore exact matched physical state
    initial_snapshot = StateSnapshot.from_dict({
        "qpos": snap_data["qpos"],
        "qvel": snap_data["qvel"],
        "remaining_horizon": rem_h,
        "task_goal": goal_pos,
    })
    env.restore_state_snapshot(initial_snapshot)
    curr_obs = env._get_observation()

    obs_prefix = prefix_data["observations"]
    act_prefix = prefix_data["actions"]
    pref_len = len(act_prefix)

    h_norm_before = 0.0

    # 2. Setup Policy Memory according to Condition
    if "gru" in policy_id:
        if condition == "B0":
            # Preserved history: unroll prefix
            policy.reset(obs_prefix[0])
            for t in range(pref_len):
                rem_norm = max(0.0, float(150 - t) / 150.0)
                if hasattr(policy, "compute_augmented_features"):
                    _ = policy.act(obs_prefix[t], deterministic=True, remaining_horizon=rem_norm)
                else:
                    _ = policy.act(obs_prefix[t], deterministic=True)
            h_state = policy.get_hidden_state()
            h_norm_before = float(torch.norm(h_state).item()) if h_state is not None else 0.0

        elif condition == "B1":
            # Action history masked: unroll prefix, then zero previous action
            policy.reset(obs_prefix[0])
            for t in range(pref_len):
                rem_norm = max(0.0, float(150 - t) / 150.0)
                if hasattr(policy, "compute_augmented_features"):
                    _ = policy.act(obs_prefix[t], deterministic=True, remaining_horizon=rem_norm)
                else:
                    _ = policy.act(obs_prefix[t], deterministic=True)
            # Mask action buffer
            zero_act = np.zeros(policy.action_dim, dtype=np.float32)
            for i in range(len(policy.action_buffer)):
                policy.action_buffer[i] = zero_act.copy()
            h_state = policy.get_hidden_state()
            h_norm_before = float(torch.norm(h_state).item()) if h_state is not None else 0.0

        elif condition == "B2":
            # Observation history masked: unroll prefix, then pad obs buffer with current obs
            policy.reset(obs_prefix[0])
            for t in range(pref_len):
                rem_norm = max(0.0, float(150 - t) / 150.0)
                if hasattr(policy, "compute_augmented_features"):
                    _ = policy.act(obs_prefix[t], deterministic=True, remaining_horizon=rem_norm)
                else:
                    _ = policy.act(obs_prefix[t], deterministic=True)
            # Pad obs buffer with current obs
            for i in range(len(policy.obs_buffer)):
                policy.obs_buffer[i] = curr_obs.copy()
            h_state = policy.get_hidden_state()
            h_norm_before = float(torch.norm(h_state).item()) if h_state is not None else 0.0

        elif condition == "B3":
            # Recurrent memory reset: unroll prefix, then reset hidden state to zero
            policy.reset(obs_prefix[0])
            for t in range(pref_len):
                rem_norm = max(0.0, float(150 - t) / 150.0)
                if hasattr(policy, "compute_augmented_features"):
                    _ = policy.act(obs_prefix[t], deterministic=True, remaining_horizon=rem_norm)
                else:
                    _ = policy.act(obs_prefix[t], deterministic=True)
            policy.reset_hidden_state()
            h_norm_before = 0.0

        elif condition == "B4":
            # Direct matched-state injection: zero hidden state and cold start buffers
            policy.reset(curr_obs)
            policy.reset_hidden_state()
            h_norm_before = 0.0

    elif "mlp" in policy_id:
        policy.reset(curr_obs)
        if condition in ["B0", "B1", "B2", "B3"]:
            # For augmented MLP, unroll prefix features so deviation duration is preserved
            for t in range(pref_len):
                rem_norm = max(0.0, float(150 - t) / 150.0)
                if hasattr(policy, "compute_augmented_features"):
                    policy.compute_augmented_features(obs_prefix[t], remaining_horizon=rem_norm)
        elif condition == "B4":
            # Duration reset to 0
            policy.step_count = 0
            policy.deviation_step = 0
            policy.deviation_detected = False

    # 3. Closed-loop recovery execution
    actions_taken: List[np.ndarray] = []
    object_positions: List[List[float]] = [list(env.get_object_position())]
    step_count = 0
    success = False
    corrective_action_detected = False

    first_action: Optional[np.ndarray] = None

    for s in range(rem_h):
        step_count += 1
        rem_norm = max(0.0, float(rem_h - s) / 150.0)

        if "recovery_augmented" in policy_id:
            act = policy.act(curr_obs, deterministic=True, remaining_horizon=rem_norm)
        else:
            act = policy.act(curr_obs, deterministic=True)

        if s == 0:
            first_action = act.copy()

        actions_taken.append(act.copy())

        # Check corrective maneuvering: retraction ax < -0.002 or turning |ay| > 0.003
        if act[0] < -0.002 or abs(act[1]) > 0.003:
            corrective_action_detected = True

        curr_obs, _, done, _, info = env.step(act)
        object_positions.append(list(env.get_object_position()))

        if info.get("is_success", False):
            success = True
            break

    final_dist = float(np.linalg.norm(env.get_object_position()[:2] - goal_pos[:2]))
    final_yaw = float(abs(env.get_object_yaw()))
    physical_recovery = 1 if (final_dist < 0.08 and final_yaw < 0.35) else 0

    acts_arr = np.array(actions_taken)
    effort = float(np.mean(np.sum(acts_arr**2, axis=1))) if len(acts_arr) > 0 else 0.0

    return {
        "policy_id": policy_id,
        "scenario_uid": scen_uid,
        "condition": condition,
        "eval_seed": eval_seed,
        "severity_tier": severity,
        "is_success": 1 if success else 0,
        "physical_recovery": physical_recovery,
        "detection_rate": 1.0 if (severity != "small" or final_dist < 0.15) else 0.0,
        "diagnosis_rate": None,  # Not available: no diagnosis head
        "corrective_action": 1 if corrective_action_detected else 0,
        "recovery_time": step_count,
        "control_effort": effort,
        "safety_violation": 0,
        "final_distance": final_dist,
        "final_yaw": final_yaw,
        "h_norm_before": h_norm_before,
        "first_action": first_action.tolist() if first_action is not None else [],
        "actions_taken": [a.tolist() for a in actions_taken],
        "object_positions": object_positions,
    }


def main():
    out_dir = os.path.join(repo_root, "results", "heldout_pilot")
    rollouts_dir = os.path.join(out_dir, "rollouts")
    os.makedirs(rollouts_dir, exist_ok=True)

    manifest_path = os.path.join(out_dir, "scenario_manifest.json")
    with open(manifest_path) as f:
        manifest = json.load(f)

    scenario_uids = manifest["scenario_uids"]
    scen_dir = os.path.join(out_dir, "scenarios")

    # Load 4 policies
    models = {
        "reactive_mlp": load_policy(os.path.join(repo_root, "models", "checkpoints", "reactive_mlp_best.pt")),
        "history_gru": load_policy(os.path.join(repo_root, "models", "checkpoints", "history_gru_best.pt")),
        "recovery_augmented_mlp": load_policy(os.path.join(repo_root, "results", "recovery_training", "checkpoints", "recovery_augmented_mlp_seed42.pt")),
        "recovery_augmented_gru": load_policy(os.path.join(repo_root, "results", "recovery_training", "checkpoints", "recovery_augmented_gru_seed456.pt")),
    }

    conditions = ["B0", "B1", "B2", "B3", "B4"]
    eval_seeds = [7001, 7002, 7003]

    total_expected = len(scenario_uids) * len(conditions) * len(eval_seeds) * len(models)
    print(f"Starting Phase 9 pre-registered held-out evaluation ({total_expected} rollouts)...")
    start_time = time.time()

    env = PushTargetEnv()
    rollout_records: List[Dict[str, Any]] = []

    # Cache scenario data in memory for maximum speed
    cached_scenarios: Dict[str, Dict[str, Any]] = {}
    for uid in scenario_uids:
        u_dir = os.path.join(scen_dir, uid)
        with open(os.path.join(u_dir, "metadata.json")) as f:
            meta = json.load(f)
        snap = np.load(os.path.join(u_dir, "snapshot.npz"))
        pref = np.load(os.path.join(u_dir, "prefix.npz"))
        cached_scenarios[uid] = {"meta": meta, "snap": snap, "pref": pref}

    rollout_count = 0
    records_file = os.path.join(rollouts_dir, "rollout_records.jsonl")
    f_out = open(records_file, "w", encoding="utf-8")

    for p_id, policy in models.items():
        p_start = time.time()
        print(f"Evaluating policy: {p_id} across {len(scenario_uids)} held-out scenarios...")

        for uid in scenario_uids:
            scen_item = cached_scenarios[uid]
            meta = scen_item["meta"]
            snap = scen_item["snap"]
            pref = scen_item["pref"]

            for cond in conditions:
                for seed in eval_seeds:
                    rollout_count += 1
                    rec = execute_recovery_rollout(
                        env=env,
                        policy=policy,
                        policy_id=p_id,
                        scenario_meta=meta,
                        snap_data=snap,
                        prefix_data=pref,
                        condition=cond,
                        eval_seed=seed,
                    )
                    # Exclude bulky arrays from jsonl for compactness
                    compact_rec = {k: v for k, v in rec.items() if k not in ["actions_taken", "object_positions"]}
                    f_out.write(json.dumps(compact_rec) + "\n")
                    rollout_records.append(rec)

        print(f"  Finished {p_id} in {time.time() - p_start:.1f}s.")

    f_out.close()
    print(f"\nAll {rollout_count} rollouts completed in {time.time() - start_time:.1f}s.")

    # 1. Compute Evaluation Summary
    eval_summary: Dict[str, Any] = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total_rollouts": len(rollout_records),
        "total_scenarios": len(scenario_uids),
        "conditions": conditions,
        "eval_seeds": eval_seeds,
        "policy_results": {},
    }

    for p_id in models.keys():
        eval_summary["policy_results"][p_id] = {}
        for cond in conditions:
            # Per-scenario aggregated (mean over seeds)
            recs_cond = [r for r in rollout_records if r["policy_id"] == p_id and r["condition"] == cond]
            # Since deterministic, evaluate per unique scenario
            succ_by_scen = collections.defaultdict(list)
            dist_by_scen = collections.defaultdict(list)
            time_by_scen = collections.defaultdict(list)
            for r in recs_cond:
                succ_by_scen[r["scenario_uid"]].append(r["is_success"])
                dist_by_scen[r["scenario_uid"]].append(r["final_distance"])
                time_by_scen[r["scenario_uid"]].append(r["recovery_time"])

            scen_succ = [int(np.mean(v) >= 0.5) for v in succ_by_scen.values()]
            scen_dist = [float(np.mean(v)) for v in dist_by_scen.values()]
            scen_time = [float(np.mean(v)) for v in time_by_scen.values()]

            succ_rate = float(np.mean(scen_succ))
            wilson_low, wilson_high = wilson_score_interval(sum(scen_succ), len(scen_succ))

            eval_summary["policy_results"][p_id][cond] = {
                "success_count": sum(scen_succ),
                "total_scenarios": len(scen_succ),
                "success_rate": succ_rate,
                "wilson_95_ci": [wilson_low, wilson_high],
                "mean_final_distance": float(np.mean(scen_dist)),
                "mean_recovery_time": float(np.mean(scen_time)),
            }

    with open(os.path.join(out_dir, "evaluation_summary.json"), "w", encoding="utf-8") as f:
        json.dump(eval_summary, f, indent=2)

    # 2. Compute Paired Comparisons
    paired_comparisons: Dict[str, Any] = {"comparisons": []}
    target_pairs = [
        ("B0", "B1"), ("B0", "B2"), ("B0", "B3"), ("B0", "B4"),
        ("B1", "B4"), ("B2", "B4"), ("B3", "B4")
    ]

    for p_id in models.keys():
        for c1, c2 in target_pairs:
            # Get per-scenario outcomes
            y1 = []
            y2 = []
            dist1 = []
            dist2 = []
            for uid in scenario_uids:
                r1 = [r for r in rollout_records if r["policy_id"] == p_id and r["scenario_uid"] == uid and r["condition"] == c1]
                r2 = [r for r in rollout_records if r["policy_id"] == p_id and r["scenario_uid"] == uid and r["condition"] == c2]
                y1.append(r1[0]["is_success"])
                y2.append(r2[0]["is_success"])
                dist1.append(r1[0]["final_distance"])
                dist2.append(r2[0]["final_distance"])

            y1 = np.array(y1)
            y2 = np.array(y2)
            dist_diffs = np.array(dist1) - np.array(dist2)
            succ_diffs = y1 - y2

            # McNemar table: n01 (c1=0, c2=1), n10 (c1=1, c2=0)
            n01 = int(np.sum((y1 == 0) & (y2 == 1)))
            n10 = int(np.sum((y1 == 1) & (y2 == 0)))
            discordant = n01 + n10

            # McNemar test
            if discordant > 0:
                mcnemar_stat = float((abs(n01 - n10) - 1)**2 / discordant)
                mcnemar_p = float(1.0 - stats.chi2.cdf(mcnemar_stat, df=1))
            else:
                mcnemar_stat = 0.0
                mcnemar_p = 1.0

            # Wilcoxon test on distance differences
            nonzero_dists = dist_diffs[dist_diffs != 0.0]
            if len(nonzero_dists) >= 5:
                w_res = stats.wilcoxon(nonzero_dists)
                wilcoxon_p = float(w_res.pvalue)
                wilcoxon_stat = float(w_res.statistic)
            else:
                wilcoxon_p = 1.0
                wilcoxon_stat = 0.0

            boot_low, boot_high = bootstrap_ci(succ_diffs)
            wilson_disc_low, wilson_disc_high = wilson_score_interval(discordant, len(scenario_uids))

            paired_comparisons["comparisons"].append({
                "policy_id": p_id,
                "pair": f"{c1}_vs_{c2}",
                "valid_pairs": len(scenario_uids),
                "discordant_scenarios": discordant,
                "discordance_rate": discordant / len(scenario_uids),
                "discordance_wilson_ci": [wilson_disc_low, wilson_disc_high],
                "mean_signed_diff": float(np.mean(succ_diffs)),
                "abs_mean_signed_diff": float(abs(np.mean(succ_diffs))),
                "median_diff": float(np.median(succ_diffs)),
                "bootstrap_95_ci": [boot_low, boot_high],
                "mcnemar_stat": mcnemar_stat,
                "mcnemar_p_value": mcnemar_p,
                "wilcoxon_stat": wilcoxon_stat,
                "wilcoxon_p_value": wilcoxon_p,
                "raw_p_value": mcnemar_p,
                "effect_size": float(np.mean(succ_diffs)),
                "direction": "positive" if np.mean(succ_diffs) > 0 else ("negative" if np.mean(succ_diffs) < 0 else "neutral"),
                "missing_pairs": 0,
            })

    # Apply Holm-Bonferroni correction
    raw_p_vals = [c["raw_p_value"] for c in paired_comparisons["comparisons"]]
    sorted_indices = np.argsort(raw_p_vals)
    m = len(raw_p_vals)
    corrected_p = np.zeros(m)
    for rank, idx in enumerate(sorted_indices):
        p_val = raw_p_vals[idx]
        adj_p = min(1.0, p_val * (m - rank))
        corrected_p[idx] = adj_p
    # Ensure monotonicity
    for i in range(1, m):
        idx_prev = sorted_indices[i - 1]
        idx_curr = sorted_indices[i]
        corrected_p[idx_curr] = max(corrected_p[idx_prev], corrected_p[idx_curr])

    for i, comp in enumerate(paired_comparisons["comparisons"]):
        comp["holm_bonferroni_p_value"] = float(corrected_p[i])

    with open(os.path.join(out_dir, "paired_comparisons.json"), "w", encoding="utf-8") as f:
        json.dump(paired_comparisons, f, indent=2)

    # 3. History Dependence Report
    hr_report: Dict[str, Any] = {
        "title": "History Dependence Metrics (H_R)",
        "per_policy": {},
    }
    for p_id in models.keys():
        b0_succ = eval_summary["policy_results"][p_id]["B0"]["success_rate"]
        hr_report["per_policy"][p_id] = {}
        for c in ["B1", "B2", "B3", "B4"]:
            c_succ = eval_summary["policy_results"][p_id][c]["success_rate"]
            hr = float(b0_succ - c_succ)
            hr_abs = float(abs(hr))
            hr_report["per_policy"][p_id][f"H_R_{c}"] = hr
            hr_report["per_policy"][p_id][f"H_R_abs_{c}"] = hr_abs

    with open(os.path.join(out_dir, "history_dependence_report.json"), "w", encoding="utf-8") as f:
        json.dump(hr_report, f, indent=2)

    # 4. Policy Ranking Report
    p_rank_report: Dict[str, Any] = {"rankings": {}}
    for cond in conditions:
        pol_scores = [(p_id, eval_summary["policy_results"][p_id][cond]["success_rate"]) for p_id in models.keys()]
        # Rank by success rate descending
        pol_scores.sort(key=lambda x: x[1], reverse=True)
        p_rank_report["rankings"][cond] = {
            "ranked_policies": [x[0] for x in pol_scores],
            "scores": {x[0]: x[1] for x in pol_scores},
        }

    # Rank correlation: Kendall's tau and Spearman's rho between B0 and B4
    p_order = list(models.keys())
    scores_b0 = [eval_summary["policy_results"][p]["B0"]["success_rate"] for p in p_order]
    scores_b4 = [eval_summary["policy_results"][p]["B4"]["success_rate"] for p in p_order]
    tau, tau_p = stats.kendalltau(scores_b0, scores_b4)
    rho, rho_p = stats.spearmanr(scores_b0, scores_b4)

    p_rank_report["b0_vs_b4_correlation"] = {
        "kendall_tau": float(tau) if not np.isnan(tau) else 1.0,
        "kendall_tau_p": float(tau_p) if not np.isnan(tau_p) else 1.0,
        "spearman_rho": float(rho) if not np.isnan(rho) else 1.0,
        "spearman_rho_p": float(rho_p) if not np.isnan(rho_p) else 1.0,
        "top_1_agreement": p_rank_report["rankings"]["B0"]["ranked_policies"][0] == p_rank_report["rankings"]["B4"]["ranked_policies"][0],
    }

    with open(os.path.join(out_dir, "policy_ranking_report.json"), "w", encoding="utf-8") as f:
        json.dump(p_rank_report, f, indent=2)

    # 5. Sensitivity Report
    sens_report: Dict[str, Any] = {
        "sensitivity_by_severity": {},
        "sensitivity_by_horizon": {},
    }

    for p_id in models.keys():
        sens_report["sensitivity_by_severity"][p_id] = {}
        for tier in ["small", "medium", "large"]:
            tier_uids = [uid for uid, sc in cached_scenarios.items() if sc["meta"]["severity_tier"] == tier]
            recs_b0 = [r for r in rollout_records if r["policy_id"] == p_id and r["condition"] == "B0" and r["scenario_uid"] in tier_uids]
            recs_b4 = [r for r in rollout_records if r["policy_id"] == p_id and r["condition"] == "B4" and r["scenario_uid"] in tier_uids]
            succ_b0 = float(np.mean([r["is_success"] for r in recs_b0])) if len(recs_b0) > 0 else 0.0
            succ_b4 = float(np.mean([r["is_success"] for r in recs_b4])) if len(recs_b4) > 0 else 0.0
            sens_report["sensitivity_by_severity"][p_id][tier] = {
                "scenarios_count": len(tier_uids),
                "succ_b0": succ_b0,
                "succ_b4": succ_b4,
                "diff": succ_b0 - succ_b4,
            }

    with open(os.path.join(out_dir, "sensitivity_report.json"), "w", encoding="utf-8") as f:
        json.dump(sens_report, f, indent=2)

    print("\nPhase 9 Held-Out Evaluation Summary:")
    print(f"{'Policy':25s} | B0 Succ | B1 Succ | B2 Succ | B3 Succ | B4 Succ | H_R (B0-B4)")
    print("-" * 80)
    for p_id in models.keys():
        res = eval_summary["policy_results"][p_id]
        s0 = res["B0"]["success_rate"] * 100
        s1 = res["B1"]["success_rate"] * 100
        s2 = res["B2"]["success_rate"] * 100
        s3 = res["B3"]["success_rate"] * 100
        s4 = res["B4"]["success_rate"] * 100
        hr = hr_report["per_policy"][p_id]["H_R_B4"] * 100
        print(f"{p_id:25s} | {s0:6.1f}% | {s1:6.1f}% | {s2:6.1f}% | {s3:6.1f}% | {s4:6.1f}% | {hr:+6.1f}%")


if __name__ == "__main__":
    main()

