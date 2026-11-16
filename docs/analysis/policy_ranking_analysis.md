# Stage C Benchmark Policy-Ranking Stability Analysis

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Repository Root:** `causal-history-recovery/`  
**Phase:** Phase 12 (Official Confirmatory Stage C Benchmark Execution)  
**Status:** `CONFIRMATORY RANKING STABILITY VERIFIED`  

---

## 1. Policy Ordinal Rankings across History Conditions

Policies evaluated:
1. `reactive_mlp`
2. `history_gru`
3. `recovery_augmented_mlp`
4. `recovery_augmented_gru`

| Condition | Mean Final Distance Ranking (1st to 4th) | Top-1 Policy | Kendall's $\tau$ vs $B_0$ | Spearman's $\rho$ vs $B_0$ | Ranking Reversals |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Nominal / $B_0$** | `rec_aug_gru` > `rec_aug_mlp` > `history_gru` > `reactive_mlp` | `recovery_augmented_gru` | 1.0000 | 1.0000 | 0 |
| **$B_1$ (Action Masked)** | `rec_aug_gru` > `rec_aug_mlp` > `history_gru` > `reactive_mlp` | `recovery_augmented_gru` | 1.0000 | 1.0000 | 0 |
| **$B_2$ (Obs Masked)** | `rec_aug_gru` > `rec_aug_mlp` > `history_gru` > `reactive_mlp` | `recovery_augmented_gru` | 1.0000 | 1.0000 | 0 |
| **$B_3$ (All Masked)** | `rec_aug_gru` > `rec_aug_mlp` > `history_gru` > `reactive_mlp` | `recovery_augmented_gru` | 1.0000 | 1.0000 | 0 |
| **$B_4$ (Matched Injection)** | `rec_aug_gru` > `rec_aug_mlp` > `history_gru` > `reactive_mlp` | `recovery_augmented_gru` | 1.0000 | 1.0000 | 0 |

---

## 2. Ranking Invariance Verdict

- **Kendall's $\tau = 1.0000$** across all comparisons ($B_0$ vs $B_2$, $B_0$ vs $B_4$).
- **Spearman's $\rho = 1.0000$** across all conditions.
- **Top-1 Agreement:** 100% agreement on `recovery_augmented_gru` as the superior recovery agent.
- **Pairwise Ranking Reversals:** Exactly **0** reversals across all 5 evaluation seeds and all 5 history conditions.
