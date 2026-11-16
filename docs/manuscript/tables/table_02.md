## Table 2: Stage C Factorial Experimental Design Matrix
*Data Source: Frozen Pre-Registration (`docs/methodology/phase_12_stage_c_preregistration.md`)*

| Design Factor | Levels ($K$) | Description / Values | Verification Status |
| :--- | :---: | :--- | :---: |
| **Tasks ($T$)** | 2 | `task1_cube` (PushTargetEnv), `task2_puck` (SecondPushTaskEnv) | `Verified` |
| **Failure Modes ($F$)** | 2 | `rotational_slip` (angular drift), `contact_loss` (transient stall) | `Verified` |
| **Policy Architectures ($P$)** | 4 | `reactive_mlp`, `history_gru`, `recovery_augmented_mlp`, `recovery_augmented_gru` | `Verified` |
| **Counterfactual Conditions ($C$)** | 5 | $B_0$ (Unrolled prefix), $B_1$ (Mask act), $B_2$ (Mask obs), $B_3$ (Mask both), $B_4$ (Matched injection) | `Verified` |
| **Evaluation Seeds ($S$)** | 5 | `15001, 15002, 15003, 15004, 15005` (Replicate stability) | `Verified` |
| **Scenarios ($N$)** | 200 | 50 scenarios per cell $\times$ 4 factorial cells (Disjoint seeds $\ge 10000$) | `Verified` |
| **Total Rollout Records** | **20,000** | $2 \times 2 \times 4 \times 5 \times 5 \times 50 = 20,000$ complete records | `Verified` |

---
