# Pre-Experiment Benchmark Specification: Official Benchmark Design Freeze (V1.0)

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Phase:** 10 — Outcome-Sensitivity Audit, Second-Task Pilot, and Final Benchmark Design Freeze  
**Document:** `docs/methodology/final_benchmark_design.md`  
**Status:** FROZEN & FORMALLY SPECIFIED (Awaiting Explicit User Approval for Phase 11)  
**Date:** 2026-11-09  

---

## 1. Benchmark Purpose and Methodological Scope

This document specifies the frozen protocol for the official benchmark evaluation of causal-history dependence in robot policy recovery under matched physical states. 

### Methodological Boundaries:
- **No Novelty Claims or Final Causality Claims Prior to Execution:** Labeled strictly as:  
  *“Pre-registered benchmark design — frozen protocol.”*
- **No Execution in Phase 10:** Execution is strictly paused pending explicit user approval.
- **Independence Guarantee:** Zero data or results inherited from prior projects (MIND-Contact / MIND-Contact++).

---

## 2. Experimental Design Matrix

| Benchmark Dimension | Frozen Specification | Scientific Justification |
|---|---|---|
| **Number of Tasks ($N_{\text{tasks}}$)** | **2 Tasks** (`PushTargetEnv`, `SecondPushTaskEnv`) | Tests across distinct geometries (box vs cylinder), masses (0.10 vs 0.15 kg), friction coefficients ($\mu=0.50$ vs $0.35$), and push directions (axis-aligned vs diagonal). |
| **Number of Failure Types ($N_{\text{failures}}$)** | **2 Failure Modes** (Off-Center Contact Slip, Contact-Loss / Premature Stall) | Contrasts rotational contact slip (active contact, high yaw) against disengagement (zero contacts, air gap, zero velocity). |
| **Number of Evaluated Policies** | **4 Learned Policy Architectures** | 1. `reactive_mlp` (memoryless negative control)<br>2. `history_gru` (recurrent imitation baseline)<br>3. `recovery_augmented_mlp` (reactive recovery baseline)<br>4. `recovery_augmented_gru` (history-conditioned recovery policy) |
| **Policy Training Seeds** | **3 Independent Training Seeds** per policy (`42, 123, 456`) | Verifies that findings are robust across stochastic initialization and training runs. |
| **Evaluation Seeds** | **5 Independent Evaluation Seeds** (`7001, 7002, 7003, 7004, 7005`) | Controls simulator forward integration and replicate evaluation. |
| **Number of Valid Paired Scenarios** | **$\ge 50$ Valid Paired Scenarios** per task/failure combination ($N \ge 200$ total scenarios) | Powered to detect a true discordance difference $\Delta R \ge 0.10$ with $\beta \ge 0.80$ at $\alpha = 0.05$. |
| **Counterfactual History Conditions** | **5 Conditions** (B0, B1, B2, B3, B4) | B0: Preserved history (prefix memory unrolled)<br>B1: Action history masked ($a_{\text{prev}} = \mathbf{0}$)<br>B2: Observation history masked (obs buffer padded)<br>B3: Hidden state reset ($h = \mathbf{0}$)<br>B4: Direct matched injection (lossless state snapshot restoration; all memory zeroed) |
| **Total Benchmark Rollouts** | **$200 \text{ scenarios} \times 5 \text{ conditions} \times 5 \text{ seeds} \times 4 \text{ policies} = \mathbf{20,000\text{ rollouts}}$** | Provides sufficient statistical power across tasks, failures, and condition pairs. |

---

## 3. Physical State Matching and Admission Filters

### 3.1 State Matching Tolerance
State matching between Condition B0 and Condition B4 must be bitwise exact via MuJoCo state snapshotting:
- Generalized coordinates error: $\|q_{\text{pos}, \text{B0}}(t_{\text{dev}}) - q_{\text{pos}, \text{B4}}(t_{\text{dev}})\|_2 \equiv 0.0000000000$.
- Generalized velocities error: $\|q_{\text{vel}, \text{B0}}(t_{\text{dev}}) - q_{\text{vel}, \text{B4}}(t_{\text{dev}})\|_2 \equiv 0.0000000000$.
- Contact state matching: Identical contact points and normal forces at $t_{\text{dev}}$.

### 3.2 Privileged Oracle Recoverability Filter
Every candidate failure scenario must be solved by the designated privileged oracle controller within the remaining horizon:
- Task 1 (Slip): `PrivilegedOracleController` achieves $R_{\text{oracle}} = 1$.
- Task 2 (Contact Loss): `ContactLossOracleController` achieves $R_{\text{oracle}} = 1$.
- Unrecoverable states ($R_{\text{oracle}} = 0$) are strictly excluded from the evaluation denominator.

### 3.3 Automated 15-Point Admission Gate
Candidate scenarios must pass all 15 automated validation gates:
1. Exact physical state snapshot integrity.
2. Verified non-teleportation (continuous velocity and acceleration).
3. Workspace containment ($|x|, |y| \le 0.40$ m).
4. Table support ($z \ge 0.015$ m).
5. Valid deviation threshold ($|\theta_{\text{yaw}}| \ge 12^\circ$ for Slip; air gap $\ge 2.0$ cm for Contact Loss).
6. Non-zero remaining horizon ($T_{\text{remain}} \ge 50$ steps).
7. Target goal consistency.
8. Zero future information leakage.
9. Zero hidden state contamination in snapshot metadata.
10. Bitwise prefix replay determinism.
11. Disjoint evaluation seed block ($\ge 10000$).
12. Coulomb friction consistency.
13. Kinematic servo bounds compliance.
14. Contact solver convergence.
15. Oracle recoverability confirmation ($R_{\text{oracle}} = 1$).

---

## 4. Evaluation Metrics and Primary/Secondary Endpoints

To resolve the floor effect identified in Phase 9 and Phase 10 audits, the benchmark establishes a **co-primary endpoint structure**:

### 4.1 Primary Endpoints
- **Co-Primary Endpoint 1 (Discrete):** Binary task success with mandatory dwell time ($R \in \{0, 1\}$).
  - Target radius: $0.060\text{ m}$ (Task 1) / $0.065\text{ m}$ (Task 2).
  - Max yaw tolerance: $0.35\text{ rad}$ ($20.0^\circ$, Task 1) / $0.50\text{ rad}$ ($28.6^\circ$, Task 2).
  - Mandatory dwell time: $\ge 5$ consecutive simulation steps ($25\text{ ms}$).
- **Co-Primary Endpoint 2 (Continuous):** Final object-to-goal position error ($\|p_{\text{obj}}(T) - p_{\text{goal}}\|_2$) and continuous trajectory divergence ($\text{MAE}(p_{\text{obj}, \text{B0}}, p_{\text{obj}, \text{B4}})$).

### 4.2 Secondary Endpoints
- **Causal History Dependence Score ($H_R$):**
  $$H_R = R(\text{Condition B0}) - R(\text{Condition B4})$$
- **Continuous Distance Divergence ($H_D$):**
  $$H_D = \mathbb{E}[\|p_{\text{obj}, \text{B0}}(T) - p_{\text{goal}}\|_2] - \mathbb{E}[\|p_{\text{obj}, \text{B4}}(T) - p_{\text{goal}}\|_2]$$
- **Motor Control Divergence:** Immediate first-action divergence ($\|a_{\text{B0}}(0) - a_{\text{B4}}(0)\|_2$) and action sequence divergence ($\text{MAE}(a_{\text{B0}}, a_{\text{B4}})$).
- **Physical Recovery Rate:** Proportion of rollouts bringing object within 8 cm and aligned within tolerance regardless of dwell.
- **Safety Violation Rate:** Count of force limit or velocity boundary breaches ($v > 0.05$ m/step).
- **Policy Ranking Stability:** Kendall's $\tau$ and Spearman's $\rho$ rank correlation across conditions B0 and B4.

---

## 5. Statistical Inference and Analysis Plan

1. **Paired Discrete Comparisons:** Exact McNemar test on $2 \times 2$ contingency tables for each policy and condition pair (B0 vs B1, B0 vs B2, B0 vs B3, B0 vs B4).
2. **Paired Continuous Comparisons:** Wilcoxon signed-rank test on paired distance and trajectory errors.
3. **Confidence Interval Estimation:** Exact 95% Wilson score intervals for binomial proportions; 10,000-sample BCa bootstrap intervals for continuous paired differences.
4. **Multiple Comparison Correction:** Holm-Bonferroni step-down correction applied across all pairwise comparisons within each policy.
5. **Effect Size Measures:** Cohen's $g$ for paired binary discordance; Cohen's $d$ and Cliff's $\delta$ for continuous trajectory metrics.
6. **Stopping Rule:** No sequential stopping or interim peeking. The full $N = 200$ scenario cohort must be evaluated across all seeds before computing final confirmatory statistics.

---

## 6. Pre-Registration Freeze Confirmation

All experimental parameters, seeds, architectures, and analysis scripts are frozen as of Phase 10. Execution will commence only upon explicit user approval for Phase 11.

