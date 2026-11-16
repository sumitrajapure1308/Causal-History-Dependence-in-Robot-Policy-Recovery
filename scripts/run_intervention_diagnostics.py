"""Phase 8 Mechanism Diagnostics Pipeline.

Executes bounded mechanism diagnostics across the 20 frozen Phase 7 development scenarios:
- Evaluates 4 policies:
  1. recovery_augmented_gru_seed42
  2. recovery_augmented_gru_seed123
  3. recovery_augmented_gru_seed456
  4. recovery_augmented_mlp_seed42 (reference)
- Evaluates conditions:
  - B0: Reconstructed policy-specific memory via prefix unrolling
  - B4: Memory removed / direct matched-state injection
- Disentangles:
  1. Input tensor differences at t_dev
  2. Hidden-state norms and differences at t_dev
  3. First-action differences at t_dev
  4. Action-sequence trajectory differences
  5. Object position & yaw trajectory differences
  6. Final continuous errors and binary success
- Saves raw traces to results/intervention_diagnostics/diagnostic_traces.jsonl
- Saves summary metrics to results/intervention_diagnostics/diagnostic_summary.json
"""

from __future__ import annotations

import collections
import copy
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import torch

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(repo_root, "src"))

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.environments.state_snapshot import StateSnapshot
from causal_history_recovery.policies.policy_registry import load_policy


def extract_scenario_prefix(
    env: PushTargetEnv,
    ep_data: Dict[str, Any],
    nominal_policy: Any,
) -> Tuple[List[np.ndarray], List[np.ndarray], StateSnapshot]:
    """Replay environment to obtain exact sequence of observations and actions up to deviation step."""
    seed = ep_data["seed"]
    pert_step = ep_data["perturb_step"]
    impulse_dur = ep_data["impulse_duration"]
    eff_offset = ep_data["offset_y"] * ep_data["direction"]
    dev_step = ep_data["deviation_step"]

    env._target_pos = np.array(ep_data["target_pos"], dtype=np.float64)
    obs, _ = env.reset(seed=seed)
    nominal_policy.reset(obs)

    actions: List[np.ndarray] = []
    observations: List[np.ndarray] = [obs.copy()]

    for step in range(dev_step + 1):
        if pert_step <= step < pert_step + impulse_dur:
            act = np.array([0.0, eff_offset, 0.0], dtype=np.float32)
        else:
            act = nominal_policy.act(obs, deterministic=True)

        actions.append(act.copy())
        obs, _, _, _, _ = env.step(act)
        observations.append(obs.copy())

    snap_dev = env.get_state_snapshot()
    return observations, actions, snap_dev


def run_mechanism_diagnostic_rollout(
    env: PushTargetEnv,
    policy: Any,
    policy_id: str,
    scenario_uid: str,
    condition: str,
    initial_snapshot: StateSnapshot,
    obs_prefix: List[np.ndarray],
    act_prefix: List[np.ndarray],
    remaining_horizon: int,
) -> Dict[str, Any]:
    """Execute a single recovery rollout with strictly defined condition semantics."""
    env.restore_state_snapshot(initial_snapshot)
    current_obs = env._get_observation()

    h_norm_before = 0.0
    initial_token = None

    if "gru" in policy_id:
        if condition == "B0":
            # Step 1: Reconstruct policy-specific memory by unrolling recorded prefix
            policy.reset(obs_prefix[0])
            for t in range(len(act_prefix)):
                rem_h = max(0.0, (150.0 - t) / 150.0)
                _ = policy.act(obs_prefix[t], deterministic=True, remaining_horizon=rem_h)

            h_dev = policy.get_hidden_state()
            h_norm_before = float(torch.norm(h_dev).item()) if h_dev is not None else 0.0
        elif condition == "B4":
            # Direct matched-state injection: zero hidden state and zero buffers
            policy.reset(current_obs)
            policy.reset_hidden_state()
            h_norm_before = 0.0

    elif "mlp" in policy_id:
        policy.reset(current_obs)
        if condition == "B4":
            # For B4 on augmented MLP, elapsed deviation duration is reset to 0
            policy.step_count = 0
            policy.deviation_step = 0
            policy.deviation_detected = False

    # Execute recovery rollout
    actions_taken: List[np.ndarray] = []
    object_positions: List[List[float]] = [list(env.get_object_position())]
    object_yaws: List[float] = [float(env.get_object_yaw())]
    contacts: List[int] = []
    success = False
    step_count = 0

    first_action: Optional[np.ndarray] = None

    for s in range(remaining_horizon):
        step_count += 1
        rem_h_norm = max(0.0, float(remaining_horizon - s) / 150.0)

        if hasattr(policy, "compute_augmented_features"):
            aug_obs = policy.compute_augmented_features(current_obs, remaining_horizon=rem_h_norm)
            if s == 0:
                initial_token = aug_obs.copy()

        act = policy.act(current_obs, deterministic=True, remaining_horizon=rem_h_norm)
        if s == 0:
            first_action = act.copy()

        actions_taken.append(act.copy())
        current_obs, _, done, _, info = env.step(act)

        obj_pos = env.get_object_position()
        obj_yaw = env.get_object_yaw()
        object_positions.append(list(obj_pos))
        object_yaws.append(float(obj_yaw))

        has_contact = 1 if len(env.get_contacts()) > 0 else 0
        contacts.append(has_contact)

        if info.get("is_success", False):
            success = True
            break

    final_dist = float(np.linalg.norm(env.get_object_position()[:2] - env.get_task_goal()[:2]))
    final_yaw = float(abs(env.get_object_yaw()))

    return {
        "policy_id": policy_id,
        "scenario_uid": scenario_uid,
        "condition": condition,
        "h_norm_before": h_norm_before,
        "first_action": first_action.tolist() if first_action is not None else [],
        "initial_token": initial_token.tolist() if initial_token is not None else [],
        "actions_taken": [a.tolist() for a in actions_taken],
        "object_positions": object_positions,
        "object_yaws": object_yaws,
        "contacts": contacts,
        "final_distance": final_dist,
        "final_yaw": final_yaw,
        "is_success": 1 if success else 0,
        "step_count": step_count,
    }


def main():
    out_dir = os.path.join(repo_root, "results", "intervention_diagnostics")
    os.makedirs(out_dir, exist_ok=True)

    # 1. Load 20 frozen scenario UIDs
    manifest_path = os.path.join(repo_root, "results", "paired_scenarios", "scenario_manifest.json")
    with open(manifest_path) as f:
        manifest = json.load(f)
    frozen_uids = manifest["scenario_uids"][:20]
    print(f"Loaded {len(frozen_uids)} frozen development scenarios.")

    # 2. Load episode metadata for exact prefix reconstruction
    ep_manifest_path = os.path.join(repo_root, "results", "paired_matching_pilot", "episode_metadata.jsonl")
    ep_lookup: Dict[str, Dict[str, Any]] = {}
    with open(ep_manifest_path) as f:
        for line in f:
            d = json.loads(line)
            if d.get("scenario_uid") in frozen_uids:
                ep_lookup[d["scenario_uid"]] = d

    # 3. Load nominal policy for prefix generation
    nominal_policy = load_policy(os.path.join(repo_root, "models", "checkpoints", "history_gru_best.pt"))

    # 4. Checkpoints to evaluate
    ckpt_dir = os.path.join(repo_root, "results", "recovery_training", "checkpoints")
    model_configs = [
        ("recovery_augmented_gru_seed42", os.path.join(ckpt_dir, "recovery_augmented_gru_seed42.pt")),
        ("recovery_augmented_gru_seed123", os.path.join(ckpt_dir, "recovery_augmented_gru_seed123.pt")),
        ("recovery_augmented_gru_seed456", os.path.join(ckpt_dir, "recovery_augmented_gru_seed456.pt")),
        ("recovery_augmented_mlp_seed42", os.path.join(ckpt_dir, "recovery_augmented_mlp_seed42.pt")),
    ]

    env = PushTargetEnv()
    scen_dir = os.path.join(repo_root, "results", "paired_scenarios", "scenarios")

    all_traces: List[Dict[str, Any]] = []
    comparisons: List[Dict[str, Any]] = []

    print("\nStarting bounded mechanism diagnostic rollouts...")
    start_time = time.time()

    for p_name, p_path in model_configs:
        print(f"Evaluating {p_name} across 20 scenarios (B0 vs B4)...")
        policy = load_policy(p_path)

        for uid in frozen_uids:
            ep_data = ep_lookup[uid]
            meta_path = os.path.join(scen_dir, uid, "metadata.json")
            with open(meta_path) as f:
                scen_meta = json.load(f)

            snap_npz = np.load(os.path.join(scen_dir, uid, "snapshot.npz"))
            snap = StateSnapshot.from_dict({
                **scen_meta["snapshot_dict"],
                "qpos": snap_npz["qpos"],
                "qvel": snap_npz["qvel"],
            })
            rem_h = scen_meta["remaining_horizon"]

            # Reconstruct exact prefix
            obs_prefix, act_prefix, snap_dev = extract_scenario_prefix(env, ep_data, nominal_policy)

            # Rollout B0 (preserved memory)
            res_b0 = run_mechanism_diagnostic_rollout(
                env, policy, p_name, uid, "B0", snap, obs_prefix, act_prefix, rem_h
            )
            # Rollout B4 (direct state injection)
            res_b4 = run_mechanism_diagnostic_rollout(
                env, policy, p_name, uid, "B4", snap, obs_prefix, act_prefix, rem_h
            )

            all_traces.append(res_b0)
            all_traces.append(res_b4)

            # Compute diagnostic comparison metrics
            act_b0 = np.array(res_b0["first_action"])
            act_b4 = np.array(res_b4["first_action"])
            first_act_diff = float(np.linalg.norm(act_b0 - act_b4)) if len(act_b0) > 0 and len(act_b4) > 0 else 0.0

            # Compare action sequence trajectories
            min_len = min(len(res_b0["actions_taken"]), len(res_b4["actions_taken"]))
            if min_len > 0:
                acts_0 = np.array(res_b0["actions_taken"][:min_len])
                acts_4 = np.array(res_b4["actions_taken"][:min_len])
                act_traj_mae = float(np.mean(np.abs(acts_0 - acts_4)))
                act_traj_max = float(np.max(np.abs(acts_0 - acts_4)))
            else:
                act_traj_mae = 0.0
                act_traj_max = 0.0

            # Trajectory object pos differences
            pos_min_len = min(len(res_b0["object_positions"]), len(res_b4["object_positions"]))
            if pos_min_len > 0:
                pos_0 = np.array(res_b0["object_positions"][:pos_min_len])
                pos_4 = np.array(res_b4["object_positions"][:pos_min_len])
                pos_drift = float(np.mean(np.linalg.norm(pos_0[:, :2] - pos_4[:, :2], axis=1)))
                pos_drift_max = float(np.max(np.linalg.norm(pos_0[:, :2] - pos_4[:, :2], axis=1)))
            else:
                pos_drift = 0.0
                pos_drift_max = 0.0

            # Yaw differences
            yaw_min_len = min(len(res_b0["object_yaws"]), len(res_b4["object_yaws"]))
            if yaw_min_len > 0:
                yaw_0 = np.array(res_b0["object_yaws"][:yaw_min_len])
                yaw_4 = np.array(res_b4["object_yaws"][:yaw_min_len])
                yaw_diff_mean = float(np.mean(np.abs(yaw_0 - yaw_4)))
            else:
                yaw_diff_mean = 0.0

            comp = {
                "policy_id": p_name,
                "scenario_uid": uid,
                "h_norm_b0": res_b0["h_norm_before"],
                "h_norm_b4": res_b4["h_norm_before"],
                "first_act_diff_norm": first_act_diff,
                "act_traj_mae": act_traj_mae,
                "act_traj_max": act_traj_max,
                "pos_drift_mean_m": pos_drift,
                "pos_drift_max_m": pos_drift_max,
                "yaw_diff_mean_rad": yaw_diff_mean,
                "final_dist_b0": res_b0["final_distance"],
                "final_dist_b4": res_b4["final_distance"],
                "dist_diff": abs(res_b0["final_distance"] - res_b4["final_distance"]),
                "success_b0": res_b0["is_success"],
                "success_b4": res_b4["is_success"],
                "outcome_discordant": 1 if res_b0["is_success"] != res_b4["is_success"] else 0,
            }
            comparisons.append(comp)

    # Save raw traces
    traces_path = os.path.join(out_dir, "diagnostic_traces.jsonl")
    with open(traces_path, "w", encoding="utf-8") as f:
        for t in all_traces:
            f.write(json.dumps(t) + "\n")

    # Aggregate summaries by policy
    summary: Dict[str, Any] = {
        "audit_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "scenarios_evaluated": len(frozen_uids),
        "total_rollouts": len(all_traces),
        "execution_time_sec": round(time.time() - start_time, 2),
        "policy_summaries": {}
    }

    for p_name, _ in model_configs:
        p_comps = [c for c in comparisons if c["policy_id"] == p_name]
        n_scens = len(p_comps)

        mean_h_b0 = float(np.mean([c["h_norm_b0"] for c in p_comps]))
        mean_first_act_diff = float(np.mean([c["first_act_diff_norm"] for c in p_comps]))
        mean_act_mae = float(np.mean([c["act_traj_mae"] for c in p_comps]))
        mean_pos_drift = float(np.mean([c["pos_drift_mean_m"] for c in p_comps]))
        mean_dist_diff = float(np.mean([c["dist_diff"] for c in p_comps]))

        succ_b0 = sum(c["success_b0"] for c in p_comps)
        succ_b4 = sum(c["success_b4"] for c in p_comps)
        discordant = sum(c["outcome_discordant"] for c in p_comps)

        summary["policy_summaries"][p_name] = {
            "num_scenarios": n_scens,
            "mean_h_norm_b0": mean_h_b0,
            "mean_first_act_diff": mean_first_act_diff,
            "mean_action_traj_mae": mean_act_mae,
            "mean_pos_drift_m": mean_pos_drift,
            "mean_final_dist_diff_m": mean_dist_diff,
            "success_b0": succ_b0,
            "success_rate_b0": succ_b0 / n_scens,
            "success_b4": succ_b4,
            "success_rate_b4": succ_b4 / n_scens,
            "signed_succ_diff": (succ_b0 - succ_b4) / n_scens,
            "abs_mean_succ_diff": abs(succ_b0 - succ_b4) / n_scens,
            "discordant_scenarios": discordant,
            "discordance_rate": discordant / n_scens,
        }

    summary_path = os.path.join(out_dir, "diagnostic_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\nCompleted diagnostics in {summary['execution_time_sec']}s.")
    print(f"Results saved to {summary_path}")
    for p_name, p_sum in summary["policy_summaries"].items():
        print(f"\n--- {p_name} ---")
        print(f"  Mean h(t_dev) norm (B0): {p_sum['mean_h_norm_b0']:.4f}")
        print(f"  Mean first action diff:  {p_sum['mean_first_act_diff']:.6f}")
        print(f"  Mean action traj MAE:    {p_sum['mean_action_traj_mae']:.6f}")
        print(f"  Mean pos drift:          {p_sum['mean_pos_drift_m']:.4f} m")
        print(f"  Success B0 vs B4:        {p_sum['success_b0']}/{n_scens} vs {p_sum['success_b4']}/{n_scens}")
        print(f"  Discordant outcomes:     {p_sum['discordant_scenarios']}/{n_scens} ({p_sum['discordance_rate']*100:.1f}%)")


if __name__ == "__main__":
    main()

