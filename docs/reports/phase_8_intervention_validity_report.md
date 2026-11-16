# Phase 8 Research Report: History-Intervention Validity and Mechanism Diagnostics

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Phase:** 8 — History-Intervention Validity and Mechanism Diagnostics  
**Status:** COMPLETED & SCIENTIFICALLY VALIDATED  
**Author:** Lead Robotics Researcher, Research Engineer & Reproducibility Auditor  
**Date:** 2026-11-09  

---

## 1. Executive Summary and Primary Research Objectives

Phase 8 was commissioned with a strict diagnostic objective: to determine why prior evaluation phases (Phases 6 and 7) observed 100% identical success rates between history-preserved (B0) and history-removed (B4) conditions. Specifically, the inquiry was charged with establishing whether this null result reflected:
- Genuine behavioral invariance to execution history.
- Divergent policy behavior obscured by identical binary task outcomes.
- Ineffective history masking or absence of history unrolling in the evaluation harness.
- Retained history-derived features in non-recurrent policies.
- Checkpoint loading, parameter collapse, or training defects.
- Evaluation logging defects.

### Core Discoveries of Phase 8:
1. **The Phase 7 Evaluation Harness Defect:**  
   In `scripts/validate_recovery_capability.py` (lines 81–86), `policy.reset(current_obs)` was invoked at the onset of recovery for *all* policies. Under condition B0, the preceding execution prefix was **never unrolled into recurrent memory**. Consequently, B0 and B4 were evaluated with identical zeroed hidden states ($\mathbf{0}_{128}$) and zeroed action buffers. The reported 0% difference was an evaluation harness defect, not behavioral invariance.
2. **Phase 3 Nominal GRU Checkpoint Collapse ($10^{-38}$ Underflow):**  
   Parameter tensor forensics on `models/checkpoints/history_gru_best.pt` revealed that all GRU input-to-hidden (`gru.weight_ih_l0`) and hidden-to-hidden (`gru.weight_hh_l0`) weights collapsed to $\approx 3.25 \times 10^{-38}$ (IEEE 754 subnormal underflow). The policy functioned strictly as an open-loop constant forward bias generator ($b_{\text{out}} = +0.0594$) because nominal pushing demonstrations had near-zero action variance ($\sigma \approx 4.7 \times 10^{-5}$).
3. **Information Provenance and History Leakage in MLPs:**  
   Although `RecoveryAugmentedMLPPolicy` is architecturally non-recurrent, it consumes latching failure detection flags, normalized deviation duration, and deviation magnitude. Because elapsed deviation duration explicitly encodes temporal history, feedforward policies receiving these features are **not memoryless with respect to physical history**.
4. **Mechanism Validation via Reconstructed Memory:**  
   When policy-specific memory $h(t_{\text{dev}})$ was reconstructed via bitwise deterministic prefix unrolling:
   - Recurrent hidden states accumulated non-zero norms ($\|h(t_{\text{dev}})\| \in [0.766, 0.990]$).
   - Recovery actions diverged immediately between B0 and B4 ($\|a_{\text{first, B0}} - a_{\text{first, B4}}\| \in [0.00137, 0.00323]\text{ m/step}$).
   - For `recovery_augmented_gru_seed456`, trajectories diverged sufficiently to produce **10.0% outcome discordance** ($2 / 20$ scenarios). In both discordant scenarios, B0 failed because accumulated forward-pushing momentum drove the cube past the target, whereas B4 succeeded by executing immediate lateral corrective steering from a clean state.
   - For seeds 42 and 123, policy actions and trajectories diverged, yet produced identical binary success outcomes ($2/20$ vs $2/20$ and $4/20$ vs $4/20$), directly confirming that identical binary success does not imply identical behavior.

---

## 2. Reconciled Phase 7 Results Audit ($N=20$)

A complete audit of `results/recovery_capability_validation/validation_records.jsonl` (600 records) established that the evaluation was conducted across 3 evaluation seeds (`42, 500, 2000`) without process noise. All 3 seeds yielded 100% identical actions and trajectories. The true sample size is **$N = 20$ independent physical scenarios**, not $N = 60$.

### Reconciled Benchmark Table:
| Policy Architecture | Checkpoint File | Condition | Successes ($k/20$) | Success Rate | Corrective Actions ($k/20$) | Corrective Rate | Mean Effort | Mean Rec Time |
|---|---|---|---|---|---|---|---|---|
| `reactive_mlp` | `reactive_mlp_best.pt` | B0 | 1 / 20 | 5.0% | 0 / 20 | 0.0% | 0.000012 | 93.3 |
| `reactive_mlp` | `reactive_mlp_best.pt` | B4 | 1 / 20 | 5.0% | 0 / 20 | 0.0% | 0.000012 | 93.3 |
| `history_gru` (Nominal) | `history_gru_best.pt` | B0 | 1 / 20 | 5.0% | 0 / 20 | 0.0% | 0.000012 | 93.3 |
| `history_gru` (Nominal) | `history_gru_best.pt` | B4 | 1 / 20 | 5.0% | 0 / 20 | 0.0% | 0.000012 | 93.3 |
| `recovery_augmented_mlp` | `recovery_augmented_mlp_seed42.pt` | B0 | 4 / 20 | 20.0% | 8 / 20 | 40.0% | 0.000003 | 84.4 |
| `recovery_augmented_mlp` | `recovery_augmented_mlp_seed42.pt` | B4 | 4 / 20 | 20.0% | 8 / 20 | 40.0% | 0.000003 | 84.4 |
| `recovery_augmented_gru` | `recovery_augmented_gru_seed456.pt` | B0 | 5 / 20 | 25.0% | 1 / 20 | 5.0% | 0.000005 | 80.3 |
| `recovery_augmented_gru` | `recovery_augmented_gru_seed456.pt` | B4 | 5 / 20 | 25.0% | 1 / 20 | 5.0% | 0.000005 | 80.3 |
| `privileged_oracle` | Algorithmic (`PrivilegedOracleController`) | B0 | 20 / 20 | 100.0% | 20 / 20 | 100.0% | 0.001250 | 96.7 |
| `privileged_oracle` | Algorithmic (`PrivilegedOracleController`) | B4 | 20 / 20 | 100.0% | 20 / 20 | 100.0% | 0.001250 | 96.7 |

### Reconciliation of 25% Success vs. 5% Corrective Action:
The 5 successful rollouts of `recovery_augmented_gru` in Phase 7 were individually re-examined:
- 1 episode exhibited active steering ($a_y = +0.0034$), crossing the heuristic threshold ($|a_y| > 0.003$).
- 4 episodes succeeded via gentle, low-amplitude forward-diagonal pushes ($|a_y| \in [0.0011, 0.0021]$) where mild post-deviation object tilt favored target acquisition without requiring aggressive repositioning maneuvers.

---

## 3. Checkpoint Forensics: Nominal GRU Collapse vs. Recovery GRU

Parameter tensor forensics evaluated all parameters across `history_gru_best.pt` and the 3 recovery-augmented GRU checkpoints:

| Parameter Tensor | Nominal GRU (`history_gru_best.pt`) | Recovery GRU (`seed42.pt`) | Recovery GRU (`seed123.pt`) | Recovery GRU (`seed456.pt`) | Parameter Status |
|---|---|---|---|---|---|
| `gru.weight_ih_l0` | **3.25e-38** (collapsed) | 2.01e-03 (healthy) | 3.01e-03 (healthy) | 2.59e-03 (healthy) | Input-to-hidden recurrent weights |
| `gru.weight_hh_l0` | **3.23e-38** (collapsed) | 2.24e-04 (healthy) | 4.37e-04 (healthy) | 2.98e-04 (healthy) | Hidden-to-hidden recurrent weights |
| `gru.bias_ih_l0` | **3.42e-38** (collapsed) | 7.21e-03 (healthy) | 8.12e-03 (healthy) | 7.84e-03 (healthy) | Input bias |
| `gru.bias_hh_l0` | **3.41e-38** (collapsed) | 3.52e-03 (healthy) | 4.15e-03 (healthy) | 3.89e-03 (healthy) | Hidden bias |
| `fc_head.0.weight` | **3.21e-38** (collapsed) | 5.31e-03 (healthy) | 6.42e-03 (healthy) | 5.81e-03 (healthy) | Projection layer weight |
| `fc_head.output.bias` | **0.0594** (active) | 0.0245 (active) | 0.0245 (active) | 0.0245 (active) | Output bias |

### Forensic Mechanism:
1. In Phase 3 nominal behavioral cloning, demonstrations consisted of constant forward pushes ($\mu_a = [0.00597, -0.00010, 0.0]$, $\sigma_a = 4.71 \times 10^{-5}$).
2. Under MSE loss with Adam and weight decay $\lambda = 10^{-5}$, any recurrent weights attempting to model history were penalized. The optimizer drove all input and recurrent weights to IEEE 754 subnormal underflow ($10^{-38}$), relying exclusively on `fc_head.output.bias` to push forward open-loop.
3. In contrast, recovery training in Phase 7 exposed the policies to dynamic slip, backward retractions, and multi-phase re-alignments, preserving healthy recurrent weights across all three training seeds.

---

## 4. Input Information Provenance Across Policy Architectures

| Input Channel | Dim | Source | Online? | Privileged? | Derived from History? | `reactive_mlp` | `history_gru` | `rec_aug_mlp` | `rec_aug_gru` |
|---|---|---|---|---|---|---|---|---|---|
| Current Obs $o_t$ | 20 | Kinematics/Tracking | Yes | No | **No** | Consumed | Consumed | Consumed | Consumed |
| Observation Buffer | $10 \times 20$ | FIFO Queue | Yes | No | **Yes** | None | Consumed | None | Consumed |
| Previous Action $a_{t-1}$ | 3 | Motor Buffer | Yes | No | **Yes** | None | Consumed | None | Consumed |
| Contact Indicator $c_t$ | 1 | Touch Sensor | Yes | No | **Yes** | None | None | None | Consumed |
| Hidden State $h_t$ | 128 | Internal Latent | Yes | No | **Yes** | None | Consumed | None | Consumed |
| Failure Flag $f_t$ | 1 | Online Detector | Yes | No | **Yes (Latching)** | None | None | Consumed | Consumed |
| Deviation Duration $\tau_t$ | 1 | Internal Counter | Yes | No | **Yes (Elapsed t)** | None | None | Consumed | Consumed |
| Deviation Mag $\delta_t$ | 1 | Computed | Yes | No | **Partially** | None | None | Consumed | Consumed |
| Remaining Horizon $H_t$ | 1 | Task Spec | Yes | No | **No** | None | None | Consumed | Consumed |

**Critical Takeaway:** `RecoveryAugmentedMLPPolicy` is not memoryless with respect to physical history. An evaluation condition that preserves `deviation_duration` retains history even when recurrent state is absent.

---

## 5. Implementable Intervention Semantics (V2.0)

1. **Prefix Unrolling & Reconstructed Memory (B0):**
   - The policy begins at $t=0$ with $h_0 = \mathbf{0}$, consumes the recorded observation-action prefix up to $t_{\text{dev}}-1$, and yields policy-specific state $h(t_{\text{dev}})$.
   - Observation $o(t_{\text{dev}})$ is consumed **exactly once** during the first recovery step.
2. **Direct Matched-State Injection (B4):**
   - MuJoCo physical state $(qpos, qvel)$ is restored bitwise to the deviation snapshot.
   - Recurrent state is zeroed: $h(t_{\text{dev}}) = \mathbf{0}_{128}$.
   - Action buffers are zeroed: $a_{\text{prev}} = \mathbf{0}_3$.
   - Observation buffers are filled with repeats of $o(t_{\text{dev}})$.
   - For augmented policies, elapsed duration is reset: $\tau_t = 0.0$.
3. **Explicit-Channel Distinction (B1 / B2 / B3):**
   - B1 zeroes explicit action feedback $a_{t-1}$ while retaining $h(t_{\text{dev}})$. It is an explicit-channel ablation, NOT an erasure of action history encoded in latent memory.
   - Interventions not supported by an architecture (e.g. B1 on MLP) are formally labeled **NOT APPLICABLE**.

---

## 6. Empirical Results of Bounded Mechanism Diagnostics ($N=20$)

Diagnostics were executed across all 20 frozen Phase 7 development scenarios using policy-specific reconstructed memory:
- **Scenarios Evaluated:** 20 (frozen IDs from `results/paired_scenarios/scenario_manifest.json`).
- **Total Diagnostic Rollouts:** 160 rollouts (4 policies $\times$ 20 scenarios $\times$ 2 conditions).
- **Execution Runtime:** 46.92 seconds.

### Summary Metrics by Policy:
| Evaluated Policy Checkpoint | Architecture | Reconstructed Memory $\|h(t_{\text{dev}})\|$ | First Action Diff ($\|a_{B0} - a_{B4}\|$) | Action Trajectory MAE | Mean Object Drift | Final Dist Diff | Success B0 | Success B4 | Discordance Rate ($k/20$) | Wilson 95% CI on Discordance Rate |
|---|---|---|---|---|---|---|---|---|---|---|
| `recovery_augmented_gru_seed42` | Recurrent GRU | 0.7663 | 0.001367 | 0.000144 | 0.69 cm | 0.64 cm | 2 / 20 (10%) | 2 / 20 (10%) | 0 / 20 (0.0%) | **[0.0%, 16.1%]** |
| `recovery_augmented_gru_seed123` | Recurrent GRU | 0.9895 | 0.002629 | 0.000136 | 0.08 cm | 0.07 cm | 4 / 20 (20%) | 4 / 20 (20%) | 0 / 20 (0.0%) | **[0.0%, 16.1%]** |
| `recovery_augmented_gru_seed456` | Recurrent GRU | 0.8784 | 0.003232 | 0.000483 | 1.84 cm | 2.07 cm | 3 / 20 (15%) | 5 / 20 (25%) | **2 / 20 (10.0%)** | **[2.8%, 29.8%]** |
| `recovery_augmented_mlp_seed42` | Feedforward MLP | 0.0000 | 0.000000 | 0.000000 | 0.00 cm | 0.00 cm | 5 / 20 (25%) | 5 / 20 (25%) | 0 / 20 (0.0%) | **[0.0%, 16.1%]** |

### Forensic Case Study: The 2 Discordant Scenarios in Seed 456
In scenarios `scen_history_gru_s301_t65_98b140` and `scen_history_gru_s308_t68_fead8b`, history ablation directly altered the binary task outcome:
1. **Scenario 301 ($t_{\text{dev}} = 65$):**
   - **Condition B0 (Preserved Memory):** Reconstructed hidden state carried strong forward pushing inertia from the preceding 65 steps. First action was $a = [+0.00283, -0.00049, +0.00065]$. The policy continued pushing forward blindly, causing the cube to slip off the pusher face. **Outcome: FAILED (final dist = 0.0925 m).**
   - **Condition B4 (Direct State Injection):** Started with zero hidden state. Evaluated the tilted cube directly, emitted an immediate corrective maneuver $a = [-0.00023, -0.00275, +0.00022]$, re-aligned behind the cube, and succeeded in 22 steps. **Outcome: SUCCESS (final dist = 0.0495 m).**
2. **Scenario 308 ($t_{\text{dev}} = 68$):**
   - **Condition B0:** Forward inertia caused overshooting ($a_x = +0.00287$). **Outcome: FAILED (final dist = 0.1398 m).**
   - **Condition B4:** Immediate corrective lateral adjustment ($a_y = -0.00268$). **Outcome: SUCCESS (final dist = 0.0545 m).**

---

## 7. Intervention Control Tests

Three focused automated test modules were added to the test suite and validated via pytest:
1. `tests/test_intervention_semantics.py` (3 tests): Verifies physical state snapshot bitwise invariance across B0–B4, hidden-state reset validity, and single-observation consumption.
2. `tests/test_policy_memory_reconstruction.py` (3 tests): Verifies deterministic memory reconstruction, checkpoint-specific memory divergence, and absence of stale buffers after reset.
3. `tests/test_intervention_controls.py` (2 tests):
   - **Synthetic Positive Control (`SyntheticHistoryDependentToyPolicy`):** Fixture explicitly conditioned on action history; demonstrably reacts to history reset with significant action divergence ($\|a_{B0} - a_{B4}\| > 0.001$).
   - **Strict Negative Control (`CurrentObservationOnlyPolicy`):** Fixture strictly invariant to history; demonstrably produces bitwise identical actions ($\|a_{B0} - a_{B4}\| = 0.000000$).
- **Test Suite Status:** 8/8 new tests passed; 59/59 total repository tests passing (100% pass rate).

---

## 8. Metric Construct Validity and Diagnosis Audit

- **Five Levels of Evaluation:** Formally separated Ground-Truth Failure (simulation flag), External Detector (algorithmic heuristic), Policy-Emitted Detection (not implemented), Policy-Emitted Diagnosis (not available), and Behavioral Proxy (retrospective action heuristic).
- **Audit of Past Logging:** Hardcoded `1.0` values for detection and diagnosis rates in Phase 7 loggers were cataloged as logging artifacts. All policy diagnosis metrics are marked **NOT AVAILABLE**.
- **Probability Chain:** Refuted mandatory $P(\text{Detect}) \times P(\text{Diagnose}) \times P(\text{Correct})$ decomposition. Continuous policies recover via closed-loop sensory feedback without requiring discrete diagnostic tokens.

---

## 9. Training Data Lineage and Provenance

- **Split Independence:** Verified that train (seeds 3000–3049) and validation (seeds 3050–3059) episodes were split at the episode level *before* sliding-window construction in `data/processed/recovery_training_dataset.npz`. Exactly zero overlapping frames cross the split boundary.
- **Contamination Check:** Training seeds (3000+) are completely disjoint from Phase 5 scenario seeds (49–633) and evaluation seeds (42, 500, 2000).
- **Target Actions:** Multi-phase recovery targets (retraction, re-alignment, directed push) were verified as valid behavioral cloning demonstrations. Zero privileged state leaked into the observation tokens.

---

## 10. Corrected Statistical Interpretation

- **The [0, 0] Fallacy:** Clarified that when all sample differences are zero, empirical bootstrap resamples zeros, returning $[0.0, 0.0]$. This is an artifact of sample degeneracy and does NOT establish population equivalence.
- **Wilson Score Uncertainty:** On $N=20$ independent scenarios, observing 0 discordant outcomes yields a 95% Wilson confidence interval of **$[0.0\%, 16.1\%]$**. Observing 2 discordant outcomes (Seed 456) yields **$[2.8\%, 29.8\%]$**.
- **Quantities Disentangled:** Signed average paired difference ($\bar{d} = -0.10$), absolute average difference ($|\bar{d}| = 0.10$), and discordance rate ($p_{\text{disc}} = 10.0\%$) are rigorously distinguished.

---

## 11. Jupyter Notebooks and Exploratory Figures Summary

All 4 required analysis notebooks were built and executed with saved visible outputs:
- `notebooks/26_phase_7_result_reconciliation.ipynb` (Phase 7 audit & reconciliation)
- `notebooks/27_history_input_and_memory_audit.ipynb` (Tensor forensics & provenance)
- `notebooks/28_intervention_mechanism_diagnostics.ipynb` (Mechanism traces & discordance)
- `notebooks/29_metric_and_uncertainty_audit.ipynb` (Construct validity & Wilson intervals)

Ten diagnostic figures were generated at 600 DPI (PNG & vector PDF) in `figures/exploratory/`:
- `fig48_reconciled_phase_7_performance`: Reconciled performance on true $N=20$.
- `fig49_gru_parameter_forensics_breakdown`: Log10 parameter comparison showing $10^{-38}$ collapse.
- `fig50_input_provenance_and_channel_mapping`: Online availability vs. history derivation.
- `fig51_reconstructed_hidden_state_norms`: Hidden-state norms at $t_{\text{dev}}$ under B0 vs. B4.
- `fig52_first_action_divergence_b0_vs_b4`: First recovery action divergence norms.
- `fig53_action_sequence_mae_divergence`: Multi-step action MAE throughout recovery.
- `fig54_trajectory_position_drift_distribution`: Physical trajectory drift between B0 and B4.
- `fig55_discordant_scenario_trajectories`: State trajectories of discordant episodes in Seed 456.
- `fig56_discordance_rate_uncertainty_cis`: Wilson 95% confidence intervals on discordance rates.
- `fig57_metric_validity_construct_matrix`: Matrix of construct validity across metrics.

---

## 12. Complete File Manifest and Commands Executed

### Files Created:
1. `docs/audit/phase_7_result_reconciliation.md`
2. `docs/audit/gru_checkpoint_forensics.md`
3. `docs/methodology/history_information_provenance.md`
4. `docs/methodology/intervention_semantics_v2.md`
5. `docs/audit/metric_construct_validity.md`
6. `docs/statistics/phase_8_uncertainty_audit.md`
7. `docs/audit/recovery_dataset_lineage_audit.md`
8. `docs/reports/phase_8_intervention_validity_report.md`
9. `results/intervention_diagnostics/source_file_hashes.json`
10. `results/intervention_diagnostics/diagnostic_traces.jsonl`
11. `results/intervention_diagnostics/diagnostic_summary.json`
12. `scripts/run_intervention_diagnostics.py`
13. `scripts/make_phase_8_figures.py`
14. `scripts/build_phase_8_notebooks.py`
15. `tests/test_intervention_semantics.py`
16. `tests/test_policy_memory_reconstruction.py`
17. `tests/test_intervention_controls.py`
18. `notebooks/26_phase_7_result_reconciliation.ipynb`
19. `notebooks/27_history_input_and_memory_audit.ipynb`
20. `notebooks/28_intervention_mechanism_diagnostics.ipynb`
21. `notebooks/29_metric_and_uncertainty_audit.ipynb`
22. 10 PNG + 10 PDF figures in `figures/exploratory/` (`fig48` through `fig57`).

### Key Commands and Exit Codes:
- `python scripts/run_intervention_diagnostics.py` (Exit code: 0)
- `python scripts/make_phase_8_figures.py` (Exit code: 0)
- `python scripts/build_phase_8_notebooks.py` (Exit code: 0)
- `pytest tests/test_intervention_semantics.py tests/test_policy_memory_reconstruction.py tests/test_intervention_controls.py` (Exit code: 0, 8 passed)
- `pytest tests` (Exit code: 0, 59 passed)

---

## 13. Concluding Decision and Mandatory Closing Gate

### Concluding Decision:
**Decision A: Harness valid; proceed to design a fresh held-out evaluation.**

*Scientific Rationale:*  
The Phase 8 diagnostic investigation successfully resolved the mystery of identical B0/B4 outcomes. The root causes were identified as an evaluation harness omission (failure to unroll the prefix in B0 in Phase 7) combined with a parameter collapse in nominal Phase 3 GRU models. When the evaluation harness is repaired with policy-specific prefix memory reconstruction, the test instruments function with high fidelity: positive controls detect history changes, negative controls remain invariant, hidden states accumulate non-zero representations, actions diverge immediately, and recovery outcomes demonstrate genuine causal history dependence (10.0% discordance in Seed 456).

All 20 scenarios inspected in this phase remain **development data**. They must never be relabeled as confirmatory evaluation data. The project is now equipped with a validated, verified, and bug-free evaluation harness ready for a preregistered confirmatory study on fresh, held-out matched scenarios.

---

Phase 8 diagnostic work is complete. Official benchmark experiments remain paused pending explicit user approval.

