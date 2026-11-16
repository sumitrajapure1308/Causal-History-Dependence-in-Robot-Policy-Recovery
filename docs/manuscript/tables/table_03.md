## Table 3: Admitted Benchmark Scenario Kinematic and Disturbance Statistics
*Data Source: `results/phase_12_stage_c/scenario_manifest.json`*

| Scenario Feature / Metric | Admitted Sample Value ($N=200$) | Pre-Registered Standard | Verification Status |
| :--- | :---: | :---: | :---: |
| **Total Valid Scenarios** | **200** | Exactly 200 (50 per cell) | `Verified` |
| **Mean Peak Yaw Deflection** | **15.62° $\pm$ 18.29°** | $> 14.0°$ (Task 1), $> 8.0°$ (Task 2) | `Verified` |
| **Mean Lateral Trajectory Drift** | **1.72 cm $\pm$ 2.51 cm** | $> 1.6\text{ cm}$ (Task 1), $> 1.2\text{ cm}$ (Task 2) | `Verified` |
| **Mean Remaining Horizon** | **132.6 steps** | $\ge 50$ recovery steps required | `Verified` |
| **Privileged Oracle Recoverability**| **100.0% (200 / 200)** | $R_\text{oracle} = 1.0$ (Unrecoverable excluded) | `Verified` |
| **State Matching Residual Error** | **$D \le 10^{-10}$ (Exact bitwise)** | Zero tolerance for state drift | `Verified` |

---
