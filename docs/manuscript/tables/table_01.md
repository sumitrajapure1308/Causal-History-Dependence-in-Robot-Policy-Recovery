## Table 1: Methodological Comparison with Existing Robot Recovery Benchmarks
*Data Source: Literature Audit & Boundary Specification (`docs/audit/literature_audit.md`)*

| Benchmark | Intervention Type | Physical Failure Modes | State Matching Precision | Negative Control Validation | Hypothesis Unit | Verification Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **RoboRecover (2024)** | Prompt / Trajectory restart | Off-path deviation | None (unmatched) | None | Unpaired rollouts | `Verified` |
| **LIBERO-Recover (2024)** | Task prompt switching | Kinematic stall | Coarse approximate | None | Unpaired rollouts | `Verified` |
| **LIBERO-Pro2.0 (2024)** | Multi-task replay | Object dislodgement | Replay initialization | None | Aggregated trials | `Verified` |
| **Ours (Stage C)** | **Counterfactual Interventions ($B_0–B_4$)** | **Rotational slip, Contact loss** | **Exact Bitwise ($D \le 10^{-10}$)** | **Memoryless MLP (0/200)** | **Scenario-level paired ($N=200$)** | **`Confirmatory`** |

---
