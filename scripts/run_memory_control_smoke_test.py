#!/usr/bin/env python3
"""Memory Control Validation Smoke Test.

Executes a targeted validation of explicit memory controls:
1. M_REPLAY_PRESERVED (Condition A): Replay prefix with preserved unrolled policy memory.
2. M_INJECT_PRESERVED (Condition B): Matched state injection with preserved policy memory.
3. M_INJECT_RESET (Condition C): Matched state injection with reset policy memory.
4. M_INJECT_ALTERNATIVE (Condition D): Matched state injection with alternative compatible memory.

Validates:
- Memory restoration exactness (||h_B - h_A|| <= 1e-6).
- Memory reset exactness (||h_C|| == 0.0).
- Action prefix unrolling determinism.
- Exact physical state restoration (D <= 1e-10 m).
- Remaining task horizon preservation across conditions.
- Absence of memory leakage across successive evaluations.

Outputs results to: results/memory_control_smoke/smoke_results.json
"""

from __future__ import annotations

import os
import sys
import time
import json
from typing import Any, Dict, List, Optional
import numpy as np
import torch

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(repo_root, "src"))

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.environments.second_push_task_env import SecondPushTaskEnv
from causal_history_recovery.environments.state_snapshot import StateSnapshot
from causal_history_recovery.policies.policy_registry import load_policy
from causal_history_recovery.counterfactuals.condition_generator import (
    ConditionGenerator,
    COND_REPLAY_PRESERVED,
    COND_INJECT_PRESERVED,
    COND_INJECT_RESET,
    COND_INJECT_ALTERNATIVE,
)


def get_fresh_env(task_id: str):
    """Instantiate a fresh environment instance to prevent cross-scenario contamination."""
    if "task2" in task_id:
        return SecondPushTaskEnv(max_yaw_tolerance_rad=3.15)
    return PushTargetEnv()


def run_memory_control_smoke_test() -> Dict[str, Any]:
    print("=" * 70)
    print("MEMORY CONTROL VALIDATION SMOKE TEST")
    print("=" * 70)

    # 1. Select 4 representative scenarios (1 per benchmark cell)
    scen_dir = os.path.join(repo_root, "results", "phase_12_stage_c", "scenarios")
    test_uids = [
        "cell1_t1_slip_10001_00",
        "cell2_t1_loss_11003_00",
        "cell3_t2_slip_12002_00",
        "cell4_t2_loss_13001_00",
    ]

    scenarios = []
    for uid in test_uids:
        u_path = os.path.join(scen_dir, uid)
        if not os.path.isdir(u_path):
            raise FileNotFoundError(f"Scenario directory missing: {u_path}")
        with open(os.path.join(u_path, "metadata.json"), "r", encoding="utf-8") as f:
            meta = json.load(f)
        snap_data = np.load(os.path.join(u_path, "snapshot.npz"), allow_pickle=True)
        pref_data = np.load(os.path.join(u_path, "prefix.npz"), allow_pickle=True)
        scenarios.append({
            "uid": uid,
            "meta": meta,
            "snap_data": snap_data,
            "pref_data": pref_data,
        })
    print(f"Loaded {len(scenarios)} representative scenarios from benchmark cells.")

    # 2. Load policies (including recurrent GRU with active memory and stateless baseline)
    ckpt_dir = os.path.join(repo_root, "models", "checkpoints")
    policies = {
        "rec_aug_gru": load_policy(os.path.join(ckpt_dir, "recovery_augmented_gru_best.pt")),
        "history_gru": load_policy(os.path.join(ckpt_dir, "history_gru_best.pt")),
        "reactive_mlp": load_policy(os.path.join(ckpt_dir, "reactive_mlp_best.pt")),
    }
    print(f"Loaded policies: {list(policies.keys())}")

    conditions = [
        COND_REPLAY_PRESERVED,
        COND_INJECT_PRESERVED,
        COND_INJECT_RESET,
        COND_INJECT_ALTERNATIVE,
    ]

    eval_results = []
    exactness_checks = {
        "memory_restoration_exactness": [],
        "memory_reset_exactness": [],
        "prefix_unroll_determinism": [],
        "state_matching_error": [],
        "remaining_horizon_preserved": [],
        "memory_leakage_checks": [],
    }

    start_time = time.time()

    for sc in scenarios:
        uid = sc["uid"]
        meta = sc["meta"]
        task_id = meta["task_id"]
        failure_mode = meta["failure_mode"]
        seed = meta["seed"]
        rem_h = meta["remaining_horizon"]
        goal_pos = np.array(meta["goal_state"], dtype=np.float64)

        snap_data = sc["snap_data"]
        pref_data = sc["pref_data"]
        act_pref = [pref_data["actions"][i] for i in range(len(pref_data["actions"]))]

        step_cnt = int(snap_data["step_count"]) if "step_count" in snap_data else len(act_pref)
        max_h = int(snap_data["max_horizon"]) if "max_horizon" in snap_data else 150
        rem_h_snap = int(snap_data["remaining_horizon"]) if "remaining_horizon" in snap_data else (max_h - step_cnt)

        # Reconstruct canonical snapshot with complete Markovian and horizon scalars
        target_snap = StateSnapshot(
            qpos=snap_data["qpos"],
            qvel=snap_data["qvel"],
            act=snap_data["act"] if "act" in snap_data and snap_data["act"] is not None else None,
            qacc_warmstart=snap_data["qacc_warmstart"] if "qacc_warmstart" in snap_data and snap_data["qacc_warmstart"] is not None else None,
            qfrc_applied=snap_data["qfrc_applied"] if "qfrc_applied" in snap_data and snap_data["qfrc_applied"] is not None else None,
            xfrc_applied=snap_data["xfrc_applied"] if "xfrc_applied" in snap_data and snap_data["xfrc_applied"] is not None else None,
            ctrl=snap_data["ctrl"] if "ctrl" in snap_data and snap_data["ctrl"] is not None else None,
            time=float(snap_data["time"]) if "time" in snap_data else 0.0,
            step_count=step_cnt,
            remaining_horizon=rem_h_snap,
            max_horizon=max_h,
            task_goal=goal_pos,
        )

        print(f"\n--- Scenario: {uid} (Task: {task_id}, Failure: {failure_mode}) ---")

        # Determinism check: unroll prefix twice with rec_aug_gru
        test_env = get_fresh_env(task_id)
        cond_gen_det = ConditionGenerator(test_env)
        rec_policy = policies["rec_aug_gru"]
        mem_unroll_1 = cond_gen_det.unroll_policy_memory_on_prefix(rec_policy, seed, act_pref)
        h_unroll_1 = mem_unroll_1["hidden_state"].numpy().copy()
        mem_unroll_2 = cond_gen_det.unroll_policy_memory_on_prefix(rec_policy, seed, act_pref)
        h_unroll_2 = mem_unroll_2["hidden_state"].numpy().copy()

        unroll_diff = float(np.linalg.norm(h_unroll_1 - h_unroll_2))
        exactness_checks["prefix_unroll_determinism"].append({
            "scenario": uid,
            "policy": "rec_aug_gru",
            "unroll_diff": unroll_diff,
            "passed": unroll_diff < 1e-10,
        })
        print(f"  Prefix Unroll Determinism Diff (rec_aug_gru): {unroll_diff:.2e} (Passed: {unroll_diff < 1e-10})")

        # Evaluate across policies and conditions
        for pol_id, policy in policies.items():
            h_preserved_replay = None

            for cond in conditions:
                # Use a clean environment instance for each condition
                run_env = get_fresh_env(task_id)
                cond_gen = ConditionGenerator(run_env)

                # Prepare condition
                setup_info = cond_gen.prepare_condition_rollout(
                    condition=cond,
                    policy=policy,
                    source_snapshot=target_snap,
                    action_prefix=act_pref,
                    seed=seed,
                )

                state_err = setup_info["state_matching_error"]
                rem_h_actual = run_env.remaining_horizon
                h_norm = setup_info["initial_hidden_norm"]

                # Check state matching error
                state_match_passed = state_err <= 1e-10
                exactness_checks["state_matching_error"].append({
                    "scenario": uid,
                    "policy": pol_id,
                    "condition": cond,
                    "state_error_m": state_err,
                    "passed": state_match_passed,
                })

                # Check horizon preservation
                horizon_passed = (rem_h_actual == rem_h_snap)
                exactness_checks["remaining_horizon_preserved"].append({
                    "scenario": uid,
                    "policy": pol_id,
                    "condition": cond,
                    "expected_rem_h": rem_h_snap,
                    "actual_rem_h": rem_h_actual,
                    "passed": horizon_passed,
                })

                # Check memory specifics for recurrent policy
                if policy.has_recurrent_memory():
                    curr_h = policy.get_hidden_state().numpy().copy()

                    if cond == COND_REPLAY_PRESERVED:
                        h_preserved_replay = curr_h.copy()

                    elif cond == COND_INJECT_PRESERVED:
                        if h_preserved_replay is not None:
                            h_diff = float(np.linalg.norm(curr_h - h_preserved_replay))
                            restoration_passed = (h_diff <= 1e-6)
                            exactness_checks["memory_restoration_exactness"].append({
                                "scenario": uid,
                                "policy": pol_id,
                                "h_diff": h_diff,
                                "passed": restoration_passed,
                            })

                    elif cond == COND_INJECT_RESET:
                        h_reset_norm = float(np.linalg.norm(curr_h))
                        reset_passed = (h_reset_norm == 0.0)
                        exactness_checks["memory_reset_exactness"].append({
                            "scenario": uid,
                            "policy": pol_id,
                            "h_norm": h_reset_norm,
                            "passed": reset_passed,
                        })

                # Execute short rollout (up to 30 steps or task completion)
                cur_obs = setup_info["current_observation"]
                steps = 0
                is_success = False
                max_rollout_steps = min(30, rem_h_actual)

                for step in range(max_rollout_steps):
                    action = policy.act(cur_obs, deterministic=True)
                    cur_obs, reward, terminated, truncated, step_info = run_env.step(action)
                    steps += 1
                    if step_info.get("is_success", False):
                        is_success = True
                        break
                    if terminated or truncated:
                        break

                eval_results.append({
                    "scenario_uid": uid,
                    "task_id": task_id,
                    "failure_mode": failure_mode,
                    "policy_id": pol_id,
                    "condition": cond,
                    "steps": steps,
                    "is_success": is_success,
                    "state_matching_error": state_err,
                    "initial_hidden_norm": h_norm,
                    "remaining_horizon": rem_h_actual,
                })

                print(f"  [{pol_id:12s}] {cond:22s} | steps={steps:2d} | succ={is_success!s:5s} | err={state_err:.1e} | rem_h={rem_h_actual:3d} | h_norm={h_norm:.4f}")

        # Memory leakage test on this scenario: B -> C -> B
        leak_env = get_fresh_env(task_id)
        cond_gen_leak = ConditionGenerator(leak_env)
        test_gru = policies["rec_aug_gru"]

        # Step 1: Set condition B (Preserved)
        cond_gen_leak.prepare_condition_rollout(
            condition=COND_INJECT_PRESERVED,
            policy=test_gru,
            source_snapshot=target_snap,
            action_prefix=act_pref,
            seed=seed,
        )
        h_b1_norm = float(torch.norm(test_gru.get_hidden_state()).item())

        # Step 2: Set condition C (Reset) on SAME policy instance
        cond_gen_leak.prepare_condition_rollout(
            condition=COND_INJECT_RESET,
            policy=test_gru,
            source_snapshot=target_snap,
            action_prefix=act_pref,
            seed=seed,
        )
        h_c_norm = float(torch.norm(test_gru.get_hidden_state()).item())

        # Step 3: Set condition B (Preserved) again on SAME policy instance
        cond_gen_leak.prepare_condition_rollout(
            condition=COND_INJECT_PRESERVED,
            policy=test_gru,
            source_snapshot=target_snap,
            action_prefix=act_pref,
            seed=seed,
        )
        h_b2_norm = float(torch.norm(test_gru.get_hidden_state()).item())

        leakage_passed = (h_b1_norm > 1e-4) and (h_c_norm == 0.0) and (np.isclose(h_b1_norm, h_b2_norm, atol=1e-5))
        exactness_checks["memory_leakage_checks"].append({
            "scenario": uid,
            "policy": "rec_aug_gru",
            "h_b1_norm": h_b1_norm,
            "h_c_norm": h_c_norm,
            "h_b2_norm": h_b2_norm,
            "passed": bool(leakage_passed),
        })
        print(f"  Memory Leakage Test (B->C->B): Passed = {leakage_passed} (h_B1={h_b1_norm:.4f}, h_C={h_c_norm:.4f}, h_B2={h_b2_norm:.4f})")

    elapsed_time = time.time() - start_time

    # Verification Summary
    restoration_all_pass = all(c["passed"] for c in exactness_checks["memory_restoration_exactness"])
    reset_all_pass = all(c["passed"] for c in exactness_checks["memory_reset_exactness"])
    unroll_all_pass = all(c["passed"] for c in exactness_checks["prefix_unroll_determinism"])
    state_match_all_pass = all(c["passed"] for c in exactness_checks["state_matching_error"])
    horizon_all_pass = all(c["passed"] for c in exactness_checks["remaining_horizon_preserved"])
    leakage_all_pass = all(c["passed"] for c in exactness_checks["memory_leakage_checks"])

    all_checks_passed = (
        restoration_all_pass
        and reset_all_pass
        and unroll_all_pass
        and state_match_all_pass
        and horizon_all_pass
        and leakage_all_pass
    )

    max_state_error = max(c["state_error_m"] for c in exactness_checks["state_matching_error"])
    max_h_diff = max(c["h_diff"] for c in exactness_checks["memory_restoration_exactness"]) if exactness_checks["memory_restoration_exactness"] else 0.0
    max_h_reset_norm = max(c["h_norm"] for c in exactness_checks["memory_reset_exactness"]) if exactness_checks["memory_reset_exactness"] else 0.0

    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"1. Memory Restoration Exactness: {'PASSED' if restoration_all_pass else 'FAILED'} (max diff = {max_h_diff:.2e})")
    print(f"2. Memory Reset Exactness:       {'PASSED' if reset_all_pass else 'FAILED'} (max norm = {max_h_reset_norm:.2e})")
    print(f"3. Prefix Unroll Determinism:    {'PASSED' if unroll_all_pass else 'FAILED'}")
    print(f"4. State Matching Invariance:   {'PASSED' if state_match_all_pass else 'FAILED'} (max error = {max_state_error:.2e} m)")
    print(f"5. Remaining Horizon Invariance: {'PASSED' if horizon_all_pass else 'FAILED'}")
    print(f"6. Memory Leakage Prevention:    {'PASSED' if leakage_all_pass else 'FAILED'}")
    print(f"Overall Validation Status:       {'ALL CHECKS PASSED' if all_checks_passed else 'SOME CHECKS FAILED'}")
    print(f"Total Runtime:                   {elapsed_time:.2f} s")
    print("=" * 70)

    smoke_output = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_scenarios_tested": len(scenarios),
        "total_rollouts_executed": len(eval_results),
        "policies_tested": list(policies.keys()),
        "conditions_tested": conditions,
        "verification_summary": {
            "all_checks_passed": all_checks_passed,
            "memory_restoration_exactness_passed": restoration_all_pass,
            "memory_reset_exactness_passed": reset_all_pass,
            "prefix_unroll_determinism_passed": unroll_all_pass,
            "state_matching_invariance_passed": state_match_all_pass,
            "remaining_horizon_invariance_passed": horizon_all_pass,
            "memory_leakage_prevention_passed": leakage_all_pass,
            "max_state_matching_error_m": max_state_error,
            "max_memory_restoration_diff": max_h_diff,
            "max_memory_reset_norm": max_h_reset_norm,
        },
        "exactness_checks": exactness_checks,
        "rollout_results": eval_results,
        "runtime_seconds": elapsed_time,
    }

    out_dir = os.path.join(repo_root, "results", "memory_control_smoke")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "smoke_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(smoke_output, f, indent=2)
    print(f"Wrote smoke test results to: {out_file}")

    return smoke_output


if __name__ == "__main__":
    run_memory_control_smoke_test()
