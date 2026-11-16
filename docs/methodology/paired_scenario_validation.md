# Paired Scenario Validation Protocol (15-Point Verification)

> **Document Type:** Research Methodology Specification & Quality Control Protocol  
> **Project:** Causal-History Dependence in Robot Policy Recovery  
> **Phase:** 5 (Paired Scenario Generation & Matching-Yield Optimization)  
> **Status:** `Verified & Operational`  
> **Mandate:** Zero unvalidated scenarios admitted into benchmark datasets.

---

## 1. Overview of Validation Framework

To ensure that generated paired scenarios are scientifically valid, mechanically plausible, and completely free from experimental confounds or information leaks, every paired scenario must pass an exhaustive **15-point automated validation gate**.

A scenario is admitted into `results/paired_scenarios/` if and only if **all 15 validation checks evaluate to PASS**. If any single check fails, the scenario is rejected, logged with the specific failure cause, and excluded from the recovery dataset.

---

## 2. 15-Point Validation Matrix

| # | Validation Rule | Physical / Algorithmic Specification | Threshold / Criterion | Failure Action |
|---|---|---|---|---|
| **1** | **Source Failure Plausibility** | Failure arises via physical contact slip; not artificial injection | Peak yaw $\ge 10.0^\circ$, lateral drift $\ge 0.012\text{ m}$ | Reject (`implausible_failure`) |
| **2** | **Oracle Recoverability** | Privileged oracle solves task from $s(t_d)$ within remaining horizon | $R_{\text{oracle}} = 1$ with dwell $\ge 5$ steps | Reject (`unrecoverable_failure`) |
| **3** | **Physical State Validity** | Coordinate vectors are finite, non-NaN, within physical bounds | $\max(|\mathbf{q}_{\text{pos}}|) < 10.0$, $\text{NaN} = 0$ | Reject (`invalid_state_vectors`) |
| **4** | **Object Workspace Bounds** | Object resting on table surface within reachable table bounds | $x \in [0.05, 0.50]$, $y \in [-0.20, 0.20]$, $z \ge 0.020$ | Reject (`object_out_of_bounds`) |
| **5** | **Manipulator Limits** | Pusher end-effector within reachable joint kinematics | $x \in [-0.15, 0.55]$, $y \in [-0.25, 0.25]$, $z \in [-0.05, 0.10]$ | Reject (`robot_limit_violation`) |
| **6** | **Contact State Consistency** | Contact manifolds recomputed cleanly via `mj_forward` | Zero phantom contacts; normal forces finite ($\le 50\text{ N}$) | Reject (`contact_restoration_failure`) |
| **7** | **Goal State Preservation** | Task goal vector $\mathbf{g}$ is strictly identical across conditions | $\|\mathbf{g}_{\text{cond}} - \mathbf{g}_{\text{source}}\|_2 < 1.0 \times 10^{-6}$ | Reject (`goal_discrepancy`) |
| **8** | **Horizon Preservation** | Remaining horizon $T_{\max} - t_d$ is strictly invariant | $|H_{\text{rem, cond}} - (T_{\max} - t_d)| == 0$ steps | Reject (`horizon_mismatch`) |
| **9** | **State-Matching Tolerance** | Generalized coordinate error between B0 at $t_d$ and injected state | $D(s_{\text{cond}}, s_{\text{source}}) \le 1.0 \times 10^{-6}$ | Reject (`state_matching_error`) |
| **10** | **Hidden State Isolation** | Hidden state $\mathbf{h}$ preserved in B0/B1/B2; bitwise zero in B3/B4 | $\|\mathbf{h}_{\text{B3}}\|_2 == 0.0$, $\|\mathbf{h}_{\text{B4}}\|_2 == 0.0$ | Reject (`hidden_state_leakage`) |
| **11** | **Observation History Masking** | Observation buffer preserved in B0/B1/B3; masked in B2/B4 | All buffered obs in B2/B4 set to current observation $\mathbf{o}_{t_d}$ | Reject (`obs_history_bleed`) |
| **12** | **Action History Masking** | Action buffer preserved in B0/B2/B3; zero-masked in B1/B4 | All buffered actions in B1/B4 set to $\mathbf{0}$ | Reject (`action_history_bleed`) |
| **13** | **Contact History Integrity** | Contact history archived up to $t_d$; properly synchronized | Contact log length equals $t_d$ | Reject (`contact_history_error`) |
| **14** | **Random State Synchronization** | Python/NumPy RNG seeds synchronized deterministically | Seed recorded; deterministic evaluation mode | Reject (`unseeded_evaluation`) |
| **15** | **Zero Future Information Leakage** | Trajectory archives contain zero timesteps $t > t_d$ | Max logged timestep in prefix $\le t_d$ | Reject (`future_info_leakage`) |

---

## 3. Automated Validation Pipeline

The validation logic is encapsulated in `PairedScenarioValidator`:
```python
validator = PairedScenarioValidator(tolerance=1e-6)
report = validator.validate_scenario(scenario_data)
if not report["all_passed"]:
    # Log rejection reason and quarantine scenario
    logger.log_rejected(scenario_data, report["failed_rules"])
```

The resulting `results/paired_scenarios/validation_report.json` logs the per-rule pass rates and ensures that the benchmark dataset contains exclusively validated scenarios.

