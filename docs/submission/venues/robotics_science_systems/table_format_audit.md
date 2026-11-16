# Table Format and Numerical Integrity Audit: RSS

**Venue:** Robotics: Science and Systems (RSS)  
**Status:** `Verified` | `Venue-specific submission package`  
**Date:** 2026-11-10  

---

## 1. Table Inventory

All 7 publication tables are stored in `results/phase_13/paper_tables.json` and `docs/manuscript/paper_tables.md`.

| Table ID | Title | Key Metrics | Format Standard | Compliance |
|---|---|---|---|---|
| Table 1 | Benchmark Factorial Experimental Design | 2 Tasks x 2 Failures x 4 Policies x 5 Conditions x 5 Seeds | Booktabs, clean rows | `Verified` |
| Table 2 | Primary Binary Recovery Rate Comparison | B0 vs B4 success rates, McNemar p, Holm-Bonferroni p | Booktabs, exact decimals | `Verified` |
| Table 3 | Continuous Goal Distance and Trajectory Metrics | Terminal error, Wilcoxon signed-rank p, Cohen's d | Booktabs, standard errors | `Verified` |
| Table 4 | Mechanistic Divergence Diagnostics | First action divergence, max path drift, hidden norm | Booktabs, p-values | `Verified` |
| Table 5 | Policy Capability Breakdown | Nominal vs recovery success, active correction rate | Booktabs, percentages | `Verified` |
| Table 6 | Multi-Dimensional Robustness Sensitivity Audit | 14 sensitivity dimensions evaluated | Booktabs, status tags | `Verified` |
| Table 7 | Minimum Detectable Effect and Power Matrix | Sample size N=200, MDE=4.8%, power=84% | Booktabs, confidence bounds | `Verified` |

## 2. Numerical Cross-Check
Verified that all numbers across Tables 1-7 match the raw execution logs in `results/phase_12_stage_c/` with bitwise exactness.

---
*Audit certified by Autonomous Agent System.*
