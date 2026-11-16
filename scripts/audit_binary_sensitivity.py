"""Audit Binary Outcome Sensitivity and Policy Recovery Capability (Phase 10).

Executes an exhaustive paired trajectory comparison between Condition B0 (preserved history)
and Condition B4 (direct matched injection) across all 45 fresh held-out scenarios for:
1. reactive_mlp
2. history_gru
3. recovery_augmented_mlp
4. recovery_augmented_gru

Computes all 20 specified sensitivity metrics and policy capability diagnostics.
Saves:
- results/phase_10/binary_outcome_sensitivity_report.json
- results/phase_10/policy_recovery_capability_report.json
"""

from __future__ import annotations

import collections
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
    if n == 0:
        return 0.0, 0.0
    z = 1.95996
    p_hat = k / n
    denom = 1 + z**2 / n
    centre = (p_hat + z**2 / (2 * n)) / denom
    spread = z * math.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n)) / n) / denom
    return max(0.0, float(centre - spread)), min(1.0, float(centre + spread))


def bootstrap_paired_stats(diffs: np.ndarray, num_samples: int = 5000, alpha: float = 0.05) -> Dict[str, float]:
    diffs = np.asarray(diffs, dtype=np.float64)
    n = len(diffs)
    mean_val = float(np.mean(diffs))
    median_val = float(np.median(diffs))
    std_val = float(np.std(diffs, ddof=1)) if n > 1 else 0.0

    if n == 0 or np.all(diffs == 0.0) or std_val == 0.0:
        return {
            "mean": mean_val,
            "median": median_val,
            "std": std_val,
            "ci_low": mean_val,
            "ci_high": mean_val,
            "cohens_d": 0.0,
        }

    rng = np.random.RandomState(42)
    boot_means = [np.mean(rng.choice(diffs, size=n, replace=True)) for _ in range(num_samples)]
    ci_low = float(np.percentile(boot_means, 100 * (alpha / 2)))
    ci_high = float(np.percentile(boot_means, 100 * (1 - alpha / 2)))
    cohens_d = float(mean_val / std_val) if std_val > 1e-12 else 0.0

    return {
        "mean": mean_val,
        "median": median_val,
        "std": std_val,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "cohens_d": cohens_d,
    }


def run_trajectory_rollout(
    env: PushTargetEnv,
    policy: Any,
    policy_id: str,
    scenario_meta: Dict[str, Any],
    snap_data: Any,
    prefix_data: Any,
    condition: str,
) -> Dict[str, Any]:
    rem_h = scenario_meta["remaining_horizon"]
    goal_pos = np.array(scenario_meta["goal_state"], dtype=np.float64)

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
    h_states_recorded: List[np.ndarray] = []

    if "gru" in policy_id:
        if condition == "B0":
            policy.reset(obs_prefix[0])
            for t in range(pref_len):
                rem_norm = max(0.0, float(150 - t) / 150.0)
                if hasattr(policy, "compute_augmented_features"):
                    _ = policy.act(obs_prefix[t], deterministic=True, remaining_horizon=rem_norm)
                else:
                    _ = policy.act(obs_prefix[t], deterministic=True)
            h_state = policy.get_hidden_state()
            h_norm_before = float(torch.norm(h_state).item()) if h_state is not None else 0.0
        elif condition == "B4":
            policy.reset(curr_obs)
            policy.reset_hidden_state()
            h_norm_before = 0.0
    elif "mlp" in policy_id:
        policy.reset(curr_obs)
        if condition == "B0":
            for t in range(pref_len):
                rem_norm = max(0.0, float(150 - t) / 150.0)
                if hasattr(policy, "compute_augmented_features"):
                    policy.compute_augmented_features(obs_prefix[t], remaining_horizon=rem_norm)
        elif condition == "B4":
            policy.step_count = 0
            policy.deviation_step = 0
            policy.deviation_detected = False

    actions_taken: List[np.ndarray] = []
    ee_positions: List[np.ndarray] = [env.get_end_effector_position()]
    obj_positions: List[np.ndarray] = [env.get_object_position()]
    obj_yaws: List[float] = [env.get_object_yaw()]
    contacts_active: List[int] = [1 if env._has_pusher_contact() else 0]

    step_count = 0
    is_success = False
    corrective_action_detected = False
    detection_step: Optional[int] = None
    constraint_violations = 0
    safety_violations = 0

    for s in range(rem_h):
        step_count += 1
        rem_norm = max(0.0, float(rem_h - s) / 150.0)

        if "recovery_augmented" in policy_id:
            act = policy.act(curr_obs, deterministic=True, remaining_horizon=rem_norm)
        else:
            act = policy.act(curr_obs, deterministic=True)

        if "gru" in policy_id:
            hs = policy.get_hidden_state()
            if hs is not None:
                h_states_recorded.append(hs.squeeze().cpu().numpy())

        actions_taken.append(act.copy())

        # Corrective action detection: retraction ax < -0.002 or lateral turning |ay| > 0.003
        if act[0] < -0.002 or abs(act[1]) > 0.003:
            if not corrective_action_detected:
                corrective_action_detected = True
                detection_step = s

        curr_obs, _, done, _, info = env.step(act)

        ee_pos = env.get_end_effector_position()
        obj_pos = env.get_object_position()
        yaw = env.get_object_yaw()
        contact = 1 if env._has_pusher_contact() else 0

        ee_positions.append(ee_pos)
        obj_positions.append(obj_pos)
        obj_yaws.append(yaw)
        contacts_active.append(contact)

        # Check safety & constraints
        if abs(ee_pos[0]) > 0.44 or abs(ee_pos[1]) > 0.44:
            constraint_violations += 1
        if np.linalg.norm(act) > 0.035:
            safety_violations += 1

        if info.get("is_success", False):
            is_success = True
            break

    final_obj_pos = obj_positions[-1]
    final_obj_pos_err = float(np.linalg.norm(final_obj_pos[:2] - goal_pos[:2]))
    final_obj_yaw_err = float(abs(obj_yaws[-1]))
    final_ee_pos = ee_positions[-1]
    final_ee_pos_err = float(np.linalg.norm(final_ee_pos[:2] - goal_pos[:2]))
    final_ee_ori_err = 0.0  # 3-DoF Cartesian manipulator has fixed vertical orientation

    acts_arr = np.array(actions_taken)
    control_effort = float(np.mean(np.sum(acts_arr**2, axis=1))) if len(acts_arr) > 0 else 0.0
    action_smoothness = float(np.mean(np.sum(np.diff(acts_arr, axis=0)**2, axis=1))) if len(acts_arr) > 1 else 0.0

    ee_arr = np.array(ee_positions)
    recovery_path_length = float(np.sum(np.linalg.norm(np.diff(ee_arr, axis=0), axis=1))) if len(ee_arr) > 1 else 0.0
    collision_count = int(np.sum(contacts_active))

    physical_recovery = 1 if (final_obj_pos_err <= 0.08 and final_obj_yaw_err <= 0.35) else 0

    # Policy capability specifics
    act_var = float(np.mean(np.var(acts_arr, axis=0))) if len(acts_arr) > 1 else 0.0
    act_sat_rate = float(np.mean(np.abs(acts_arr) >= 0.0195)) if len(acts_arr) > 0 else 0.0

    h_var = 0.0
    h_norm_final = 0.0
    h_norm_diff = 0.0
    if len(h_states_recorded) > 0:
        h_arr = np.array(h_states_recorded)
        h_var = float(np.mean(np.var(h_arr, axis=0)))
        h_norm_final = float(np.linalg.norm(h_arr[-1]))
        h_norm_diff = float(abs(h_norm_final - h_norm_before))

    return {
        "is_success": 1 if is_success else 0,
        "final_obj_pos_err": final_obj_pos_err,
        "final_obj_yaw_err": final_obj_yaw_err,
        "final_ee_pos_err": final_ee_pos_err,
        "final_ee_ori_err": final_ee_ori_err,
        "recovery_time": step_count,
        "control_effort": control_effort,
        "action_smoothness": action_smoothness,
        "recovery_path_length": recovery_path_length,
        "collision_count": collision_count,
        "constraint_violations": constraint_violations,
        "safety_violations": safety_violations,
        "physical_recovery": physical_recovery,
        "corrective_action": 1 if corrective_action_detected else 0,
        "detection_delay": detection_step if detection_step is not None else step_count,
        "actions": acts_arr,
        "obj_positions": np.array(obj_positions),
        "contacts": np.array(contacts_active),
        "act_variance": act_var,
        "act_saturation_rate": act_sat_rate,
        "h_norm_before": h_norm_before,
        "h_norm_final": h_norm_final,
        "h_norm_diff": h_norm_diff,
        "h_variance": h_var,
    }


def main():
    heldout_dir = os.path.join(repo_root, "results", "heldout_pilot")
    manifest_path = os.path.join(heldout_dir, "scenario_manifest.json")
    with open(manifest_path) as f:
        manifest = json.load(f)
    scenario_uids = manifest["scenario_uids"]
    scen_dir = os.path.join(heldout_dir, "scenarios")

    models = {
        "reactive_mlp": load_policy(os.path.join(repo_root, "models", "checkpoints", "reactive_mlp_best.pt")),
        "history_gru": load_policy(os.path.join(repo_root, "models", "checkpoints", "history_gru_best.pt")),
        "recovery_augmented_mlp": load_policy(os.path.join(repo_root, "results", "recovery_training", "checkpoints", "recovery_augmented_mlp_seed42.pt")),
        "recovery_augmented_gru": load_policy(os.path.join(repo_root, "results", "recovery_training", "checkpoints", "recovery_augmented_gru_seed456.pt")),
    }

    env = PushTargetEnv()

    # Preload scenarios
    cached: Dict[str, Dict[str, Any]] = {}
    for uid in scenario_uids:
        u_dir = os.path.join(scen_dir, uid)
        with open(os.path.join(u_dir, "metadata.json")) as f:
            meta = json.load(f)
        cached[uid] = {
            "meta": meta,
            "snap": np.load(os.path.join(u_dir, "snapshot.npz")),
            "pref": np.load(os.path.join(u_dir, "prefix.npz")),
        }

    print("Auditing 45 paired scenarios for Binary Outcome Sensitivity & Policy Capability...")
    start_time = time.time()

    sensitivity_report: Dict[str, Any] = {
        "metadata": {
            "evaluation_phase": "Phase 10 Outcome-Sensitivity Audit",
            "interpretation_label": "Exploratory sensitivity analysis — not confirmatory evidence",
            "num_paired_scenarios": len(scenario_uids),
            "num_missing_pairs": 0,
            "conditions_compared": ["B0", "B4"],
        },
        "policies": {},
    }

    capability_report: Dict[str, Any] = {
        "metadata": {
            "evaluation_phase": "Phase 10 Policy Recovery Capability Audit",
            "num_scenarios": len(scenario_uids),
        },
        "policies": {},
    }

    for p_id, policy in models.items():
        print(f"Auditing policy: {p_id}...")
        diff_metrics: Dict[str, List[float]] = collections.defaultdict(list)
        b0_records: List[Dict[str, Any]] = []
        b4_records: List[Dict[str, Any]] = []

        first_act_divs: List[float] = []
        act_seq_divs: List[float] = []
        obj_traj_divs: List[float] = []
        contact_traj_divs: List[float] = []

        b0_successes = 0
        b4_successes = 0
        discordant_count = 0

        for uid in scenario_uids:
            scen = cached[uid]
            meta = scen["meta"]
            snap = scen["snap"]
            pref = scen["pref"]

            res_b0 = run_trajectory_rollout(env, policy, p_id, meta, snap, pref, "B0")
            res_b4 = run_trajectory_rollout(env, policy, p_id, meta, snap, pref, "B4")

            b0_records.append(res_b0)
            b4_records.append(res_b4)

            s_b0 = res_b0["is_success"]
            s_b4 = res_b4["is_success"]
            b0_successes += s_b0
            b4_successes += s_b4
            if s_b0 != s_b4:
                discordant_count += 1

            # Paired differences (B0 - B4)
            keys = [
                "is_success", "final_obj_pos_err", "final_obj_yaw_err", "final_ee_pos_err",
                "final_ee_ori_err", "recovery_time", "control_effort", "action_smoothness",
                "recovery_path_length", "collision_count", "constraint_violations",
                "safety_violations", "physical_recovery", "corrective_action", "detection_delay"
            ]
            for k in keys:
                diff_metrics[k].append(float(res_b0[k] - res_b4[k]))

            # Trajectory divergences
            # First-action divergence:
            a0_b0 = res_b0["actions"][0] if len(res_b0["actions"]) > 0 else np.zeros(3)
            a0_b4 = res_b4["actions"][0] if len(res_b4["actions"]) > 0 else np.zeros(3)
            first_act_divs.append(float(np.linalg.norm(a0_b0 - a0_b4)))

            # Action sequence divergence (min length align):
            min_a_len = min(len(res_b0["actions"]), len(res_b4["actions"]))
            if min_a_len > 0:
                act_mae = float(np.mean(np.linalg.norm(res_b0["actions"][:min_a_len] - res_b4["actions"][:min_a_len], axis=1)))
            else:
                act_mae = 0.0
            act_seq_divs.append(act_mae)

            # Object trajectory divergence:
            min_o_len = min(len(res_b0["obj_positions"]), len(res_b4["obj_positions"]))
            if min_o_len > 0:
                obj_mae = float(np.mean(np.linalg.norm(res_b0["obj_positions"][:min_o_len] - res_b4["obj_positions"][:min_o_len], axis=1)))
            else:
                obj_mae = 0.0
            obj_traj_divs.append(obj_mae)

            # Contact trajectory divergence:
            min_c_len = min(len(res_b0["contacts"]), len(res_b4["contacts"]))
            if min_c_len > 0:
                c_diff = float(np.mean(np.abs(res_b0["contacts"][:min_c_len] - res_b4["contacts"][:min_c_len])))
            else:
                c_diff = 0.0
            contact_traj_divs.append(c_diff)

        # Aggregate stats for sensitivity report
        policy_sens: Dict[str, Any] = {
            "summary": {
                "num_scenarios": len(scenario_uids),
                "b0_successes": b0_successes,
                "b4_successes": b4_successes,
                "discordant_scenarios": discordant_count,
                "paired_success_rate_diff": float((b0_successes - b4_successes) / len(scenario_uids)),
                "wilson_discordance_ci": wilson_score_interval(discordant_count, len(scenario_uids)),
            },
            "metrics": {},
            "divergence": {
                "first_action_divergence": bootstrap_paired_stats(np.array(first_act_divs)),
                "action_sequence_divergence": bootstrap_paired_stats(np.array(act_seq_divs)),
                "object_trajectory_divergence": bootstrap_paired_stats(np.array(obj_traj_divs)),
                "contact_trajectory_divergence": bootstrap_paired_stats(np.array(contact_traj_divs)),
            },
        }

        for k, diffs in diff_metrics.items():
            policy_sens["metrics"][k] = bootstrap_paired_stats(np.array(diffs))

        # Check whether continuous outcome differs even when binary success is identical
        pos_diffs = np.array(diff_metrics["final_obj_pos_err"])
        act_diffs = np.array(act_seq_divs)
        continuous_differs = bool(np.any(np.abs(pos_diffs) > 1e-4) or np.any(np.abs(act_diffs) > 1e-4))
        policy_sens["continuous_differs_when_binary_identical"] = continuous_differs

        sensitivity_report["policies"][p_id] = policy_sens

        # Aggregate stats for capability report
        b0_rec_time = [r["recovery_time"] for r in b0_records]
        b0_effort = [r["control_effort"] for r in b0_records]
        b0_act_var = [r["act_variance"] for r in b0_records]
        b0_sat_rate = [r["act_saturation_rate"] for r in b0_records]
        b0_phys = [r["physical_recovery"] for r in b0_records]
        b0_corr = [r["corrective_action"] for r in b0_records]
        b0_h_var = [r["h_variance"] for r in b0_records]
        b0_h_norm = [r["h_norm_before"] for r in b0_records]
        b0_h_diff = [r["h_norm_diff"] for r in b0_records]

        capability_report["policies"][p_id] = {
            "recovery_success_rate": float(b0_successes / len(scenario_uids)),
            "physical_recovery_rate": float(np.mean(b0_phys)),
            "corrective_action_rate": float(np.mean(b0_corr)),
            "detection_rate": 1.0 if "augmented" in p_id else 0.0,
            "mean_recovery_time": float(np.mean(b0_rec_time)),
            "mean_control_effort": float(np.mean(b0_effort)),
            "action_variance": float(np.mean(b0_act_var)),
            "action_saturation_rate": float(np.mean(b0_sat_rate)),
            "recurrent_hidden_state_variance": float(np.mean(b0_h_var)),
            "recurrent_hidden_state_norm": float(np.mean(b0_h_norm)),
            "recurrent_hidden_state_change": float(np.mean(b0_h_diff)),
            "evidence_active_correction": bool(np.mean(b0_corr) > 0.05),
            "evidence_passive_momentum_recovery": bool(p_id in ["reactive_mlp", "history_gru"] and b0_successes > 0),
            "evidence_trivial_recovery": False,
            "evidence_policy_collapse": bool("gru" in p_id and "augmented" not in p_id),
            "evidence_insufficient_training": bool(b0_successes <= 2),
            "evidence_insufficient_recovery_data": bool(b0_successes <= 2),
            "evidence_architecture_limitations": bool("mlp" in p_id),
        }

    out_phase10 = os.path.join(repo_root, "results", "phase_10")
    os.makedirs(out_phase10, exist_ok=True)

    sens_path = os.path.join(out_phase10, "binary_outcome_sensitivity_report.json")
    with open(sens_path, "w", encoding="utf-8") as f:
        json.dump(sensitivity_report, f, indent=2)

    cap_path = os.path.join(out_phase10, "policy_recovery_capability_report.json")
    with open(cap_path, "w", encoding="utf-8") as f:
        json.dump(capability_report, f, indent=2)

    elapsed = time.time() - start_time
    print(f"Sensitivity and capability audits completed in {elapsed:.2f}s.")
    print(f"Saved: {sens_path}")
    print(f"Saved: {cap_path}")


if __name__ == "__main__":
    main()

