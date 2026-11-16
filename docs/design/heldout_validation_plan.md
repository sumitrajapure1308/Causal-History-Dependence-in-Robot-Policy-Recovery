# Held-Out Validation Plan: Confirmatory Evaluation of Causal-History Dependence

**Document ID:** `docs/design/heldout_validation_plan.md`  
**Status:** PROPOSED VALIDATION PLAN (UNEXECUTED)  
**Project:** Causal-History Dependence in Robot Policy Recovery  
**Directory:** `causal-history-recovery/`  
**Mandate:** Establish an airtight, pre-registered held-out validation protocol to evaluate causal history dependence without data leakage, post-hoc threshold tuning, or conflation with development cohorts.

---

## 1. Existing Scenario Inventory

Across the lifecycle of the repository, a total of 383 scenarios and demonstration trajectories were generated across distinct development, exploratory, and confirmatory phases:

| Phase / Artifact | Seed Range | Count ($N$) | Environment / Task | Purpose & Exposure Level | Storage Location |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Training Demonstrations** | 3000–3059 | 60 | Task 1 Cube ($\mu=0.40$) | Behavioral cloning dataset used to train recovery-augmented policies. **Exposed to model weights.** | `data/processed/recovery_training_dataset.npz` |
| **Phase 5 Paired Pilot** | 1000–1150 | 38 | Task 1 Cube ($\mu=0.40$) | Initial state matching validation and feasibility pilot. **Exposed to exploratory analysis.** | `results/paired_scenarios/` |
| **Phase 7 Recovery Pilot** | 2000–2050 | 20 | Task 1 Cube ($\mu=0.40$) | Exploratory verification of recovery controller behavior. **Exposed to exploratory analysis.** | `results/pilot_recovery/` |
| **Phase 9 Held-Out Pilot** | 5000–5234 | 45 | Task 1 Cube ($\mu=0.40$) | Exploratory 5-condition pilot evaluation. **Exposed to exploratory analysis.** | `results/heldout_pilot/` |
| **Phase 10 Second Task Pilot**| 9001–9050 | 30 | Task 2 Puck ($\mu=0.35$) | Tuning puck geometry, friction, and second-task controller. **Exposed to parameter tuning.** | `results/phase_10/second_task_pilot/` |
| **Phase 11 Benchmark Smoke** | 9901–9920 | 20 | Task 1 & 2 Combined | Pre-benchmark pipeline validation. **Exposed to pipeline testing.** | `results/phase_11/` |
| **Stage C Primary Benchmark**| 10001–13050| 200 | Tasks 1 & 2 ($50 \times 4$ cells) | Confirmatory 12,000-rollout benchmark analyzed in Phases 12–38. **Exposed to primary results analysis.** | `results/phase_12_stage_c/scenarios/` |

---

## 2. Development Scenarios

All scenarios listed above (seeds 1000 through 13050) are classified as **Development and Primary Benchmark Cohorts**:

1. **Model Training Exposure (Seeds 3000–3059):** Policies `recovery_augmented_mlp` and `recovery_augmented_gru` computed parameter gradients over these trajectories.
2. **Hyperparameter and Threshold Calibration (Seeds 1000–2050, 9001–9050):** The physical deviation thresholds (yaw $\ge 15^\circ$, drift $\ge 0.020\text{ m}$, air gap $\ge 0.020\text{ m}$) and matching tolerance ($D \le 10^{-10}\text{ m}$) were verified and calibrated on these runs.
3. **Primary Benchmark Exposure (Seeds 10001–13050):** The 200 scenarios of Stage C were extensively evaluated, and their empirical recovery rates (1.0% to 4.5%) are already documented.

**Methodological Constraint:** Because the empirical findings of the 200 Stage C scenarios are known to the investigators, running further analyses or threshold calibrations on them cannot be considered blinded or held-out. A completely segregated seed cohort must be provisioned.

---

## 3. Held-Out Scenarios

A fresh, virgin cohort of **$N = 200$ strictly held-out scenarios** is established in a quarantined seed domain ($S_{\text{heldout}} \ge 20000$):

| Benchmark Cell | Task ID | Object Geometry | Surface Friction | Failure Mode | Reserved Seed Range | Target Admitted ($N$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cell 1** | `task1_cube` | Cube ($0.05\text{ m}$) | $\mu = 0.40$ | Rotational Slip | 20001–20250 | 50 |
| **Cell 2** | `task1_cube` | Cube ($0.05\text{ m}$) | $\mu = 0.40$ | Contact Loss | 21001–21250 | 50 |
| **Cell 3** | `task2_puck` | Cylinder ($r=0.035\text{ m}$) | $\mu = 0.35$ | Rotational Slip | 22001–22250 | 50 |
| **Cell 4** | `task2_puck` | Cylinder ($r=0.035\text{ m}$) | $\mu = 0.35$ | Contact Loss | 23001–23250 | 50 |

### Pre-Admission Criteria
Every candidate scenario must satisfy three automated admittance gates prior to inclusion in the held-out manifest:
1. **Perturbation Trigger:** Verified physical deviation detected at $t_{\text{perturb}}$ (rotational yaw $|\psi| \ge 15^\circ$, lateral drift $\ge 0.020\text{ m}$, or contact air gap $\ge 0.020\text{ m}$).
2. **Oracle Recoverability:** The privileged oracle controller must independently solve the scenario from snapshot $S_{\text{fail}}$ to guarantee that failure is physically recoverable.
3. **Horizon Sufficiency:** Remaining task horizon at failure must satisfy $H_{\text{rem}} \ge 60$ timesteps to ensure ample physical time for recovery maneuvers.

---

## 4. Task-Level and Scenario-Level Splits

The validation plan enforces a dual-hierarchy evaluation split:

```
                            [Evaluation Splits]
                                     |
         +---------------------------+---------------------------+
         |                                                       |
[Scenario-Level Split]                                  [Task-Level Split]
(Within-Domain Generalization)                          (Cross-Domain Generalization)
- Fresh Initial Poses (qpos jitter)                     - Task 1 -> Task 2 Transfer
- Perturbation Step Variation (t_p in [20, 28])         - Distinct Geometry (Cube vs Cylinder)
- Disjoint Noise Seeds (20000+)                         - Distinct Contact Friction (0.40 vs 0.35)
- Same Contact Physics & Kinematics                     - Distinct Push Axis (Straight vs Diagonal)
```

1. **Scenario-Level Split (Within-Domain Generalization):** Evaluates whether the policy's recovery behavior generalizes across stochastic variations in initial workpiece placement, pusher engagement offsets, and perturbation onset timings within known physical models.
2. **Task-Level Split (Cross-Domain Generalization):** Evaluates zero-shot transfer across environments. Policies trained exclusively on Task 1 demonstrations are tested on Task 2 scenarios, isolating how geometric curvature (planar square vs. cylindrical manifold) impacts recovery and history dependence.

---

## 5. Policy Splits

The evaluation suite tests fixed, immutable policy checkpoints with zero gradient updates or architecture adjustments:

| Policy Identifier | Model Architecture | Training Source | Recurrent Memory | Role in Validation |
| :--- | :--- | :--- | :--- | :--- |
| **`reactive_mlp`** | 2-layer MLP (64-64) | Baseline PPO / BC | Stateless ($h = \emptyset$) | Stateless Control Baseline |
| **`history_gru`** | GRU (128-d) + MLP head | Baseline BC | Active Recurrent ($h \in \mathbb{R}^{128}$) | Standard Recurrent Baseline |
| **`recovery_augmented_mlp`** | 2-layer MLP + Causal Feat | Multi-phase Recovery BC | Stateless ($h = \emptyset$) | Recovery-Specialized Stateless |
| **`recovery_augmented_gru`** | GRU (128-d) + Causal Feat | Multi-phase Recovery BC | Active Recurrent ($h \in \mathbb{R}^{128}$) | Recovery-Specialized Recurrent |
| **`privileged_oracle`** | Analytical State Machine | Privileged State Access | Analytical State | Algorithmic Upper Bound |

- **Replicate Partitioning:** For `recovery_augmented_mlp` and `recovery_augmented_gru`, all three training seed replicates (seeds 42, 123, 456) must be evaluated to compute inter-training-run variance.

---

## 6. Seed Policy

The validation protocol establishes an arithmetic, non-overlapping seed hierarchy:

```
[0000 - 0999]: Unit tests & smoke tests (e.g., seed 42, 77, 88, 123)
[1000 - 1999]: Phase 5 paired pilot scenarios
[2000 - 2999]: Phase 7 recovery capability scenarios
[3000 - 3999]: Offline training demonstrations (dataset generation)
[5000 - 5999]: Phase 9 pilot evaluation scenarios
[7001 - 7003]: Post-intervention policy rollout evaluation seeds (fixed)
[9000 - 9999]: Phase 10 & 11 environment calibration & smoke scenarios
[10000 - 13999]: Stage C Primary Benchmark scenarios (Cells 1-4)
[20000 - 23999]: RESERVED HELD-OUT VALIDATION SCENARIOS (Cells 1-4)
```

- **Rollout Determinism:** Post-intervention execution uses triplicated evaluation seeds (7001, 7002, 7003) for stochastic action noise, enabling direct paired comparisons across conditions.

---

## 7. Matching Criteria

Every held-out scenario must enforce the verified bitwise matched-state criteria established in Phase 12 and Task 1B:

1. **Generalized Coordinate Match:**
   $$\|q_{\text{pos}}^{\text{replay}} - q_{\text{pos}}^{\text{inject}}\|_{\infty} \le 10^{-10}\text{ m}$$
2. **Generalized Velocity Match:**
   $$\|q_{\text{vel}}^{\text{replay}} - q_{\text{vel}}^{\text{inject}}\|_{\infty} \le 10^{-10}\text{ m/s}$$
3. **Dynamic State Cache Match:** Bitwise preservation of `qacc_warmstart`, `qfrc_applied`, `xfrc_applied`, and actuator controls `ctrl`.
4. **Horizon Invariance:** Remaining task horizon $H_{\text{rem}}$ must be strictly equal between replay and injection conditions:
   $$H_{\text{rem}}(\text{replay}) \equiv H_{\text{rem}}(\text{inject})$$
5. **Rejection Rule:** Any candidate run with matching error $D > 10^{-10}\text{ m}$ is rejected and flagged as an infrastructure fault.

---

## 8. Evaluation Conditions

All held-out evaluations execute the four canonical decoupled memory conditions formalized in Task 1B:

| Condition Code | Canonical Identifier | Environment State | Policy Memory State | Causal Question Addressed |
| :--- | :--- | :--- | :--- | :--- |
| **Cond A** | `M_REPLAY_PRESERVED` | Prefix Replay ($0 \to t_{\text{fail}}$) | Unrolled ($h = h(t_{\text{fail}})$) | Combined physical + memory history baseline |
| **Cond B** | `M_INJECT_PRESERVED` | Matched Injection ($D \le 10^{-10}$) | Injected ($h = h(t_{\text{fail}})$) | **Physical ablation with isolated memory preservation** |
| **Cond C** | `M_INJECT_RESET` | Matched Injection ($D \le 10^{-10}$) | Reset ($h = \mathbf{0}$) | **Dual physical and memory ablation** |
| **Cond D** | `M_INJECT_ALTERNATIVE`| Matched Injection ($D \le 10^{-10}$) | Alternative ($h = -h_{\text{nom}}$) | Control for memory incompatibility / perturbation |

---

## 9. Primary Outcome Metric

The validation protocol evaluates two primary causal contrast metrics:

### Metric 1: Causal Physical History Effect ($\Delta \text{SR}_{\text{physical}}$)
$$\Delta \text{SR}_{\text{physical}} = \text{SR}(\text{M\_REPLAY\_PRESERVED}) - \text{SR}(\text{M\_INJECT\_PRESERVED})$$
*Holding policy recurrent memory constant ($h = h(t_{\text{fail}})$), does physical trajectory history alter recovery success?*

### Metric 2: Policy Memory Initialization Effect ($\Delta \text{SR}_{\text{memory}}$)
$$\Delta \text{SR}_{\text{memory}} = \text{SR}(\text{M\_INJECT\_PRESERVED}) - \text{SR}(\text{M\_INJECT\_RESET})$$
*Holding the physical environment state constant ($D \le 10^{-10}\text{ m}$), does policy hidden memory alter recovery success?*

Secondary metrics:
- **Mean Recovery Time ($T_{\text{rec}}$):** Steps to stable target dwell.
- **Terminal Goal Error ($d_{\text{goal}}$):** Final Euclidean distance to target.
- **Trajectory Divergence:** Mean Euclidean action difference over the first 5 recovery steps.

---

## 10. Sample-Size Target and Power Analysis

- **Scenario Cohort:** $N = 200$ fresh held-out scenarios (50 per cell $\times$ 4 cells).
- **Conditions:** 4 conditions (A, B, C, D).
- **Evaluation Seeds:** 3 seeds per scenario (7001, 7002, 7003).
- **Policy Checkpoints:** 8 checkpoints (1 reactive MLP, 1 history GRU, 3 recovery MLP replicates, 3 recovery GRU replicates).
- **Total Rollouts:**
  $$N_{\text{total}} = 200 \text{ scenarios} \times 4 \text{ conditions} \times 8 \text{ policies} \times 3 \text{ seeds} = 19,200 \text{ rollouts}$$
- **Statistical Power:** For paired McNemar testing on 200 scenarios at significance level $\alpha = 0.01$, the design achieves statistical power $1 - \beta \ge 0.95$ to detect a minimal effect size $\Delta \text{SR} \ge 0.05$.

---

## 11. Statistical Analysis Plan

1. **Paired Hypothesis Testing:** Two-sided paired McNemar tests for binary recovery success differences on matched scenario pairs.
2. **Confidence Intervals:** Exact Wilson score 95% confidence intervals for all binomial success rates.
3. **Mixed-Effects Modeling:** Generalized linear mixed-effects model (GLMM) with logit link:
   $$\text{logit}(P(Y_{ij} = 1)) = \beta_0 + \beta_1 \text{Cond}_{ij} + \beta_2 \text{Task}_i + \beta_3 \text{FailureMode}_i + u_i$$
   where $u_i \sim \mathcal{N}(0, \sigma_u^2)$ represents random intercepts for scenarios.
4. **Multiple Testing Correction:** Benjamini-Hochberg False Discovery Rate (FDR) control applied across all pairwise condition contrasts ($\alpha_{\text{FDR}} = 0.05$).
5. **Equivalence Testing (TOST):** Two One-Sided Tests with equivalence bounds $[-\delta, +\delta] = [-0.05, +0.05]$ to statistically demonstrate the absence of history dependence if $\Delta \text{SR} \approx 0$.

---

## 12. Stopping Rule

1. **Fixed-Horizon Execution:** All 19,200 planned rollouts must be executed to completion. No early stopping based on interim p-values, significance trends, or running averages is permitted.
2. **Technical Abort Triggers:** An individual rollout or batch must be aborted only under verifiable computational faults:
   - Numerical instability: MuJoCo state vector containing `NaN` or `Inf`.
   - Matching failure: $D > 10^{-10}\text{ m}$.
   - Memory restoration mismatch: $\|h_B - h_A\| > 10^{-6}$.
3. **Fault Logging:** Aborted rollouts are logged in an unalterable fault log (`results/heldout_validation/fault_log.json`); replacement with alternate seeds is prohibited.

---

## 13. Data Leakage Prevention Protocol

To ensure total scientific blinding and prevent data leakage:
1. **Directory Segregation:** Held-out scenarios reside exclusively in `data/heldout_validation/scenarios/`. No script in `src/causal_history_recovery/training/` shall have path references to this directory.
2. **Pre-Execution Cryptographic Hashing:** Before rollouts commence, a manifest of SHA-256 hashes for all 200 held-out scenario snapshots and prefixes is computed and committed to git (`docs/audit/heldout_manifest_hashes.json`).
3. **Frozen Checkpoints:** Policy weights are verified to have filesystem modification timestamps strictly preceding the generation of the held-out scenarios. Checkpoint SHA-256 hashes must match the pre-registered hashes in Phase 12.
4. **No Re-tuning:** Checkpoints cannot undergo fine-tuning, adaptation, or temperature adjustment on held-out data.

---

## 14. Threshold Pre-Registration Protocol

All analytical and behavioral decision thresholds are frozen based on the original pre-registered specifications:

| Parameter | Operational Value | Physical Justification | Permissible Alterations |
| :--- | :--- | :--- | :--- |
| **Target Radius ($r_{\text{goal}}$)** | $0.05\text{ m}$ (Task 1) / $0.065\text{ m}$ (Task 2) | Physical goal boundary marker | **STRICTLY ZERO** |
| **Minimum Dwell ($N_{\text{dwell}}$)** | $5$ consecutive steps | Prevents transient pass-throughs | **STRICTLY ZERO** |
| **Yaw Alignment ($|\psi_{\text{max}}|$)** | $0.25\text{ rad}$ ($\approx 14.3^\circ$) | Workpiece orientation stability | **STRICTLY ZERO** |
| **Matching Tolerance ($D_{\text{tol}}$)** | $10^{-10}\text{ m}$ | Numerical double-precision limit | **STRICTLY ZERO** |
| **Slip Detection Threshold** | $|\psi| \ge 15^\circ$ AND $d_{\text{drift}} \ge 0.020\text{ m}$ | Kinematic contact slip boundary | **STRICTLY ZERO** |
| **Contact Loss Threshold** | Pusher-object air gap $\ge 0.020\text{ m}$ | Complete mechanical detachment | **STRICTLY ZERO** |

**Prohibition Rule:** No post-hoc modification of success radii, dwell counts, or deviation thresholds is allowed after observing held-out recovery outcomes.

---

## 15. Independent Positive-Control Handling

Positive-control experiments (such as the sensor occlusion task defined in `docs/design/positive_control_design.md`):
1. **Physical Segregation:** Positive-control scenarios must be stored in an isolated directory (`data/positive_control_scenarios/`).
2. **Independent Analysis Stream:** Positive-control rollouts must be processed by a dedicated analysis pipeline writing to `results/positive_control/`.
3. **No Metric Pooling:** Under no circumstances shall positive-control recovery metrics be averaged, pooled, or combined with held-out validation benchmark metrics.
4. **Interpretive Boundary:** The positive control is treated strictly as an *instrument calibration check* (confirming that the harness can detect history dependence when observations are artificially degraded), whereas the held-out validation measures *intrinsic history dependence in standard execution*.

---

## 16. Protocol Integrity Notice

- **No Experiment Run:** This document constitutes a formal design and validation plan. No held-out rollouts have been executed.
- **No Claims of Completion:** Held-out validation is designated as **PLANNED**; no claims of held-out validation completion or empirical generalizability are made.
- **Original Results Unaltered:** All existing benchmark results in `results/phase_12_stage_c/` remain strictly immutable and unoverwritten.

