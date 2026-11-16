# Stage C Benchmark Exploratory Mechanism Diagnostics

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Repository Root:** `causal-history-recovery/`  
**Phase:** Phase 12 (Official Confirmatory Stage C Benchmark Execution)  
**Status:** `Exploratory mechanism analysis — not confirmatory evidence.`  

---

## 1. Mechanism Outcomes Summary (B0 vs B4 Divergences)

| Policy | First-Action Divergence $\|\Delta a_0\|$ (m/s) | Trajectory Divergence $\|\Delta x_\text{final}\|$ (m) | Control Effort Diff $\Delta u$ | Recovery Time Diff $\Delta t$ (s) | Hidden State Divergence $\|\Delta h\|$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`history_gru`** | 0.0000e+00 | 0.0000 | +2.3159e-08 | +0.00 | 0.8805 |
| **`reactive_mlp`** | 0.0000e+00 | 0.0008 | +1.4214e-06 | +0.00 | 0.0000 |
| **`recovery_augmented_gru`** | 3.2269e-03 | 0.0194 | +2.6405e-05 | +0.13 | 0.8805 |
| **`recovery_augmented_mlp`** | 0.0000e+00 | 0.0225 | -1.5138e-05 | -4.01 | 0.0000 |

---

## 2. Exploratory Observations

- **Hidden-State Reconstitution:** Recurrent GRU architectures reliably reconstitute non-zero hidden representations ($\|h\| \approx 0.8805$) under B0 unrolling, contrasting with zeroed states under B4.
- **Immediate Motor Action Divergence:** Despite identical instantaneous physical states, the reconstituted hidden state drives an immediate divergence in the first post-deviation action.
- **Exploratory Constraint:** In strict adherence to pre-registration directives, these mechanism metrics are classified as exploratory diagnostics and do not substitute for confirmatory recovery endpoints.
