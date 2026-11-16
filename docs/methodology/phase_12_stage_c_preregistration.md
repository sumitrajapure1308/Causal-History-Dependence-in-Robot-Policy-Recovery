# Phase 12 Pre-Registration: Official Stage C Benchmark Execution

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Repository Directory:** `causal-history-recovery/`  
**Phase:** Phase 12 (Official Confirmatory Stage C Benchmark Execution)  
**Date:** November 2026  
**Status Tags:** `Pre-registered`, `Confirmatory`, `Benchmark`, `Frozen Protocol`  

---

## 1. Administrative Information & Methodological Separation

- **Study Type:** Confirmatory simulation-based robotic recovery benchmark with matched-state counterfactual memory interventions.
- **Project Boundary:** Completely independent project. Zero linkage, code sharing, or data transfer with MIND-Contact or MIND-Contact++.
- **Version Control Status:** Local file manifest audited with SHA-256 signatures; Git version control is not initialized in the local repository directory.
- **Protocol Freeze Timestamp:** Pre-registered and frozen prior to any Stage C scenario generation or rollout execution.

---

## 2. 6-Factor Full Factorial Benchmark Design

The official Stage C confirmatory benchmark evaluates a full factorial design comprising:

$$\text{Total Rollouts} = 2 \times 2 \times 4 \times 5 \times 5 \times 50 = 20,000$$

### 2.1 Tasks ($T=2$)
1. `task1_cube`: `PushTargetEnv`
   - Manipulator: 3-DoF Cartesian manipulator ($[-0.02, 0.02]\,\text{m/step}$).
   - Object: 6-DoF free-joint cube ($m = 0.10\,\text{kg}, \text{half-size} = 0.025\,\text{m}$, sliding friction $\mu = 0.50$).
   - Goal: Target radius $r = 0.05\,\text{m}$ at $[0.25, 0.0, 0.025]$.
   - Dwell Requirement: $\ge 5$ consecutive steps inside radius with $|\Delta \theta| \le 15^\circ$.
2. `task2_puck`: `SecondPushTaskEnv`
   - Manipulator: 3-DoF Cartesian manipulator ($[-0.02, 0.02]\,\text{m/step}$).
   - Object: 6-DoF cylinder puck ($m = 0.15\,\text{kg}, r = 0.035\,\text{m}, h = 0.020\,\text{m}$, sliding friction $\mu = 0.35$).
   - Goal: Target radius $r = 0.065\,\text{m}$ at $[0.20, 0.08, 0.020]$ (diagonal push).
   - Dwell Requirement: $\ge 5$ consecutive steps inside radius.

### 2.2 Failure Modes ($F=2$)
1. `rotational_slip` (Failure Mode 1): Execution-induced rotational slip via off-center contact torque.
   - Criterion Task 1: Yaw deflection $\ge 15.0^\circ$, lateral drift $\ge 0.018\,\text{m}$, contact steps $\ge 5$.
   - Criterion Task 2: Yaw deflection $\ge 8.0^\circ$ or lateral drift $\ge 0.012\,\text{m}$.
2. `contact_loss` (Failure Mode 2): Premature push disengagement via transient manipulator deceleration.
   - Criterion: Zero contacts, air gap $\ge 0.020\,\text{m}$, distance to goal $\ge 0.080\,\text{m}$, object speed $\le 0.015\,\text{m/s}$ sustained for $\ge 3$ consecutive steps.

### 2.3 Policy Suite ($P=4$)
All policies evaluate identical frozen checkpoints trained during Phases 3 and 7:
1. `reactive_mlp`: Nominal reactive MLP policy (`models/checkpoints/reactive_mlp_best.pt`).
2. `history_gru`: Nominal history-aware GRU policy (`models/checkpoints/history_gru_best.pt`).
3. `recovery_augmented_mlp`: Recovery-augmented reactive policy (`results/recovery_training/checkpoints/recovery_augmented_mlp_seed42.pt`).
4. `recovery_augmented_gru`: Recovery-augmented history policy (`results/recovery_training/checkpoints/recovery_augmented_gru_seed456.pt`).

*Privileged Oracle Policy Rule:* The privileged geometric oracle (`PrivilegedOracleController` / `ContactLossOracleController`) is restricted strictly to offline scenario admission filtering and establishing the empirical upper bound. It is **never** used as a learned policy baseline or given to learned policies during rollouts.

### 2.4 History-Intervention Conditions ($C=5$)
All conditions evaluate from the bitwise-identical physical state $S^*$ ($D_{\text{match}} \le 10^{-10}$):
- **B0 (Unrolled History):** Policy observation and action buffers reconstructed by unrolling the ground-truth prefix trajectory $H_{0:\tau}$ through the policy network.
- **B1 (Action Masking):** Ground-truth observation prefix unrolled; action history buffer zero-masked at recovery onset.
- **B2 (Observation Masking):** Ground-truth action prefix preserved; observation history buffer set to single current state $s_\tau$.
- **B3 (Full Masking):** Both action buffer and observation buffer masked at recovery onset.
- **B4 (Direct Matched Injection / Memoryless):** Policy initialized with fresh blank memory at state $S^*$ without prefix replay; recurrent hidden state $h_0 = 0$.

### 2.5 Evaluation Seeds ($S=5$)
5 replicate evaluation seeds are frozen:
`eval_seeds = [15001, 15002, 15003, 15004, 15005]`

*Pseudoreplication Constraint:* Deterministic simulation replicates test numerical stability, not scenario degrees of freedom. Results are averaged across seeds within each scenario before paired hypothesis testing.

### 2.6 Matched Scenarios ($N=50$ per cell, $N=200$ aggregate)
Fresh, disjoint seed ranges are frozen for scenario generation:
- **Cell 1 (Task 1 Cube + Slip):** Generation seeds starting at 10000.
- **Cell 2 (Task 1 Cube + Contact Loss):** Generation seeds starting at 11000.
- **Cell 3 (Task 2 Puck + Slip):** Generation seeds starting at 12000.
- **Cell 4 (Task 2 Puck + Contact Loss):** Generation seeds starting at 13000.

Every admitted scenario must pass all 15 automated validation rules (no future leakage, exact physical state matching $D \le 10^{-10}$, remaining horizon preservation, contact state restoration, and 100% privileged oracle recoverability).

---

## 3. Pre-Registered Outcome Hierarchy

The pre-registered outcome hierarchy strictly enforces non-conflation:

### 3.1 Tier 1: Primary Confirmatory Outcome
- **Metric:** Binary Task Success Indicator ($R \in \{0, 1\}$).
- **Primary Hypothesis:**
  - $H_0: P(R_{\text{B0}}=1, R_{\text{B4}}=0) = P(R_{\text{B0}}=0, R_{\text{B4}}=1)$
  - $H_1: P(R_{\text{B0}}=1, R_{\text{B4}}=0) \neq P(R_{\text{B0}}=0, R_{\text{B4}}=1)$
- **Statistical Test:** Exact paired McNemar test with continuity correction.
- **Effect Size Measure:** Discordance risk difference $\Delta R = R_{\text{B0}} - R_{\text{B4}}$ and paired odds ratio.
- **Multiple Comparison Correction:** Holm-Bonferroni step-down procedure across the 4 planned policy comparisons against B0 at family-wise error rate $\alpha = 0.05$.
- **Decision Rule:** Confirmatory evidence of causal-history dependence in policy recovery requires statistically significant discordance between B0 and B4 ($p_{\text{adj}} < 0.05$) in learned history policies.

### 3.2 Tier 2: Key Continuous Outcome
- **Metric:** Final Object-to-Goal Distance Error ($D_{\text{goal}} = \|x_{\text{obj}}(T) - x_{\text{goal}}\|$).
- **Primary Hypothesis:**
  - $H_0: \text{Median}(D_{\text{B0}} - D_{\text{B4}}) = 0$
  - $H_1: \text{Median}(D_{\text{B0}} - D_{\text{B4}}) \neq 0$
- **Statistical Test:** Paired Wilcoxon signed-rank test.
- **Effect Size Measure:** Paired Cohen's $d$ and rank-biserial correlation $r_{\text{rb}}$.
- **Multiple Comparison Correction:** Holm-Bonferroni correction at $\alpha = 0.05$.

### 3.3 Tier 3: Exploratory Mechanism Metrics
- Initial action divergence: $\|\Delta a_0\| = \|a_0^{\text{B0}} - a_0^{\text{B4}}\|$.
- Cumulative trajectory divergence: $\text{MAE}_{\text{traj}} = \frac{1}{K}\sum_{t=1}^K \|x_t^{\text{B0}} - x_t^{\text{B4}}\|$.
- Hidden-state reconstruction norm: $\|h_{\tau}\|$.
- Action-sequence divergence.

### 3.4 Tier 4: Secondary Contextual Outcomes
- Physical contact re-acquisition rate.
- Time-to-recovery (steps).
- Control effort: $\sum_{t} \|u_t\|^2$.
- Safety violation rate (workspace / joint limits).
- Policy ranking stability: Kendall's $\tau$ and Spearman's $\rho$ between B0 and B4.

---

## 4. Pre-Registered Statistical Analysis Plan

1. **Aggregation:**
   For each scenario $i \in \{1 \dots 50\}$ in cell $c$, policy $p$, and condition $k$, compute the seed-averaged success $\bar{R}_{i, p, k} = \frac{1}{5}\sum_{s=1}^5 R_{i, p, k, s}$ and seed-averaged final distance $\bar{D}_{i, p, k} = \frac{1}{5}\sum_{s=1}^5 D_{i, p, k, s}$.
2. **Paired Differences:**
   Compute paired differences $\Delta \bar{R}_i = \bar{R}_{i, p, \text{B0}} - \bar{R}_{i, p, k}$ and $\Delta \bar{D}_i = \bar{D}_{i, p, \text{B0}} - \bar{D}_{i, p, k}$ for $k \in \{\text{B1}, \text{B2}, \text{B3}, \text{B4}\}$.
3. **Inference:**
   Compute exact two-sided McNemar p-values on discordant pairs and two-sided Wilcoxon signed-rank p-values on continuous differences. Apply Holm-Bonferroni correction.
4. **Bootstrap Confidence Intervals:**
   Generate 10,000 paired bootstrap resamples at the scenario level to obtain 95% BCa confidence intervals for mean and median differences.
5. **Stopping Rule:**
   All 20,000 planned rollouts must be executed. No interim stopping, optional stopping, or data-dependent exclusion is permitted.

---

## 5. Pre-Registration Freeze Confirmation

This pre-registration document is hereby frozen. All scenario generation, benchmark execution, and statistical analyses will strictly adhere to the specifications herein.

