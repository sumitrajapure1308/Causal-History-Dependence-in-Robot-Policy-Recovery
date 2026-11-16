# Related Work Comparison Matrix

This matrix provides a comprehensive comparison between existing robot manipulation benchmarks, recovery frameworks, and the proposed **Causal-History Matched-State Protocol**.

---

## Comparison Table

| Feature / Dimension | Standard LIBERO / RoboTwin | Initial-State Perturbation (e.g. LIBERO-Plus) | LIBERO-Recover | RoboRecover (arXiv:2409.28952) | LIBERO-Pro / Pro2.0 | **Proposed Protocol (Causal History Recovery)** |
|---|---|---|---|---|---|---|
| **Failure Origin** | None (Nominal execution) | External static scene shifts | Natural / reconstructed failures | Replayed execution deviations | Static perturbations & runtime interventions | **Controlled: Policy-induced, replayed prefix, & matched state injection** |
| **History Preserved?** | N/A | No (Starts from perturbed $t=0$) | Partly (Scenario-dependent) | Yes (Prefix replay) | Varies (Perturbation injected mid-task) | **Rigidly Controlled (Condition A, B, C, D)** |
| **Physical State Matched?** | No | Initial scene pose only | Scenario-dependent | Fixed recovery start point | Not primary objective | **Yes: Rigorous weighted distance $d(s_1, s_2) \le \epsilon$** |
| **Action Prefix Isolated?** | No | No | No | Confounded with state | Confounded with runtime shift | **Yes: Isolates action prefix from physical state** |
| **Failure Detection Evaluated?** | No | No | Implicit | No | Implicit | **Yes: AUROC, AUPRC, detection delay $D_{\text{delay}}$, Brier score** |
| **Failure Diagnosis Evaluated?** | No | No | Partly (Recovery tiers) | Limited | Limited | **Yes: Multi-class failure & contact mode accuracy** |
| **Recovery Decomposition?** | No | No | 4 Recovery Levels | No (Task success from dev state) | Task completion after disturbance | **Yes: $P(F) = P(D)P(Z \mid D)P(C \mid Z,D)P(P \mid C,Z,D)P(F \mid P,C,Z,D)$** |
| **Causal History Metric ($H_R$)?**| No | No | No | No | No | **Yes: $H_R = R_{\text{replay}} - R_{\text{injected}}$ and $H_R^{\text{abs}}$** |
| **Policy-Ranking Stability?** | Nominal rank only | Static shift rank | Level-wise rank | Deviation rank only | Robustness rank drop | **Yes: Cross-protocol correlation ($\tau, \rho$) and rank-reversal frequency** |
| **Recoverability Ground Truth?**| Trivial (Nominal) | Heuristic | Heuristic | Trajectory validity filter | Human review | **Yes: Privileged oracle controller execution filter** |
| **Sim-to-Real Scope Claim** | Sim / Real | Sim / Real | Sim / Real | Sim | Sim | **Simulation-only counterfactual validity audit** |

---

## Detailed Comparative Analysis

### 1. Standard Benchmarks vs. Causal History Evaluation
Conventional benchmarks (standard LIBERO, Meta-World, RoboTwin) evaluate policies exclusively from nominal starting states. While essential for establishing basic manipulation competence, they cannot evaluate error correction or distribution shifts occurring during closed-loop execution.

### 2. Static Perturbations vs. Runtime Deviations
Benchmarks like LIBERO-Plus introduce static perturbations (lighting, table textures, object repositioning) at $t=0$. These do not capture dynamic execution errors where the robot's own interaction causes slippage, tipping, or partial misalignments.

### 3. LIBERO-Recover vs. Proposed Protocol
LIBERO-Recover classifies recovery into four hierarchical levels (Action Retry, Action Adaptation, Object State Recovery, Environmental Recovery). However, it does not isolate physical state equivalence from causal history. An agent facing an "object state recovery" scenario in LIBERO-Recover is dropped into a preset environment configuration; it does not evaluate whether that same configuration reached through previous policy errors alters recovery competence.

### 4. RoboRecover vs. Proposed Protocol
RoboRecover represents the closest existing baseline. It correctly recognizes that execution deviations are critical and reconstructs intermediate deviation states via action-prefix replay. However:
- RoboRecover evaluates recovery **only under prefix replay** (Condition B).
- It treats the replayed state as the baseline evaluation unit, implicitly assuming that recovery depends only on being at that intermediate state.
- It **does not** perform counterfactual state-matched injection without history (Condition C).
- It **does not** evaluate the difference metric $H_R = R_{\text{replay}} - R_{\text{injected}}$.
- It does not decompose recovery into separate detection, diagnosis, and action selection stages.
Our proposed work takes RoboRecover as a direct baseline and asks the unresolved scientific question: *Does the policy recover because of the physical state, or because of the action prefix that led to it?*

### 5. LIBERO-Pro / LIBERO-Pro2.0 vs. Proposed Protocol
LIBERO-Pro2.0 evaluates 22 static and 20 runtime interventions across 6 dimensions. While comprehensive in cataloging disturbance types, its evaluation focuses on robustness score degradation under external interventions rather than controlled causal-history counterfactual testing with matched physical configurations.

