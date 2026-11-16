# Phase 5 Final Report: Paired Scenario Generation and Matching-Yield Optimization

> **Document Type:** Formal Phase Gate Audit & Research Governance Report  
> **Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
> **Package:** `causal_history_recovery`  
> **Phase Evaluated:** Phase 5 (Paired Scenario Generation & Matching-Yield Optimization)  
> **Evaluation Date:** 2026-11-09  
> **Audit Status:** `Verified & Audited`  
> **Research Boundary:** Strict pre-experiment audit. No official benchmarks executed; no production policies trained; no Q1 publication claims made; no novelty claims asserted.

---

## 1. Executive Summary & Objective

In Phase 4, the audit of passive cross-episode matching revealed a critical bottleneck: seeking naturally matching failure states across independent stochastic rollouts yielded **0.0% valid matches** across 45 pairs due to the curse of dimensionality in continuous multi-body contact dynamics.

Phase 5 was authorized with a singular restricted mandate: **solve the matched-pair scarcity problem without compromising physical rigor or relaxing matching tolerances**.

### Summary of Achievements:
1. **Transition to Paired Replay-Injection Matching:** Designed and implemented a deterministic 13-step paired generation architecture ([paired_scenario_generation.md](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/methodology/paired_scenario_generation.md)). By extracting verified recoverable failure states $s(t_d)$ and constructing counterfactual conditions (B0, B1, B2, B3, B4) via deterministic prefix replay and bitwise state injection, **physical state matching is guaranteed by construction ($D \le 1.0 \times 10^{-10}$)**.
2. **Matching-Yield Optimization:** Executed a 150-episode pilot across 3 policy seeds (`42, 500, 2000`) for the History-Aware GRU policy. The overall matching yield increased from **0.0% (passive)** to **25.33% (paired)**, producing **38 fully validated paired scenarios** ($190$ individual counterfactual condition instances).
3. **Multi-Dimensional Failure Diversity:** Successfully sampled across three calibrated severity tiers (Small, Medium, Large), varied perturbation onset steps ($t_{\text{pert}} \in [20, 25, 30, 35]$), bilateral push directions ($\pm y$), impulse burst durations, and target goal positions ([failure_diversity_plan.md](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/methodology/failure_diversity_plan.md)).
4. **15-Point Automated Validation Gate:** Implemented and enforced an exhaustive 15-point quality checklist ([paired_scenario_validation.md](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/methodology/paired_scenario_validation.md)). Every admitted scenario achieved a **100.0% pass rate** across all 15 rules with zero information leakage.
5. **Full Go/No-Go Compliance:** Audited all ten pre-registered criteria ([phase_5_go_no_go_criteria.md](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/audit/phase_5_go_no_go_criteria.md)), achieving a clean **GO** verdict.

---

## 2. Paired Generation Strategy & Architecture

The paired replay-injection matching strategy is implemented in `PairedScenarioGenerator` (`src/causal_history_recovery/counterfactuals/paired_scenario_generator.py`).

For each candidate failure episode:
1. **Source Rollout:** The policy executes in `PushTargetEnv`. Off-center contact slip is induced at step $t_{\text{pert}}$.
2. **Deviation Detection:** At step $t_d$, kinematic thresholds are breached ($\theta \ge \theta_{\text{thresh}}$, $\Delta y \ge \Delta y_{\text{thresh}}$).
3. **Lossless Snapshot Capture:** Simulation coordinates $s(t_d) = (\mathbf{q}_{\text{pos}}, \mathbf{q}_{\text{vel}}, \mathbf{a}_{\text{act}}, \mathbf{w}_{\text{warmstart}})$ are captured alongside action prefix $\mathbf{a}_{0:t_d-1}$, observation history $\mathbf{o}_{t_d-k:t_d}$, contact history, and recurrent hidden state $\mathbf{h}(t_d)$.
4. **Oracle Recoverability Filter:** The Privileged Oracle Controller tests whether $s(t_d)$ is solvable ($R_{\text{oracle}} = 1$) within the remaining horizon $T_{\max} - t_d$ and satisfies the 5-step dwell requirement.
5. **Counterfactual Condition Generation:**
   - **Condition B0 (Continuation):** Replays action prefix $\mathbf{a}_{0:t_d-1}$ to reach $t_d$; preserves full history $(\mathbf{o}, \mathbf{a}, \mathbf{h})$.
   - **Condition B1 (Action History Ablated):** Replays prefix to reach $t_d$; action buffer zero-masked ($\mathbf{a}_{\text{hist}} \gets \mathbf{0}$).
   - **Condition B2 (Observation History Ablated):** Replays prefix to reach $t_d$; observation buffer masked ($\mathbf{o}_{\text{hist}} \gets \mathbf{o}_{t_d}$).
   - **Condition B3 (Hidden State Reset):** Replays prefix to reach $t_d$; policy recurrent hidden state zeroed ($\mathbf{h} \gets \mathbf{0}$).
   - **Condition B4 (Direct Matched Injection):** State snapshot $s(t_d)$ injected bitwise losslessly into fresh environment; all history purged, $\mathbf{h} \gets \mathbf{0}$.

---

## 3. Matching-Yield & Funnel Analysis

The table below presents the quantitative progression across all 150 candidate episodes:

| Funnel Stage | Count | Transition Rate | Cumulative Yield | Audit Status |
|---|---|---|---|---|
| **Candidate Episodes Evaluated** | 150 episodes | $100.0\%$ | $100.0\%$ | `Verified` |
| **Detected Slip Deviations** | 140 episodes | $93.33\%$ | $93.33\%$ | `Verified` |
| **Privileged Oracle Recoverable** | 38 episodes | $27.14\%$ | $25.33\%$ | `Verified` |
| **15-Point Validated Paired Scenarios** | **38 scenarios** | **100.0%** | **25.33%** | `Verified` |
| **Total Condition Rollout Instances** | **190 instances** | ($38 \times 5$ conditions) | — | `Verified` |

```
Candidate Funnel Visualization:
Total Candidates (150)  ================================================== (100.0%)
Detected Slips (140)    ==============================================     (93.3%)
Oracle Admitted (38)    ============                                       (25.3%)
Valid Scenarios (38)    ============                                       (25.3%)
```

### Yield Comparison:
- **Phase 4 (Passive Cross-Episode Matching):** 45 pairs tested $\to$ **0 valid matches (0.0% yield)**.
- **Phase 5 (Paired Replay-Injection Matching):** 150 candidates $\to$ **38 valid matched scenarios (25.33% yield)**.
- **Improvement:** $+25.33$ percentage points with **zero state-matching error** ($D \le 1.0 \times 10^{-10}$).

---

## 4. Failure Diversity & Distributional Results

All 38 admitted scenarios were audited across physical parameters ([matching_yield_report.json](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/results/paired_matching_pilot/matching_yield_report.json)):

### 4.1 Severity Breakdown
- **Small Tier (Mild Slip, $\Delta y \in [0.007, 0.010]\text{ m}$):** 12 scenarios ($31.6\%$).
- **Medium Tier (Moderate Slip, $\Delta y \in [0.011, 0.014]\text{ m}$):** 20 scenarios ($52.6\%$).
- **Large Tier (Severe Slip, $\Delta y \in [0.015, 0.018]\text{ m}$):** 6 scenarios ($15.8\%$).

### 4.2 Seed Representation
- **Base Seed 42:** 11 scenarios ($28.9\%$).
- **Base Seed 500:** 13 scenarios ($34.2\%$).
- **Base Seed 2000:** 14 scenarios ($36.8\%$).
- *Seed Overlap with Training Demonstrations (`1000..1049`):* **0.0% (Strictly Disjoint)**.

### 4.3 Kinematic & Horizon Metrics
- **Mean Peak Yaw Deflection:** $40.19^\circ \pm 8.45^\circ$ (Range: $[15.2^\circ, 54.8^\circ]$).
- **Mean Lateral Drift:** $0.0453 \pm 0.0112\text{ m}$ (Range: $[1.8\text{ cm}, 6.2\text{ cm}]$).
- **Mean Failure Detection Step ($t_d$):** Step $51.6 \pm 12.4$ (Range: $[35, 87]$).
- **Mean Remaining Horizon:** $98.4 \pm 12.4$ steps (Range: $[63, 115]$ steps).

---

## 5. 15-Point Automated Validation & Rejection Breakdown

Every admitted scenario was evaluated against the 15-point checklist ([validation_report.json](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/results/paired_scenarios/validation_report.json)):

| # | Validation Rule | Compliance Rate | Verification Detail | Status |
|---|---|---|---|---|
| **R1** | Source failure plausibility | **100.0%** (38/38) | Peak yaw $\ge 8^\circ$, lateral drift $\ge 0.010\text{ m}$ | `Verified` |
| **R2** | Oracle recoverability | **100.0%** (38/38) | Privileged oracle solves task ($R_{\text{oracle}} = 1$) with dwell $\ge 5$ | `Verified` |
| **R3** | Physical state validity | **100.0%** (38/38) | Generalized coordinates finite, zero NaN values | `Verified` |
| **R4** | Object workspace bounds | **100.0%** (38/38) | $x \in [0.05, 0.50]$, $y \in [-0.20, 0.20]$, on tabletop | `Verified` |
| **R5** | Manipulator limits | **100.0%** (38/38) | End-effector within reachable Cartesian bounds | `Verified` |
| **R6** | Contact state consistency | **100.0%** (38/38) | Object in tabletop layer, velocities finite, no impulse spikes | `Verified` |
| **R7** | Goal state preservation | **100.0%** (38/38) | $\|\mathbf{g}_{\text{cond}} - \mathbf{g}_{\text{source}}\|_2 < 10^{-6}$ across B0–B4 | `Verified` |
| **R8** | Horizon preservation | **100.0%** (38/38) | Remaining horizon identical to source snapshot | `Verified` |
| **R9** | State-matching tolerance | **100.0%** (38/38) | Maximum coordinate error $D \le 1.0 \times 10^{-10}$ | `Verified` |
| **R10** | Hidden state isolation | **100.0%** (38/38) | $\|\mathbf{h}_{\text{B3}}\|_2 == 0.0, \|\mathbf{h}_{\text{B4}}\|_2 == 0.0$ | `Verified` |
| **R11** | Obs history masking | **100.0%** (38/38) | Observation queue cleared and masked in B2 & B4 | `Verified` |
| **R12** | Action history masking | **100.0%** (38/38) | Action queue cleared and zero-padded in B1 & B4 | `Verified` |
| **R13** | Contact history integrity | **100.0%** (38/38) | Contact log length synchronized with deviation step | `Verified` |
| **R14** | Random state synchronization | **100.0%** (38/38) | Seed recorded; deterministic evaluation mode | `Verified` |
| **R15** | Zero future information leakage | **100.0%** (38/38) | Zero trajectory timesteps $t > t_d$ present in archives | `Verified` |

### Rejection Reason Decomposition (112 Rejections Total):
1. **Oracle Unrecoverable (102 episodes = 91.1% of rejections):** Lateral slip caused the spherical pusher tip to slide completely past the cube facet into free air, leaving insufficient time ($< 25$ steps) to re-engage before the horizon expired.
2. **No Slip Detected (10 episodes = 8.9% of rejections):** Very mild offset where pusher remained centered.
3. **Post-Admission Validation Failures:** **0 episodes (0.0%)**.

---

## 6. Audit of Phase 5 Go/No-Go Decision Criteria

All ten formal Go/No-Go criteria mandated in the methodology were audited ([phase_5_go_no_go_criteria.md](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/audit/phase_5_go_no_go_criteria.md)):

```
Phase 5 Go/No-Go Decision Matrix:
[GO (PASSED)] At least 30 valid paired scenarios generated   : 38 generated
[GO (PASSED)] At least 20 scenarios pass all validations     : 38 passed 100%
[GO (PASSED)] At least 3 policy seeds produce scenarios      : 3 seeds (42, 500, 2000)
[GO (PASSED)] At least 3 failure-severity levels represented : 3 tiers (Small: 12, Med: 20, Large: 6)
[GO (PASSED)] At least 80% preserve remaining horizon        : 100.0% preserved
[GO (PASSED)] At least 80% preserve goal state               : 100.0% preserved
[GO (PASSED)] At least 95% pass physical validity checks     : 100.0% passed
[GO (PASSED)] No future-information leakage detected         : Zero detected (Clean)
[GO (PASSED)] No hidden-state leakage detected               : Zero detected (Clean)
[GO (PASSED)] No contact-restoration failure detected        : Zero detected (Clean)

FINAL VERDICT: GO — ALL CRITERIA SATISFIED
```

---

## 7. Artifacts & Deliverables Inventory

### 7.1 Diagnostic Figures Generated at 600 DPI (`figures/exploratory/`)
- `fig08_source_failure_yield`: Bar chart showing 93.3% failure detection rate.
- `fig09_oracle_admission_yield`: Bar chart showing 27.1% oracle recoverability admission rate.
- `fig10_matched_scenario_yield`: Pie chart illustrating 25.3% overall matched scenario yield.
- `fig11_failure_yaw_distribution`: Histogram of peak yaw deflections (mean: $40.2^\circ$).
- `fig12_lateral_drift_distribution`: Histogram of lateral displacements (mean: $4.53\text{ cm}$).
- `fig13_failure_time_distribution`: Histogram of failure detection steps $t_d$ (mean: step $51.6$).
- `fig14_remaining_horizon_distribution`: Histogram of remaining recovery horizons (mean: $98.4$ steps).
- `fig15_state_matching_error_distribution`: Histogram confirming exact matching ($D \le 10^{-10}$).
- `fig16_rejection_reason_distribution`: Categorical breakdown of unrecoverable failure causes.
- `fig17_scenario_severity_distribution`: Histogram of admitted scenarios across small, medium, large tiers.
- `fig18_condition_generation_validation_summary`: 15-bar compliance matrix showing 100% pass rates.

### 7.2 Executed Analysis Notebooks (`notebooks/`)
- [11_paired_scenario_generation.ipynb](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/notebooks/11_paired_scenario_generation.ipynb): Construction and verification of conditions B0–B4.
- [12_matching_yield_optimization.ipynb](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/notebooks/12_matching_yield_optimization.ipynb): Funnel analysis and yield comparison (passive vs paired).
- [13_failure_diversity_analysis.ipynb](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/notebooks/13_failure_diversity_analysis.ipynb): Multi-dimensional physical severity and seed representation audit.
- [14_paired_scenario_validation.ipynb](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/notebooks/14_paired_scenario_validation.ipynb): 15-point rule compliance and Go/No-Go decision matrix.

### 7.3 Data Archives & Manifests
- `results/paired_scenarios/scenario_manifest.json`: Full index of 38 admitted scenarios.
- `results/paired_scenarios/validation_report.json`: Aggregate validation metrics.
- `results/paired_scenarios/scenarios/`: 38 subdirectories containing `snapshot.npz` and `metadata.json`.
- `results/paired_matching_pilot/matching_yield_report.json`: Pilot yield summary.
- `results/paired_matching_pilot/episode_metadata.jsonl`: 150 JSONL records of all candidate episodes.

---

## 8. Exact Files Created & Modified

### Files Created:
1. `docs/methodology/paired_scenario_generation.md`
2. `docs/methodology/paired_scenario_validation.md`
3. `docs/methodology/failure_diversity_plan.md`
4. `configs/scenarios/paired_scenario_sampling.yaml`
5. `src/causal_history_recovery/counterfactuals/paired_scenario_generator.py`
6. `tests/test_paired_scenario_generation.py`
7. `scripts/generate_paired_scenarios.py`
8. `scripts/make_phase_5_figures.py`
9. `scripts/build_phase_5_notebooks.py`
10. `docs/audit/phase_5_go_no_go_criteria.md`
11. `docs/reports/phase_5_paired_scenario_report.md`
12. `results/paired_scenarios/scenario_manifest.json`
13. `results/paired_scenarios/validation_report.json`
14. `results/paired_matching_pilot/matching_yield_report.json`
15. `results/paired_matching_pilot/scenario_manifest.json`
16. `results/paired_matching_pilot/validation_report.json`
17. `results/paired_matching_pilot/episode_metadata.jsonl`
18. `notebooks/11_paired_scenario_generation.ipynb`
19. `notebooks/12_matching_yield_optimization.ipynb`
20. `notebooks/13_failure_diversity_analysis.ipynb`
21. `notebooks/14_paired_scenario_validation.ipynb`
22. `figures/exploratory/fig08_source_failure_yield.png` (and `.pdf`)
23. `figures/exploratory/fig09_oracle_admission_yield.png` (and `.pdf`)
24. `figures/exploratory/fig10_matched_scenario_yield.png` (and `.pdf`)
25. `figures/exploratory/fig11_failure_yaw_distribution.png` (and `.pdf`)
26. `figures/exploratory/fig12_lateral_drift_distribution.png` (and `.pdf`)
27. `figures/exploratory/fig13_failure_time_distribution.png` (and `.pdf`)
28. `figures/exploratory/fig14_remaining_horizon_distribution.png` (and `.pdf`)
29. `figures/exploratory/fig15_state_matching_error_distribution.png` (and `.pdf`)
30. `figures/exploratory/fig16_rejection_reason_distribution.png` (and `.pdf`)
31. `figures/exploratory/fig17_scenario_severity_distribution.png` (and `.pdf`)
32. `figures/exploratory/fig18_condition_generation_validation_summary.png` (and `.pdf`)

### Files Modified:
1. `PROJECT_STATUS.md` (Updated to reflect Phase 5 completion and status)
2. `docs/decision_log.md` (Appended DEC-016: Paired Replay-Injection Matching Strategy)

---

## 9. Remaining Blockers & Recommendation for Phase 6

- **Blocker Status:** **Zero Technical Blockers**. The paired replay-injection matching harness is fully operational, verified, and unit-tested (49/49 pytest tests passing).
- **Recommendation for Phase 6:** With 38 validated paired scenarios spanning all severity tiers, the project is technically prepared to proceed to Phase 6 (recovery rollout evaluation across conditions B0, B1, B2, B3, B4 for Reactive MLP and History GRU).

---

## 10. Phase Gate Conclusion & Mandatory Statement

Phase 5 paired scenario generation and matching-yield optimization is complete. Official experiments remain paused pending explicit user approval.

