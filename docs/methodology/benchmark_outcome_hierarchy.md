# Formal Statistical Specification: Benchmark Outcome Hierarchy & Hypothesis Registry

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Phase:** 11 — Benchmark-Readiness Audit and Staged Pilot-Scale Confirmation  
**Document:** `docs/methodology/benchmark_outcome_hierarchy.md`  
**Status:** COMPLETED & SCIENTIFICALLY VALIDATED  
**Author:** Lead Statistical Methodologist & Robotics Researcher  
**Date:** 2026-11-10  

---

## 1. Outcome Hierarchy Architecture

In accordance with Phase 11 directives, binary success and trajectory divergence are **NOT** treated as co-primary endpoints. Instead, a strict four-tier hierarchy is established to prevent endpoint inflation while capturing fine-grained motor and continuous physical dynamics:

1. **Tier 1 — Primary Confirmatory Endpoint:** Binary recovery success ($R \in \{0, 1\}$) under paired Condition B0 versus Condition B4 comparison.
2. **Tier 2 — Key Continuous Endpoint:** Final object-to-goal position error ($\|p_{\text{obj}}(T) - p_{\text{goal}}\|_2$) under paired Condition B0 versus Condition B4 comparison.
3. **Tier 3 — Mechanism Endpoints (Exploratory):** First-action divergence, action-sequence divergence, object-trajectory divergence, hidden-state divergence, contact-trajectory divergence.
4. **Tier 4 — Secondary Endpoints (Exploratory / Descriptive):** Physical recovery rate, detection rate, corrective action rate, recovery time, control effort, safety violations, policy ranking stability.

---

## 2. Exhaustive Specification Table Across All Outcomes

| Outcome Category | Outcome Metric | Status | Hypothesis ($H_1$) | Null Hypothesis ($H_0$) | Statistical Test | Effect-Size Measure | Confidence Interval | Multiple-Comparison Correction | Interpretation Rule |
|---|---|---|---|---|---|---|---|---|---|
| **Tier 1: Primary Outcome** | **Binary Recovery Success ($R$)** | **Confirmatory** | Unrolling execution history significantly alters binary task success: $P(R_{\text{B0}} = 1) \neq P(R_{\text{B4}} = 1)$. | History unrolling does not alter binary success: $P(R_{\text{B0}} = 1) = P(R_{\text{B4}} = 1)$. | Exact McNemar's Test on $2 \times 2$ paired contingency table. | Cohen's $g = \|p - 0.5\|$ on discordant pairs; Risk Difference $\Delta R = R_{\text{B0}} - R_{\text{B4}}$. | Exact 95% Wilson score interval for binomial proportions; 95% BCa bootstrap CI for $\Delta R$. | Holm-Bonferroni step-down correction across the 4 policy comparisons. | If $p_{\text{adj}} < 0.05$, reject $H_0$ and claim history-dependent binary recovery. If $p_{\text{adj}} \ge 0.05$, retain $H_0$ and interpret as history-invariant binary recovery. |
| **Tier 2: Key Continuous Outcome** | **Final Object Goal Position Error ($e_{\text{pos}}$)** | **Confirmatory** | Unrolling execution history significantly reduces final distance to target: $\mathbb{E}[e_{\text{pos}, \text{B0}}] \neq \mathbb{E}[e_{\text{pos}, \text{B4}}]$. | History unrolling has no effect on final distance: $\mathbb{E}[e_{\text{pos}, \text{B0}}] = \mathbb{E}[e_{\text{pos}, \text{B4}}]$. | Wilcoxon Signed-Rank Test (paired continuous). | Cohen's $d = \frac{\bar{D}}{s_D}$; Cliff's Delta ($\delta$). | 95% BCa bootstrap confidence interval (10,000 resamples). | Holm-Bonferroni step-down correction across policies. | Tested conditionally or in parallel with Tier 1. Confirms whether trajectory guidance diverges even when binary threshold is missed. |
| **Tier 3: Mechanism Outcome** | **First-Action Divergence ($\Delta a_0$)** | **Exploratory** | Unrolling prefix memory produces an immediate action divergence at $t_{\text{dev}}$: $\|a_{\text{B0}}(0) - a_{\text{B4}}(0)\| > 0$. | Immediate actions are invariant: $\|a_{\text{B0}}(0) - a_{\text{B4}}(0)\| = 0$. | Paired two-tailed Student's $t$-test or Wilcoxon test. | Cohen's $d$ on action vector difference. | 95% bootstrap CI. | None (Exploratory / Diagnostic). | Verifies that policy memory alters instantaneous motor output at deviation onset. |
| **Tier 3: Mechanism Outcome** | **Action Sequence Divergence ($\text{MAE}_a$)** | **Exploratory** | Unrolling prefix memory alters the subsequent action sequence: $\text{MAE}(a_{\text{B0}}, a_{\text{B4}}) > 0$. | Action sequences are identical: $\text{MAE}(a_{\text{B0}}, a_{\text{B4}}) = 0$. | Wilcoxon Signed-Rank Test. | Cohen's $d$. | 95% bootstrap CI. | None (Exploratory / Diagnostic). | Measures persistence of memory influence across the rollout. |
| **Tier 3: Mechanism Outcome** | **Object Trajectory Divergence ($\text{MAE}_{\text{obj}}$)** | **Exploratory** | Spatial object path diverges under history unrolling: $\text{MAE}(p_{\text{obj}, \text{B0}}, p_{\text{obj}, \text{B4}}) > 0$. | Spatial object paths are identical: $\text{MAE} = 0$. | Wilcoxon Signed-Rank Test. | Cohen's $d$. | 95% bootstrap CI. | None (Exploratory / Diagnostic). | Measures physical divergence in the environment induced by action changes. |
| **Tier 3: Mechanism Outcome** | **Hidden-State Divergence ($\|h_{\text{B0}} - h_{\text{B4}}\|$)** | **Exploratory** | Prefix unrolling reconstructs non-zero hidden vectors: $\|h_{\text{B0}}(t_{\text{dev}})\| > 0$. | Hidden states remain zero: $\|h_{\text{B0}}(t_{\text{dev}})\| = 0$. | One-sample $t$-test against 0. | Vector norm $\|h\|$. | 95% bootstrap CI. | None (Exploratory / Diagnostic). | Confirms recurrent representation is populated and active. |
| **Tier 3: Mechanism Outcome** | **Contact Trajectory Divergence ($\Delta c$)** | **Exploratory** | Discrete contact sequences differ between B0 and B4: $\text{MAE}(c_{\text{B0}}, c_{\text{B4}}) > 0$. | Contact sequences are identical: $\text{MAE} = 0$. | Paired Sign Test. | Proportion discordant contact steps. | 95% Wilson CI. | None (Exploratory / Diagnostic). | Detects differences in physical contact manifolds and slip events. |
| **Tier 4: Secondary Outcome** | **Physical Recovery Rate** | **Exploratory** | Object within 8 cm and aligned within tolerance regardless of dwell. | Rate equivalence. | McNemar's Test. | Risk Difference ($\Delta$). | 95% Wilson CI. | None (Secondary). | Measures coarse physical proximity independent of strict dwell time. |
| **Tier 4: Secondary Outcome** | **Corrective Action Rate** | **Exploratory** | Policy initiates active turning or retraction ($a_x < -0.002$ or $\|a_y\| > 0.003$). | Rate equivalence. | McNemar's Test. | Risk Difference ($\Delta$). | 95% Wilson CI. | None (Secondary). | Differentiates active recovery maneuvers from open-loop forward pushing. |
| **Tier 4: Secondary Outcome** | **Detection Rate & Delay** | **Exploratory** | Time steps from deviation onset to corrective action initiation. | Equal detection latency. | Mann-Whitney $U$ test. | Median difference (steps). | 95% bootstrap CI. | None (Secondary). | Quantifies temporal lag in policy reaction. |
| **Tier 4: Secondary Outcome** | **Recovery Time ($T_{\text{rec}}$)** | **Exploratory** | Steps to successful goal dwell. | Equal completion speed. | Wilcoxon Signed-Rank Test. | Mean difference (steps). | 95% bootstrap CI. | None (Secondary). | Evaluates efficiency of recovery. |
| **Tier 4: Secondary Outcome** | **Control Effort ($\sum \|a\|^2$)** | **Exploratory** | Total squared motor action norm. | Equal motor effort. | Wilcoxon Signed-Rank Test. | Mean difference. | 95% bootstrap CI. | None (Secondary). | Evaluates energy/torque expenditure. |
| **Tier 4: Secondary Outcome** | **Safety Violations** | **Exploratory** | Count of boundary, table-escape, or velocity limit breaches. | Zero violations in both conditions. | Poisson exact test. | Rate ratio. | Exact Poisson CI. | None (Safety Check). | Zero-tolerance safety filter; any violation triggers immediate flag. |
| **Tier 4: Secondary Outcome** | **Policy Ranking Stability** | **Exploratory** | Relative performance ranking is preserved across conditions: $\tau(R_{\text{B0}}, R_{\text{B4}}) = 1.0$. | Independence of rankings: $\tau \le 0$. | Kendall's Rank Correlation Test ($\tau$). | Kendall's $\tau$; Spearman's $\rho$. | Permutation CI. | None (Systematic Check). | Detects rank inversions where history alters which policy is superior. |

---

## 3. Confirmatory vs Exploratory Decision Rules

1. **Confirmatory Findings:** Only Tier 1 (Binary Success) and Tier 2 (Final Goal Error) qualify for confirmatory statistical claims regarding causal history dependence. Rejection of $H_0$ requires $p_{\text{adj}} < 0.05$ following Holm-Bonferroni correction.
2. **Exploratory Findings:** Tiers 3 and 4 are explicitly diagnostic. They elucidate the internal representational and physical mechanisms of policy behavior, but cannot alone justify claims of causal recovery superiority unless Tier 1 or Tier 2 demonstrates statistically significant differences.

