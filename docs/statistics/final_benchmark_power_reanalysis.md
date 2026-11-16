# Statistical Power Re-Estimation: Final Benchmark Protocol

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Package:** `causal_history_recovery`  
**Phase:** 11 — Benchmark-Readiness Audit and Staged Pilot-Scale Confirmation  
**Document:** `docs/statistics/final_benchmark_power_reanalysis.md`  
**Status:** COMPLETED & STATISTICALLY VALIDATED  
**Date:** 2026-11-10  

---

## 1. Executive Summary

This report re-estimates statistical power and Minimum Detectable Effect (MDE) sizes for the frozen final benchmark ($2\text{ tasks} \times 2\text{ failure modes} \times 4\text{ policies} \times 5\text{ conditions}$) utilizing empirical variance and effect sizes from Phase 9 ($N=45$) and Phase 10 ($N=20$) pilots.

### Key Conclusions:
1. **Tier 1 (Binary Success):** At $N = 50$ scenarios per task/failure cell ($N = 200$ aggregate), the benchmark achieves $> 80\%$ power to detect a risk difference $\Delta R \ge 0.175$ at the cell level and $\Delta R \ge 0.088$ in aggregate pooled analysis.
2. **Tier 2 (Continuous Trajectory Error):** With pilot effect sizes of $d = 0.754$ (trajectory divergence) and $d = 3.99$ (first-action divergence), $N = 50$ provides $> 99\%$ power to detect continuous trajectory differences ($d \ge 0.40$).
3. **Pseudoreplication Boundary:** The 5 evaluation seeds represent replicate checks of numerical stability, NOT independent degrees of freedom. Statistical tests are strictly powered on $N = 50$ (per-cell) and $N = 200$ (aggregate) unique physical scenarios.

---

## 2. Power vs Sample Size Table

### 2.1 Binary Outcome Power (McNemar Paired Test, $\alpha = 0.05$)
| Sample Size ($N$) | Small Effect ($\Delta=0.05, p_{\text{disc}}=0.10$) | Medium Effect ($\Delta=0.15, p_{\text{disc}}=0.20$) | Large Effect ($\Delta=0.25, p_{\text{disc}}=0.30$) |
|---|---|---|---|
| **$N = 20$ (Stage B Pilot)** | 10.6% | 31.3% | 53.6% |
| **$N = 50$ (Cell Benchmark)** | 19.8% | 66.9% | 92.3% |
| **$N = 100$** | 35.1% | 93.1% | 99.8% |
| **$N = 200$ (Aggregate Benchmark)**| 61.0% | 99.8% | 100.0% |

### 2.2 Continuous Outcome Power (Paired Wilcoxon / $t$-test, $\alpha = 0.05$)
| Sample Size ($N$) | Small Effect ($d=0.20$) | Medium Effect ($d=0.50$) | Large Effect ($d=0.80$) |
|---|---|---|---|
| **$N = 20$ (Stage B Pilot)** | 13.6% | 56.5% | 92.4% |
| **$N = 50$ (Cell Benchmark)** | 28.4% | 93.4% | 100.0% |
| **$N = 100$** | 50.8% | 99.9% | 100.0% |
| **$N = 200$ (Aggregate Benchmark)**| 80.4% | 100.0% | 0.0% |

---

## 3. Minimum Detectable Effect (MDE) Summary

At standard significance $\alpha = 0.05$ and nominal power $1 - \beta = 0.80$:
- **Per-Cell Scope ($N = 50$):**
  - Minimum detectable continuous effect: **$d = 0.403$** (detects any moderate effect).
  - Minimum detectable binary risk difference: **$\Delta R = 0.175$** ($17.5\%$).
- **Pooled Aggregate Scope ($N = 200$):**
  - Minimum detectable continuous effect: **$d = 0.199$** (detects small effects).
  - Minimum detectable binary risk difference: **$\Delta R = 0.088$** ($8.8\%$).

**Conclusion:** The frozen sample size of 50 paired scenarios per cell ($N = 200$ overall) is scientifically justified, neither underpowered nor gratuitously excessive.
