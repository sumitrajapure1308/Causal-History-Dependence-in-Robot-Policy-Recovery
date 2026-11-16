# Metric Construct Validity and Diagnosis Audit

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Status:** VALIDATED AUDIT  
**Document:** `docs/audit/metric_construct_validity.md`  
**Date:** 2026-11-09  

---

## 1. Disentangling Evaluation Constructs

In robotics recovery literature, evaluation metrics are often conflated under broad labels such as "detection rate" or "diagnosis accuracy." To ensure construct validity, we formally distinguish five separate operational constructs:

| Construct Level | Operational Definition | Agent / Evaluator | Availability in Current Policies |
|---|---|---|---|
| **1. Ground-Truth Failure Label** | Omniscient environment state flag indicating whether a physical perturbation was applied or dynamic slip occurred ($y \in \{0, 1\}$). | Simulation Harness | Privileged Ground Truth |
| **2. External Detector** | Algorithmic threshold test operating on environment observations ($|\text{yaw}| > 15^\circ$ or lateral drift $> 0.025\text{ m}$). | Evaluation Script | External Evaluator |
| **3. Policy-Emitted Detection** | Explicit classification head or binary output scalar emitted by the policy model predicting failure onset. | Policy Model | **NOT IMPLEMENTED** (Policies output motor action deltas only) |
| **4. Policy-Emitted Diagnosis** | Multi-class categorical distribution emitted by the policy predicting the exact physical failure mode (e.g. slip vs. jamming vs. boundary collision). | Policy Model | **NOT AVAILABLE** (No diagnosis classification head exists) |
| **5. Post-Hoc Behavioral Proxy** | Retrospective classification of the executed trajectory based on kinematic action heuristics (e.g., retraction $a_x < -0.002$ or turning $|a_y| > 0.003$). | Evaluation Script | Unprivileged Behavioral Heuristic |

### Critical Finding on Past Logging:
In Phase 7, the rollout logger in `validate_recovery_capability.py` recorded:
```python
"detection_rate": 1.0,
"diagnosis_rate": 1.0,
```
These fields were hardcoded constants in the evaluation dictionary, not measurements from policy heads. Reporting these as policy capabilities is invalid. All diagnosis metrics for the current policy suite must be labeled **NOT AVAILABLE**.

---

## 2. Investigation of 25% Success vs. 5% Corrective Action Mismatch

In the Phase 7 capability validation on $N=20$ unique scenarios, `recovery_augmented_gru` achieved:
- **Task Success Rate:** 5 / 20 (25.0%)
- **Corrective-Action Rate:** 1 / 20 (5.0%)

### Empirical Action Rule Under Audit:
The corrective action heuristic was:
$$\text{Corrective Action Detected} \iff \exists t \in [0, T_{\text{rem}}]: \quad a_x(t) < -0.002 \quad \lor \quad |a_y(t)| > 0.003$$

### Rollout Trace Inspection of the 5 Successes:

```
Scenario 1 (scen_history_gru_s49_t53_a2060d):
  - Outcome: SUCCESS (t = 54 steps)
  - Action Profile: ax in [+0.001, +0.004], ay peaked at +0.0034 at t = 12.
  - Heuristic Result: CORRECTIVE ACTION DETECTED (ay > 0.003). Active steering maneuver.

Scenario 2 (scen_history_gru_s91_t58_aaa2eb):
  - Outcome: SUCCESS (t = 62 steps)
  - Action Profile: ax in [+0.002, +0.005], ay peaked at +0.0018.
  - Heuristic Result: NO CORRECTIVE ACTION. Yaw perturbation was mild (16.2 deg). Forward push grazed cube forward-right, entering the 4 cm target radius without crossing the 0.003 ay threshold.

Scenario 4 (scen_history_gru_s112_t49_ff2be3):
  - Outcome: SUCCESS (t = 58 steps)
  - Action Profile: ax in [+0.003, +0.006], ay peaked at +0.0014.
  - Heuristic Result: NO CORRECTIVE ACTION. Cube slid across pusher face into goal alignment.

Scenario 7 (scen_history_gru_s196_t52_41373d):
  - Outcome: SUCCESS (t = 65 steps)
  - Action Profile: ax in [+0.002, +0.004], ay peaked at -0.0011.
  - Heuristic Result: NO CORRECTIVE ACTION. Shallow forward push succeeded passively.

Scenario 15 (scen_history_gru_s385_t50_4ccf26):
  - Outcome: SUCCESS (t = 72 steps)
  - Action Profile: ax in [+0.003, +0.005], ay peaked at +0.0021.
  - Heuristic Result: NO CORRECTIVE ACTION. Pusher gently nudged tilted cube directly to goal.
```

### Mechanism Analysis:
The heuristic rule ($a_x < -0.002$ or $|a_y| > 0.003$) was calibrated to detect **aggressive, high-amplitude corrective maneuvers** (such as explicit back-off retractions or sharp orthogonal turns). In four of the five successful episodes, recovery was achieved via **gentle, low-amplitude steering adjustments** ($|a_y| \in [0.0011, 0.0021]$) that stayed beneath the arbitrary $0.003$ threshold.

---

## 3. Rejection of the Mandatory Linear Probability Chain

Prior literature often conceptualizes recovery as a rigid probabilistic pipeline:
$$P(\text{Recovery}) = P(\text{Detect}) \times P(\text{Diagnose} \mid \text{Detect}) \times P(\text{Correct} \mid \text{Diagnose})$$
This decomposition is conceptually flawed for end-to-end continuous neural policies for three reasons:
1. **Implicit Recovery:** A policy can successfully correct a disturbance continuously through closed-loop feedback without ever forming an explicit discrete diagnosis classification.
2. **Unobservable Stages:** Forcing intermediate stage probabilities when the architecture does not emit detection or diagnosis tokens produces fabricated metrics.
3. **Single-Class Triviality:** Evaluating "diagnosis" in an environment with only one failure mode (rotational slip) reduces diagnosis to detection, offering zero scientific evidence of multi-mode diagnostic competence.

**Guideline for Benchmark Evaluation:** Recovery performance must be quantified using directly observable continuous metrics: final goal distance, final orientation error, control effort, and binary goal achievement.

