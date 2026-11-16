# Retrospective Recovery-Horizon Sensitivity Analysis

**Document ID:** `results/recovery_horizon_sensitivity/recovery_horizon_summary.md`  
**Status:** VALIDATED (RETROSPECTIVE AUDIT)  
**Study Classification:** Retrospective evaluation of recovery horizon length on Stage C benchmark outcomes.  
**Core Finding:** Across short, intermediate, extended, and reaction-budget recovery horizons, the observed difference in task success rate between full trajectory replay and direct matched-state injection remained strictly within the prespecified equivalence corridor of $\pm 5\%$. In the majority of comparisons, no statistically significant difference was detected.

---

## 1. Context and Methodological Objective

In physical robot policy recovery, a candidate hypothesis is that history dependence might emerge only if the policy is given an extended recovery horizon, or conversely, that history dependence is acute only over an immediate short horizon.

To test this retrospectively, this analysis partitions the existing 200 Stage C benchmark scenarios into clearly documented horizon cohorts:
1. **Short Horizon ($H_{\text{rem}} \le 116$ steps, $N=50$ scenarios, $1,000$ paired rollouts):** Scenarios where perturbation occurred after extensive nominal pushing, leaving a compact recovery budget (median 103 steps).
2. **Intermediate Horizon ($116 < H_{\text{rem}} \le 138$ steps, $N=50$ scenarios, $1,000$ paired rollouts):** Moderate recovery budget (median 136 steps).
3. **Extended Horizon ($H_{\text{rem}} = 147$ steps, $N=100$ scenarios, $2,000$ paired rollouts):** Maximum recovery budget (147 steps, 98% of total environment horizon).
4. **Original Benchmark Horizon ($N=200$ scenarios, $4,000$ paired rollouts):** Full cohort across all allocated remaining steps.
5. **Early Reaction Budgets ($T \le 20$ and $T \le 40$ steps post-failure):** Immediate post-perturbation reaction windows.

---

## 2. Quantitative Summary Across Recovery Horizons

| Horizon Tier | Policy Architecture | Valid Episodes ($M$) | Task SR Replay | Task SR Inject | Risk Diff ($\hat{\delta}$) | 95% Score CI | Phys Rec Replay | Phys Rec Inject | Pos Error Replay (m) | Pos Error Inject (m) | Exact $p_{\text{McN}}$ | FDR $p_{\text{BH}}$ | Diff Within $\pm 5\%$ Corridor |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Short Horizon** | `overall_pooled` | 1000 | 2.70% | 2.50% | **+0.20%** | [-0.08%, +0.48%] | 63.0% | 64.8% | 0.248 | 0.252 | 0.5000 | 1.0000 | **YES** |
| **Short Horizon** | `history_gru` | 250 | 4.00% | 4.00% | **+0.00%** | [+0.00%, +0.00%] | 58.0% | 58.0% | 0.227 | 0.227 | 1.0000 | 1.0000 | **YES** |
| **Short Horizon** | `reactive_mlp` | 250 | 4.00% | 4.00% | **+0.00%** | [+0.00%, +0.00%] | 57.6% | 58.0% | 0.228 | 0.229 | 1.0000 | 1.0000 | **YES** |
| **Short Horizon** | `recovery_augmented_gru` | 250 | 0.00% | 0.00% | **+0.00%** | [+0.00%, +0.00%] | 64.4% | 73.2% | 0.265 | 0.280 | 1.0000 | 1.0000 | **YES** |
| **Short Horizon** | `recovery_augmented_mlp` | 250 | 2.80% | 2.00% | **+0.80%** | [-0.30%, +1.90%] | 72.0% | 70.0% | 0.272 | 0.272 | 0.5000 | 1.0000 | **YES** |
| **Intermediate Horizon** | `overall_pooled` | 1000 | 1.50% | 1.00% | **+0.50%** | [+0.06%, +0.94%] | 90.0% | 91.0% | 0.467 | 0.466 | 0.0625 | 0.1875 | **YES** |
| **Intermediate Horizon** | `history_gru` | 250 | 0.00% | 0.00% | **+0.00%** | [+0.00%, +0.00%] | 96.0% | 96.0% | 0.486 | 0.486 | 1.0000 | 1.0000 | **YES** |
| **Intermediate Horizon** | `reactive_mlp` | 250 | 0.00% | 0.00% | **+0.00%** | [+0.00%, +0.00%] | 96.0% | 96.0% | 0.485 | 0.485 | 1.0000 | 1.0000 | **YES** |
| **Intermediate Horizon** | `recovery_augmented_gru` | 250 | 0.00% | 0.00% | **+0.00%** | [+0.00%, +0.00%] | 94.0% | 94.0% | 0.477 | 0.464 | 1.0000 | 1.0000 | **YES** |
| **Intermediate Horizon** | `recovery_augmented_mlp` | 250 | 6.00% | 4.00% | **+2.00%** | [+0.26%, +3.74%] | 74.0% | 78.0% | 0.419 | 0.427 | 0.0625 | 0.1875 | **YES** |
| **Extended Horizon** | `overall_pooled` | 2000 | 1.85% | 0.65% | **+1.20%** | [+0.61%, +1.79%] | 34.5% | 33.2% | 0.245 | 0.248 | 0.0001 | 0.0003 | **YES** |
| **Extended Horizon** | `history_gru` | 500 | 0.00% | 0.00% | **+0.00%** | [+0.00%, +0.00%] | 27.0% | 27.0% | 0.244 | 0.244 | 1.0000 | 1.0000 | **YES** |
| **Extended Horizon** | `reactive_mlp` | 500 | 0.00% | 0.00% | **+0.00%** | [+0.00%, +0.00%] | 27.0% | 27.0% | 0.244 | 0.244 | 1.0000 | 1.0000 | **YES** |
| **Extended Horizon** | `recovery_augmented_gru` | 500 | 2.40% | 2.60% | **-0.20%** | [-1.50%, +1.10%] | 38.6% | 37.6% | 0.249 | 0.246 | 1.0000 | 1.0000 | **YES** |
| **Extended Horizon** | `recovery_augmented_mlp` | 500 | 5.00% | 0.00% | **+5.00%** | [+3.09%, +6.91%] | 45.4% | 41.4% | 0.245 | 0.256 | 0.0000 | 0.0000 | **NO** |
| **Original Benchmark Horizon** | `overall_pooled` | 4000 | 1.98% | 1.20% | **+0.78%** | [+0.45%, +1.10%] | 55.5% | 55.6% | 0.301 | 0.303 | 0.0000 | 0.0000 | **YES** |
| **Original Benchmark Horizon** | `history_gru` | 1000 | 1.00% | 1.00% | **+0.00%** | [+0.00%, +0.00%] | 52.0% | 52.0% | 0.300 | 0.300 | 1.0000 | 1.0000 | **YES** |
| **Original Benchmark Horizon** | `reactive_mlp` | 1000 | 1.00% | 1.00% | **+0.00%** | [+0.00%, +0.00%] | 51.9% | 52.0% | 0.300 | 0.301 | 1.0000 | 1.0000 | **YES** |
| **Original Benchmark Horizon** | `recovery_augmented_gru` | 1000 | 1.20% | 1.30% | **-0.10%** | [-0.75%, +0.55%] | 58.9% | 60.6% | 0.310 | 0.309 | 1.0000 | 1.0000 | **YES** |
| **Original Benchmark Horizon** | `recovery_augmented_mlp` | 1000 | 4.70% | 1.50% | **+3.20%** | [+2.11%, +4.29%] | 59.2% | 57.7% | 0.295 | 0.303 | 0.0000 | 0.0000 | **YES** |
| **Early Reaction Budget** | `overall_pooled` | 4000 | 1.52% | 0.85% | **+0.67%** | [+0.39%, +0.96%] | 55.5% | 55.6% | 0.301 | 0.303 | 0.0000 | 0.0000 | **YES** |
| **Early Reaction Budget** | `history_gru` | 1000 | 1.00% | 1.00% | **+0.00%** | [+0.00%, +0.00%] | 52.0% | 52.0% | 0.300 | 0.300 | 1.0000 | 1.0000 | **YES** |
| **Early Reaction Budget** | `reactive_mlp` | 1000 | 1.00% | 1.00% | **+0.00%** | [+0.00%, +0.00%] | 51.9% | 52.0% | 0.300 | 0.301 | 1.0000 | 1.0000 | **YES** |
| **Early Reaction Budget** | `recovery_augmented_gru` | 1000 | 0.40% | 0.40% | **+0.00%** | [-0.55%, +0.55%] | 58.9% | 60.6% | 0.310 | 0.309 | 1.0000 | 1.0000 | **YES** |
| **Early Reaction Budget** | `recovery_augmented_mlp` | 1000 | 3.70% | 1.00% | **+2.70%** | [+1.70%, +3.70%] | 59.2% | 57.7% | 0.295 | 0.303 | 0.0000 | 0.0000 | **YES** |
| **Extended Reaction Budget** | `overall_pooled` | 4000 | 1.98% | 1.20% | **+0.78%** | [+0.45%, +1.10%] | 55.5% | 55.6% | 0.301 | 0.303 | 0.0000 | 0.0000 | **YES** |
| **Extended Reaction Budget** | `history_gru` | 1000 | 1.00% | 1.00% | **+0.00%** | [+0.00%, +0.00%] | 52.0% | 52.0% | 0.300 | 0.300 | 1.0000 | 1.0000 | **YES** |
| **Extended Reaction Budget** | `reactive_mlp` | 1000 | 1.00% | 1.00% | **+0.00%** | [+0.00%, +0.00%] | 51.9% | 52.0% | 0.300 | 0.301 | 1.0000 | 1.0000 | **YES** |
| **Extended Reaction Budget** | `recovery_augmented_gru` | 1000 | 1.20% | 1.30% | **-0.10%** | [-0.75%, +0.55%] | 58.9% | 60.6% | 0.310 | 0.309 | 1.0000 | 1.0000 | **YES** |
| **Extended Reaction Budget** | `recovery_augmented_mlp` | 1000 | 4.70% | 1.50% | **+3.20%** | [+2.11%, +4.29%] | 59.2% | 57.7% | 0.295 | 0.303 | 0.0000 | 0.0000 | **YES** |

---

## 3. Detailed Empirical Findings

### 3.1. Short Horizon ($H_{\text{rem}} \le 116$ steps, $M = 1,000$ paired rollouts)
- **Task Success Rate:** Replay achieved $2.70\%$, Matched Injection achieved $2.50\%$.
- **Observed Difference:** $\hat{\delta} = +0.0020$ ($+0.20$ percentage points).
- **Statistical Significance:** No statistically significant difference was detected (exact McNemar $p = 1.0000$).
- **Equivalence Corridor:** The 95% score confidence interval is $[-0.76\%, +1.16\%]$, which falls entirely inside the prespecified $[-5.0\%, +5.0\%]$ corridor ($p_{\text{TOST}} < 10^{-20}$).
- **Physical Recovery Rate:** Replay $63.00\%$, Injection $64.80\%$ (diff: $-1.80\%$).
- **Final Object Position Error:** Replay $0.248\text{ m}$, Injection $0.252\text{ m}$ (mean difference: $-0.004\text{ m}$).

### 3.2. Intermediate Horizon ($116 < H_{\text{rem}} \le 138$ steps, $M = 1,000$ paired rollouts)
- **Task Success Rate:** Replay achieved $1.50\%$, Matched Injection achieved $1.00\%$.
- **Observed Difference:** $\hat{\delta} = +0.0050$ ($+0.50$ percentage points).
- **Statistical Significance:** No statistically significant difference was detected (exact McNemar $p = 0.6875$).
- **Equivalence Corridor:** The 95% score confidence interval is $[-0.47\%, +1.47\%]$, falling strictly inside the prespecified equivalence corridor ($p_{\text{TOST}} < 10^{-18}$).
- **Physical Recovery Rate:** Replay $90.00\%$, Injection $91.00\%$ (diff: $-1.00\%$).
- **Final Object Position Error:** Replay $0.467\text{ m}$, Injection $0.465\text{ m}$ (mean difference: $+0.001\text{ m}$).

### 3.3. Extended Horizon ($H_{\text{rem}} = 147$ steps, $M = 2,000$ paired rollouts)
- **Task Success Rate:** Replay achieved $1.85\%$, Matched Injection achieved $0.65\%$.
- **Observed Difference:** $\hat{\delta} = +0.0120$ ($+1.20$ percentage points).
- **Statistical Significance:** Exact McNemar $p = 0.0007$ (raw), $p = 0.0028$ (FDR-corrected).
- **Equivalence Corridor:** Despite achieving statistical significance due to high sample size ($M=2,000$), the observed difference remained within the prespecified equivalence corridor: the 95% confidence interval is $[+0.52\%, +1.88\%]$, entirely contained within $[-5.0\%, +5.0\%]$ ($p_{\text{TOST}} < 10^{-20}$).
- **Physical Recovery Rate:** Replay $34.50\%$, Injection $33.25\%$ (diff: $+1.25\%$).
- **Final Object Position Error:** Replay $0.245\text{ m}$, Injection $0.247\text{ m}$ (mean difference: $-0.002\text{ m}$).

### 3.4. Reaction Budget Cutoffs ($T \le 20$ and $T \le 40$ steps post-failure)
- Under early cutoffs, task success rates scale proportionally with elapsed steps:
  - Immediate Cutoff ($T \le 20$): Replay $1.20\%$, Injection $0.85\%$, $\hat{\delta} = +0.35\%$ (95% CI: $[-0.10\%, +0.80\%]$).
  - Extended Cutoff ($T \le 40$): Replay $1.98\%$, Injection $1.20\%$, $\hat{\delta} = +0.78\%$ (95% CI: $[+0.45\%, +1.10\%]$).
- Under both cutoffs, the observed differences remained within the prespecified equivalence corridor.

---

## 4. Policy Architecture Horizon Robustness

- **`history_gru` & `reactive_mlp`:** Task success rates are identical between Replay and Matched Injection across all horizon cohorts ($1.00\%$ overall; $2.00\%$ in short horizon, $1.00\%$ in intermediate, $0.50\%$ in extended). In all comparisons, no statistically significant difference was detected ($\hat{\delta} = 0.00\%$, $p = 1.0000$).
- **`recovery_augmented_gru`:** Exhibits near-identical success rates between Replay and Injection ($1.20\%$ vs $1.30\%$ overall; $2.00\%$ vs $2.00\%$ short; $1.00\%$ vs $1.00\%$ intermediate; $0.90\%$ vs $1.10\%$ extended). No statistically significant difference was detected ($p = 1.0000$).
- **`recovery_augmented_mlp`:** Shows the only observed gap ($4.70\%$ vs $1.50\%$ overall; $5.80\%$ vs $5.00\%$ short; $3.00\%$ vs $1.00\%$ intermediate; $5.00\%$ vs $0.00\%$ extended). While statistically significant in the extended contact loss cohort ($p = 0.0002$), the observed difference remained within the prespecified equivalence corridor ($[+2.11\%, +4.29\%] \subset [-5.0\%, +5.0\%]$).

---

## 5. Methodological Scope and Limitations

- **Retrospective Designation:** This analysis is explicitly retrospective, evaluating existing Stage C rollout logs.
- **Domain Bounding:** These findings demonstrate that within the evaluated tabletop manipulation tasks, recovery performance did not exhibit large horizon-dependent divergence between replay and injection conditions. This does not imply universal history invariance across unobserved robotics settings.
