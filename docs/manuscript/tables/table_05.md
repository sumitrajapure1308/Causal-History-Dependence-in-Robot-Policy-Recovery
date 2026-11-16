## Table 5: History-Dependence and Continuous Outcome Analysis
*Data Source: `results/phase_12_stage_c/analysis/continuous_analysis.json`*

| Policy Architecture | Mean $B_0$ Error (m) | Mean $B_4$ Error (m) | Paired Diff $\Delta D$ (m) [95% Bootstrap CI] | Cohen's $d$ | Wilcoxon $p_\text{raw}$ | Wilcoxon $p_\text{adj}$ | Rank-Biserial $r_\text{rb}$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`reactive_mlp`** | 0.3004 | 0.3006 | -0.0002 [-0.0011, +0.0005] | -0.033 | 2.8413e-01 | 1.0000e+00 | +0.101 |
| **`history_gru`** | 0.3002 | 0.3002 | +0.0000 [-0.0000, +0.0001] | +0.094 | 9.7769e-01 | 1.0000e+00 | -0.003 |
| **`recovery_augmented_mlp`** | 0.2950 | 0.3026 | -0.0076 [-0.0156, -0.0003] | -0.137 | 7.1085e-01 | 1.0000e+00 | +0.034 |
| **`recovery_augmented_gru`** | 0.3098 | 0.3092 | +0.0006 [-0.0062, +0.0075] | +0.013 | 9.8844e-01 | 1.0000e+00 | -0.001 |

---
