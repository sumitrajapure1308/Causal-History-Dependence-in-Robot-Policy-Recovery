"""Counterfactual Recovery Condition Evaluation Script.

Executes pilot counterfactual recovery evaluations across Conditions B0, B2, and B4:
- B0: Matched physical state with full original observation, action, and hidden history.
- B2: Matched physical state with observation history ablated.
- B4: Matched physical state with all history removed (obs ablated, act ablated, h = 0).
- Oracle filter: Verifies physical recoverability (R_oracle == 1) from state s(t_d).
- Saves condition report to results/pilot_recovery/condition_report.json.
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

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.environments.state_snapshot import StateSnapshot
from causal_history_recovery.policies.policy_registry import load_policy
from causal_history_recovery.controllers.privileged_oracle import PrivilegedOracleController
from causal_history_recovery.counterfactuals.condition_generator import ConditionGenerator


def evaluate_recovery_conditions(
    policy_type: str = "history_gru",
    num_episodes: int = 20,
    base_seed: int = 42,
    output_path: str = "results/pilot_recovery/condition_report.json",
) -> Dict[str, Any]:
    """Run pilot counterfactual recovery protocol across B0, B2, B4."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    checkpoint_path = os.path.join(repo_root, "models", "checkpoints", f"{policy_type}_best.pt")

    policy = load_policy(checkpoint_path, device="cpu")
    env = PushTargetEnv(max_horizon=150)
    cond_gen = ConditionGenerator(env)
    oracle = PrivilegedOracleController()

    conditions_to_test = ["B0", "B2", "B4"]
    evaluation_records = []
    condition_success_counts = {c: 0 for c in conditions_to_test}
    total_recoverable_scenarios = 0

    print(f"Running Pilot Recovery Evaluation for {policy_type} ({num_episodes} episodes, conditions {conditions_to_test})...")
    start_time = time.time()

    for idx in range(num_episodes):
        ep_seed = base_seed + idx * 7

        # 1. Generate candidate deviation
        obs, info = env.reset(seed=ep_seed)
        policy.reset(obs)
        obj_init = env.get_object_position().copy()

        action_prefix = []
        deviation_detected = False
        deviation_time = None
        candidate_snapshot = None

        for step in range(150):
            if step == 25:
                act = np.array([0.0, 0.016, 0.0], dtype=np.float32)
            else:
                act = policy.act(obs, deterministic=True)

            action_prefix.append(act.copy())
            obs, r, term, trunc, step_info = env.step(act)

            yaw_deg = abs(np.degrees(env.get_object_yaw()))
            drift_m = abs(env.get_object_position()[1] - obj_init[1])

            if step >= 25 and not deviation_detected:
                if yaw_deg >= 15.0 and drift_m >= 0.020:
                    deviation_detected = True
                    deviation_time = step
                    candidate_snapshot = env.get_state_snapshot()
                    break

            if term or trunc:
                break

        if not deviation_detected or candidate_snapshot is None:
            continue

        # 2. Privileged Oracle Recoverability Filter
        oracle_admitted, oracle_audit = oracle.verify_scenario_recoverability(env, candidate_snapshot)
        if not oracle_admitted:
            # Strictly exclude unrecoverable failure states from evaluation
            continue

        total_recoverable_scenarios += 1

        # 3. Evaluate each counterfactual condition from the matched candidate state
        scenario_record = {
            "episode_index": idx,
            "seed": ep_seed,
            "deviation_time": deviation_time,
            "oracle_recoverable": True,
            "oracle_steps": oracle_audit["execution"]["steps_executed"],
            "conditions": {},
        }

        for cond in conditions_to_test:
            prep_info = cond_gen.prepare_condition_rollout(
                condition=cond,
                policy=policy,
                source_snapshot=candidate_snapshot,
                action_prefix=action_prefix,
                seed=ep_seed,
            )

            # Roll out policy from t_d to end of horizon
            cur_obs = prep_info["current_observation"]
            rem_h = prep_info["remaining_horizon"]
            success = False
            dwell_count = 0

            for t in range(rem_h):
                act = policy.act(cur_obs, deterministic=True)
                cur_obs, r, term, trunc, step_info = env.step(act)
                dwell_count = step_info.get("dwell_count", 0)

                if step_info["is_success"]:
                    success = True
                    break
                if term or trunc:
                    break

            if success:
                condition_success_counts[cond] += 1

            scenario_record["conditions"][cond] = {
                "success": bool(success),
                "dwell_count": int(dwell_count),
                "final_dist_to_goal": float(step_info.get("dist_to_goal", 0.0)),
                "state_matching_error": prep_info["state_matching_error"],
            }

        evaluation_records.append(scenario_record)
        print(f"Scenario {len(evaluation_records):2d} (Ep {idx:2d}, td={deviation_time:2d}) | B0: {scenario_record['conditions']['B0']['success']} | B2: {scenario_record['conditions']['B2']['success']} | B4: {scenario_record['conditions']['B4']['success']}")

    total_time = time.time() - start_time

    summary = {
        "policy_type": policy_type,
        "base_seed": base_seed,
        "total_episodes_tested": num_episodes,
        "recoverable_scenarios_admitted": total_recoverable_scenarios,
        "condition_success_counts": condition_success_counts,
        "condition_recovery_rates": {
            cond: float(condition_success_counts[cond] / total_recoverable_scenarios)
            if total_recoverable_scenarios > 0
            else 0.0
            for cond in conditions_to_test
        },
        "total_runtime_seconds": float(total_time),
        "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "scenarios": evaluation_records,
    }

    abs_out = os.path.join(repo_root, output_path)
    os.makedirs(os.path.dirname(abs_out), exist_ok=True)
    with open(abs_out, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Recovery condition evaluation complete in {total_time:.2f}s.")
    print(f"Admitted recoverable scenarios: {total_recoverable_scenarios}")
    print(f"Recovery rates: {summary['condition_recovery_rates']}")
    print(f"Saved report to {abs_out}")

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=str, default="history_gru", choices=["reactive_mlp", "history_gru"])
    parser.add_argument("--episodes", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str, default="results/pilot_recovery/condition_report.json")
    args = parser.parse_args()

    evaluate_recovery_conditions(
        policy_type=args.policy,
        num_episodes=args.episodes,
        base_seed=args.seed,
        output_path=args.output,
    )

