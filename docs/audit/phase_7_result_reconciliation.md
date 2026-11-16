# Phase 7 Result Reconciliation Audit

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Status:** VALIDATED AUDIT  
**Audit Date:** 2026-11-09  
**Auditor:** Lead Robotics Researcher & Reproducibility Auditor  
**Dataset Under Audit:** `results/recovery_capability_validation/validation_records.jsonl` (600 records)  

---

## 1. Executive Summary

This forensic reconciliation audits the recovery capability evaluation records generated in Phase 7. The primary objective is to verify whether the 600 logged execution records represent 600 independent stochastic trials, explain the exact denominators behind every published percentage, inspect the apparent mismatch between recovery success rates and corrective-action rates, and establish the exact experimental conditions under which the policies were evaluated.

### Key Audit Findings:
1. **Deterministic Duplication ($N=20$, Not $N=60$):**
   The 600 logged rollout records in `validation_records.jsonl` represent exactly 200 unique `(policy, scenario, condition)` combinations evaluated across 3 evaluation seeds (`42, 500, 2000`). Because simulation restoration (`env.restore_state_snapshot`) and policy inference (`act(deterministic=True)`) are entirely deterministic and no process noise was injected, **all 3 repeats produced 100% bitwise identical actions, state trajectories, and outcomes**. The true effective sample size for statistical analysis is $N = 20$ independent physical scenarios per condition, not $N = 60$.

2. **Reconciled Performance Table (Exact Denominator $N=20$):**
   - **Reactive MLP:** 1/20 (5.0%) success in B0; 1/20 (5.0%) success in B4; 0/20 (0.0%) corrective action in both.
   - **History-Aware GRU (Nominal):** 1/20 (5.0%) success in B0; 1/20 (5.0%) success in B4; 0/20 (0.0%) corrective action in both.
   - **Recovery-Augmented MLP:** 4/20 (20.0%) success in B0; 4/20 (20.0%) success in B4; 8/20 (40.0%) corrective action in both.
   - **Recovery-Augmented GRU:** 5/20 (25.0%) success in B0; 5/20 (25.0%) success in B4; 1/20 (5.0%) corrective action in both.
   - **Privileged Oracle:** 20/20 (100.0%) success in B0; 20/20 (100.0%) success in B4; 20/20 (100.0%) corrective action in both.

3. **Identification of Phase 7 Logging & Evaluation Harness Defects:**
   - **Detection and Diagnosis Hardcoding:** In `validate_recovery_capability.py`, the fields `detection_rate: 1.0` and `diagnosis_rate: 1.0` were hardcoded constants in the returned dictionary for all policies. None of the learned policies possess an active diagnosis head.
   - **Absence of Prefix Unrolling in B0:** In `validate_recovery_capability.py` (lines 81–86), `policy.reset(current_obs)` was invoked at the onset of recovery for all policies. Under condition B0, the execution prefix was never replayed into the policy's recurrent memory or observation/action buffers. Consequently, B0 and B4 both executed with zeroed hidden states and zeroed buffers, guaranteeing 100% identical outputs.

---

## 2. Experimental Factor Lineage & Disentanglement

To ensure total transparency, all seeds, hashes, identifiers, and conditions are explicitly disentangled below:

| Column / Factor | Explicit Value / Range | Role & Scientific Meaning |
|---|---|---|
| `training_seed` | 42 (MLP, Nom GRU, Rec MLP), 456 (Rec GRU best) | Pseudo-random seed used during PyTorch network training and parameter optimization. |
| `scenario_generation_seed` | 49, 91, 98, 112, 133, 147, 196, 217, 231, 238, 252, 287, 301, 308, 385, 528, 570, 591, 626, 633 | Seed passed to `PushTargetEnv.reset(seed=...)` to generate the initial physical placement. |
| `evaluation_noise_seed` | 42, 500, 2000 | Nominal seed argument passed to `evaluate_rollout`. Injected zero process or sensor noise. |
| `checkpoint_hash` | See Table in Section 3 | SHA-256 fingerprint of the exact `.pt` binary weights used. |
| `scenario_uid` | 20 unique strings (e.g. `scen_history_gru_s49_t53_a2060d`) | Unique identifier for physical state snapshot. |
| `condition` | B0, B4 | Intended history intervention condition. |
| `repeat_id` | 1, 2, 3 (corresponding to eval seeds 42, 500, 2000) | Deterministic triplicate run. |

---

## 3. Checkpoint Inventory & Provenance

| Policy ID | Checkpoint File Path | Checkpoint SHA-256 (first 16 chars) | Training Seed | Parameter Health Status |
|---|---|---|---|---|
| `reactive_mlp` | `models/checkpoints/reactive_mlp_best.pt` | `f99beb840b878d34` | 42 | Healthy weights; nominal non-recurrent policy. |
| `history_gru` | `models/checkpoints/history_gru_best.pt` | `5fcf94e2410efca8` | 42 | **Collapsed weights:** all GRU weights $\sim 3.25 \times 10^{-38}$. Open-loop bias pusher. |
| `recovery_augmented_mlp` | `models/checkpoints/recovery_augmented_mlp_best.pt` | `1aba926f4ad7bbd1` | 42 | Healthy weights; conditioned on augmented features ($d=24$). Matches `seed42.pt`. |
| `recovery_augmented_gru` | `models/checkpoints/recovery_augmented_gru_best.pt` | `7888cc1fc63b7d2d` | 456 | Healthy weights; conditioned on recurrent history ($d=28$). Matches `seed456.pt`. |
| `privileged_oracle` | Algorithmic (`PrivilegedOracleController`) | N/A (Code) | N/A | Closed-loop geometric standoff controller with direct MuJoCo state access. |

---

## 4. Reconciled Evaluation Results on $N=20$ Unique Physical Scenarios

The 20 physical scenarios evaluated were drawn from the admitted pool of 38 paired scenarios validated in Phase 5. All 20 scenarios were verified by the privileged oracle as mechanically recoverable within their remaining horizons.

| Policy | Condition | Successes ($k / 20$) | Success Rate | Corrective Actions ($k / 20$) | Corrective Rate | Mean Effort ($\bar{u}^2$) | Mean Recovery Time ($t_{\text{rec}}$) |
|---|---|---|---|---|---|---|---|
| `reactive_mlp` | B0 | 1 / 20 | 5.0% | 0 / 20 | 0.0% | 0.000012 | 93.3 |
| `reactive_mlp` | B4 | 1 / 20 | 5.0% | 0 / 20 | 0.0% | 0.000012 | 93.3 |
| `history_gru` | B0 | 1 / 20 | 5.0% | 0 / 20 | 0.0% | 0.000012 | 93.3 |
| `history_gru` | B4 | 1 / 20 | 5.0% | 0 / 20 | 0.0% | 0.000012 | 93.3 |
| `recovery_augmented_mlp` | B0 | 4 / 20 | 20.0% | 8 / 20 | 40.0% | 0.000003 | 84.4 |
| `recovery_augmented_mlp` | B4 | 4 / 20 | 20.0% | 8 / 20 | 40.0% | 0.000003 | 84.4 |
| `recovery_augmented_gru` | B0 | 5 / 20 | 25.0% | 1 / 20 | 5.0% | 0.000005 | 80.3 |
| `recovery_augmented_gru` | B4 | 5 / 20 | 25.0% | 1 / 20 | 5.0% | 0.000005 | 80.3 |
| `privileged_oracle` | B0 | 20 / 20 | 100.0% | 20 / 20 | 100.0% | 0.001250 | 96.7 |
| `privileged_oracle` | B4 | 20 / 20 | 100.0% | 20 / 20 | 100.0% | 0.001250 | 96.7 |

---

## 5. Investigation of the 25% Success vs. 5% Corrective Action Mismatch

A central mystery raised in Phase 7 is how `recovery_augmented_gru` achieved 5 successes (25.0%) while logging active corrective maneuvering in only 1 scenario (5.0%).

### Forensic Rollout Inspection:
In `validate_recovery_capability.py`, the heuristic for detecting corrective action was defined as:
$$\text{Corrective Action} \iff \exists t \in [0, T]: \quad a_x(t) < -0.002 \quad \lor \quad |a_y(t)| > 0.003$$
This threshold detects explicit backward retraction ($a_x < -0.002$) or aggressive lateral turning ($|a_y| > 0.003$).

Examining the 5 successful episodes of `recovery_augmented_gru`:
1. **Scenario 1 (`scen_..._s49_t53`):** Succeeded at $t=54$. Corrective action logged: **YES**. Action sequence exhibited lateral corrective push $a_y = +0.0034$.
2. **Scenario 2 (`scen_..._s91_t58`):** Succeeded at $t=62$. Corrective action logged: **NO**. The object initial post-deviation pose had already aligned favorably with the target. A forward push with $a_y = 0.0018$ was sufficient to cross the $4\text{ cm}$ target boundary without exceeding the $0.003$ threshold.
3. **Scenario 4 (`scen_..._s112_t49`):** Succeeded at $t=58$. Corrective action logged: **NO**. Pusher gently made contact on the left edge, nudging the block forward-right toward the goal ($a_y = 0.0014$).
4. **Scenario 7 (`scen_..._s196_t52`):** Succeeded at $t=65$. Corrective action logged: **NO**. Object reached goal boundary through shallow forward drift.
5. **Scenario 15 (`scen_..._s385_t50`):** Succeeded at $t=72$. Corrective action logged: **NO**. Block pushed straight into target zone without requiring aggressive lateral turning.

**Conclusion:** The mismatch is an artifact of the conservative heuristic threshold. 4 of the 5 "successes" were mild perturbations where gentle, sub-threshold forward-diagonal pushes were sufficient for target acquisition. The policy did not execute an explicit repositioning maneuver in those 4 episodes.

---

## 6. Audit of the Privileged Oracle Comparison

The Privileged Oracle achieved 20/20 (100.0%) recovery success under both B0 and B4.
- **Why 100%?** In Phase 5, candidate failure states were admitted into the paired benchmark only if they passed an initial recoverability filter executed by this exact same Privileged Oracle (`oracle.verify_scenario_recoverability(...)`). Therefore, by construction, the admitted pool represents the set of scenarios geometrically solvable by the oracle.
- **Oracle Role:** As established in project directives, the oracle serves strictly as an upper-bound feasibility instrument and scenario verification gate, **not as a learned policy baseline**.

---

## 7. Audit Sign-Off

The Phase 7 results are fully reconciled. The apparent sample size of $N=600$ is formally clarified as $N=20$ independent scenarios evaluated across deterministic triplicates. The zero B0/B4 difference in Phase 7 is proven to be caused by the omission of prefix unrolling in the evaluation script.

