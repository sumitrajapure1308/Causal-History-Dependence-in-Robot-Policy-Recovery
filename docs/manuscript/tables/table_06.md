## Table 6: Counterfactual History Intervention Ablation Across Conditions B0–B4
*Data Source: `results/phase_12_stage_c/evaluation_summary.json`*

| Policy Architecture | $B_0$ Unrolled (%) | $B_1$ Mask Act (%) | $B_2$ Mask Obs (%) | $B_3$ Mask All (%) | $B_4$ Matched Inj (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`reactive_mlp`** | 1.00% | 1.00% | 1.00% | 1.00% | 1.00% |
| **`history_gru`** | 1.00% | 1.00% | 1.00% | 1.00% | 1.00% |
| **`recovery_augmented_mlp`** | 4.70% | 2.50% | 1.90% | 2.10% | 1.50% |
| **`recovery_augmented_gru`** | 1.20% | 1.40% | 1.10% | 1.00% | 1.30% |

---
