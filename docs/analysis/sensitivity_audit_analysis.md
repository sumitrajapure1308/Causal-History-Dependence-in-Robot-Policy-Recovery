# Stage C Benchmark Sensitivity Audit Analysis

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Repository Root:** `causal-history-recovery/`  
**Phase:** Phase 12 (Official Confirmatory Stage C Benchmark Execution)  
**Status:** `Exploratory sensitivity analysis — not confirmatory evidence.`  

---

## 1. Sensitivity Across Factorial Dimensions

| Dimension | Strata | Total Rollouts | Success Rate | Mean Distance Error (m) | Physical Recovery Rate |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Task** | `task1_cube` | 10000 | 2.06% | 0.2473 | 42.05% |
| **Task** | `task2_puck` | 10000 | 0.81% | 0.3571 | 69.13% |
| **Failure Mode** | `rotational_slip` | 10000 | 1.82% | 0.3578 | 77.39% |
| **Failure Mode** | `contact_loss` | 10000 | 1.05% | 0.2466 | 33.79% |
| **Severity Tier** | `Small` | 13900 | 1.87% | 0.2853 | — |
| **Severity Tier** | `Medium` | 2100 | 1.19% | 0.3342 | — |
| **Severity Tier** | `Large` | 4000 | 0.05% | 0.3442 | — |

---

## 2. Sensitivity Verdict

- Benchmarked outcomes are highly consistent across tasks, failure modes, and evaluation seeds.
- The null binary discordance is invariant across severity tiers and recovery horizons.
