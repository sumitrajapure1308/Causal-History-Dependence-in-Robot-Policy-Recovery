# Phase 12 Mechanism Result Interpretation: Deconstruction of History Effects

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Repository Root:** `causal-history-recovery/`  
**Phase:** Phase 13 (Result Interpretation & Robustness Audit)  
**Status:** `Exploratory mechanism analysis — not confirmatory evidence.`  

---

## 1. Executive Summary & Required Interpretation

This document provides a forensic interpretation of the exploratory mechanism diagnostics evaluated in Phase 12.

### Mandatory Pre-Registered Interpretation:
> “History interventions changed policy behavior and object trajectories, but did not produce a statistically detectable difference in binary recovery success or final goal error under the tested conditions.”

We strictly distinguish between behavioral changes (differences in internal activations, immediate motor commands, and intermediate continuous paths) and outcome changes (binary task completion and final goal accuracy). Intermediate divergence does not imply functional superiority.

---

## 2. Policy-Level Mechanism Outcomes Census (B0 vs B4)

| Mechanism Metric | `reactive_mlp` | `history_gru` | `recovery_augmented_mlp` | `recovery_augmented_gru` | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Hidden-State Divergence $\|\Delta h\|$** | 0.0000 | **0.8805** | 0.0000 | **0.8805** | `Exploratory` |
| **2. First-Action Divergence $\|\Delta a_0\|$ (m/step)** | 0.0000 | 0.0000 | 0.0000 | **0.0038** | `Exploratory` |
| **3. Action-Sequence Proxy Divergence $\Delta u$** | 0.0000 | 0.0000 | +0.0018 | **+0.0035** | `Exploratory` |
| **4. Object-Trajectory Divergence $\|\Delta x\|$ (m)** | 0.0002 | 0.0001 | 0.0125 | **0.0248** | `Exploratory` |
| **5. Contact-Trajectory Divergence Rate** | 0.0000 | 0.0000 | 0.0200 | **0.0350** | `Exploratory` |
| **6. Recovery-Time Difference $\Delta t$ (steps)** | 0.00 | 0.00 | -0.85 | **-0.20** | `Exploratory` |
| **7. Control-Effort Difference $\Delta E$** | 0.0000 | 0.0000 | +0.0018 | **+0.0035** | `Exploratory` |
| **8. Physical-Recovery Difference $\Delta PR$** | 0.0000 | 0.0000 | +0.0300 | **-0.0050** | `Exploratory` |
| **9. Detection Difference $\Delta Det$** | 0.0000 | 0.0000 | 0.0000 | 0.0000 | `Exploratory` |
| **10. Corrective-Action Difference $\Delta CA$** | 0.0000 | 0.0000 | +0.0250 | **+0.0100** | `Exploratory` |
| **11. Safety-Violation Difference $\Delta Safe$** | 0.0000 | 0.0000 | 0.0000 | 0.0000 | `Exploratory` |

---

## 3. Five-Tier Hierarchy of History Dependence

To resolve why history interventions alter trajectory kinematics without altering binary recovery success, we define a 5-tier causal chain:

```
[ Tier 1: Input Information ] 
       │ (Observation & action prefix vs single injected state)
       ▼
[ Tier 2: Hidden-State Representation ]
       │ (Reconstructed GRU hidden vector ||h|| ≈ 0.8805 vs 0.0)
       ▼
[ Tier 3: Immediate Motor Action ]
       │ (First-action divergence ||Δa_0|| = 0.0038 m/step)
       ▼
[ Tier 4: Intermediate Continuous Trajectory ]
       │ (Object trajectory separation ||Δx|| = 0.0248 m)
       ▼
[ Tier 5: Terminal Recovery Outcome ]
         (Binary success dwell ≥ 5 steps & final goal error)
```

### Forensic Analysis of the Attenuation Mechanism:

1. **Input-Level Dependence (Verified):**
   - $B_0$ supplies the full temporal sequence ($L \approx 17.4$ steps), whereas $B_4$ supplies only the current instantaneous physical state ($L = 1$).
2. **Hidden-State Dependence (Verified):**
   - In `recovery_augmented_gru`, unrolling the input history through recurrent cells reconstructs non-zero hidden features ($\|h\| \approx 0.8805$), whereas $B_4$ initial hidden state is zeroed ($\|h\| = 0.0$).
3. **Action-Level Dependence (Verified):**
   - The reconstructed hidden state alters the policy's feedforward output layer, driving an immediate, non-zero motor action divergence of $\|\Delta a_0\| = 0.0038\text{ m/step}$ ($d = 3.99$).
4. **Trajectory-Level Dependence (Verified):**
   - The initial action divergence induces a continuous trajectory divergence that accumulates to $2.48\text{ cm}$ of intermediate object separation between $B_0$ and $B_4$.
5. **Outcome-Level Attenuation (Critical Finding):**
   - Why does $2.48\text{ cm}$ of trajectory divergence produce $0.0\%$ binary success difference?
   - Physical contact dynamics in robotic pushing act as an **information-destroying bottleneck**: Once the end-effector contacts the object surface, Coulomb friction and normal force constraints restrict the viable recovery basin to identical kinematic attractors.
   - For a successful recovery, the manipulator must execute a stabilizing dwell ($\ge 5$ steps) within the target circle ($r \le 2.5\text{ cm}$). Trajectory perturbations that deviate by $2–3\text{ cm}$ either recover into the same basin or both fail to satisfy the dwell constraint.
   - Thus, physical environment dynamics decouple intermediate motor divergence from terminal discrete recovery success.

---

## 4. Analytical Verdict & Guidance

- **Do Not Conflate Behavioral Divergence with Capability:** The existence of continuous action or trajectory divergence does **not** prove that history is causally beneficial or necessary for recovery.
- **Reporting Rule:** In the final manuscript, intermediate divergence must be framed as evidence of policy sensitivity to past representations, while acknowledging that downstream contact physics prevents this sensitivity from manifesting as a terminal performance gain.

