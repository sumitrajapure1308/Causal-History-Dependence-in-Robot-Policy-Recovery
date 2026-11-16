## Table 4: Main Recovery Results: Primary Binary Success ($B_0$ vs $B_4$)
*Data Source: `results/phase_12_stage_c/analysis/primary_analysis.json`*

| Policy Architecture | $N$ Valid Pairs | $B_0$ Successes | $B_4$ Successes | Discordant ($b+c$) | Discordance Rate [95% Clopper-Pearson CI] | $\Delta R = R_{B0} - R_{B4}$ [95% Bootstrap CI] | McNemar $p_\text{raw}$ | Holm-Bonferroni $p_\text{adj}$ | Verdict |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`reactive_mlp`** | 200 | 2 | 2 | 0 | 0.00% [0.00%, 1.83%] | +0.0000 [+0.0000, +0.0000] | 1.0000 | 1.0000 | `Null (Negative Control)` |
| **`history_gru`** | 200 | 2 | 2 | 0 | 0.00% [0.00%, 1.83%] | +0.0000 [+0.0000, +0.0000] | 1.0000 | 1.0000 | `Null (Bounded)` |
| **`recovery_augmented_mlp`** | 200 | 9 | 3 | 5 | 2.50% [0.82%, 5.74%] | +0.0320 [+0.0130, +0.0540] | 0.0625 | 0.2500 | `Inconclusive (Sub-MDE Trend)` |
| **`recovery_augmented_gru`** | 200 | 2 | 3 | 1 | 0.50% [0.01%, 2.75%] | -0.0010 [-0.0060, +0.0030] | 1.0000 | 1.0000 | `Null (Bounded)` |

---
