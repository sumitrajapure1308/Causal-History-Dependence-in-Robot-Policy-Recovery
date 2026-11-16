# Provisional Statistical Analysis Plan & Pilot Calibration Protocol

> **Document Status:** PROVISIONAL STATISTICAL SPECIFICATION  
> **Rule:** No statistical tests or models are finalized until empirical pilot data calibration is conducted in Phase 7.  
> **Scope:** Establishes explicit requirements for sample size determination, variance estimation, and model feasibility checks based on pilot rollouts.

---

## 1. Explicit Provisional Status of Statistical Parameters

All preliminary parameters specified in Phase 0 are explicitly classified as **provisional estimates subject to pilot calibration**:

1. **Five-Seed Plan is Provisional:**
   - The initial target of 5 seeds ($[42, 1337, 2026, 777, 999]$) is provisional. If pilot evaluations reveal high cross-seed policy variance, seed counts will be increased (e.g. to 10 seeds). If within-policy variance is minimal and between-condition differences dominate, computational resources may be allocated to deeper per-seed rollouts.
2. **50–100 Episode Sample Size is Provisional:**
   - The target of 50–100 evaluation episodes per condition is an initial estimate. The actual required sample size $N^*$ must be calculated via statistical power analysis ($\text{Power} \ge 0.80, \alpha = 0.05$) based on the empirical variance and effect sizes observed in pilot runs.
3. **Statistical Test Selection is Contingent on Pilot Distributions:**
   - Paired Wilcoxon signed-rank tests assume continuous or ordinal symmetric difference distributions. If recovery outcomes are strictly binary $\{0, 1\}$ without continuous auxiliary cost metrics, McNemar's exact test for paired binary proportions or permutation testing will be adopted.
4. **Mixed-Effects Models Require Verification of Prerequisites:**
   - Linear or logistic mixed-effects models ($y_{ijk} = \beta_0 + \beta_1 \text{Cond}_i + \dots + u_{\text{scenario}} + \epsilon$) require:
     - A sufficient number of valid matched scenario pairs ($N_{\text{pairs}} \ge 50$).
     - Sufficient outcome variance (i.e., avoiding complete separation or zero variance within scenario clusters).
     - Model convergence without singular covariance fits.

---

## 2. Pilot Calibration Requirements (To be Executed in Phase 7)

Before official benchmark execution, the pilot experiment must empirically estimate and report:

### 2.1 Valid Matching Yield Rate ($\eta_{\text{match}}$)
$$\eta_{\text{match}} = \frac{N_{\text{accepted matched pairs}}}{N_{\text{candidate mined deviation states}}}$$
- If $\eta_{\text{match}} < 0.20$ under the strict threshold ($\epsilon_1$), the deviation mining distribution must be widened, or moderate matching thresholds ($\epsilon_2$) calibrated.

### 2.2 Oracle Recoverability Rate ($\eta_{\text{recoverable}}$)
$$\eta_{\text{recoverable}} = \frac{N_{\text{oracle recovered episodes}}}{N_{\text{mined failure episodes}}}$$
- Confirms what proportion of mined failures are actually recoverable by a privileged controller. If $\eta_{\text{recoverable}} < 0.50$, the deviation trigger threshold $t_d$ is occurring too late (after irreversible terminal failure) and must be adjusted earlier in the trajectory.

### 2.3 Outcome Variance & Power Calculation
- Calculate empirical standard deviation $\hat{\sigma}$ of $H_R = R_{\text{replay}} - R_{\text{injected}}$ across pilot seeds.
- Determine required $N^*$ to detect a minimal meaningful recovery difference of $\delta = 0.10$ (10 percentage points) at power $1 - \beta = 0.80$:
  $$N^* \ge \left( \frac{z_{1 - \alpha/2} + z_{1 - \beta}}{\delta / \hat{\sigma}} \right)^2$$

---

## 3. Contingency Decision Matrix

| Pilot Observation | Statistical Consequence | Methodological Action |
|---|---|---|
| **Binary Recovery Outcome Only ($R \in \{0, 1\}$)** | Wilcoxon test has reduced granularity | Use **McNemar's test** for paired contingency tables; augment with continuous metric $C_{\text{recovery}}$. |
| **High Scenario-Level Clustered Variance** | Standard paired $t$-test biased | Fit **Generalized Linear Mixed Models (GLMM)** with logit link and random intercepts for scenario. |
| **Small Matched Pair Sample ($N < 30$)** | Asymptotic tests invalid | Use **Exact Permutation Tests** (10,000 resamples) and non-parametric bootstrap CIs. |
| **Zero Difference ($H_R = 0$) in Pilot** | Null hypothesis cannot be rejected | Conduct equivalence testing (Two One-Sided Tests, **TOST**) to bound the maximum possible history effect within $[-\Delta_0, +\Delta_0]$. |

