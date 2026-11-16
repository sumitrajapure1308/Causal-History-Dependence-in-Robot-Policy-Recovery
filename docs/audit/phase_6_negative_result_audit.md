# Phase 6 Negative-Result Audit: Causal-History Invariance & Policy Incapacity

> **Document Type:** Scientific Failure Analysis & Root Cause Audit  
> **Project Title:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
> **Phase:** 7 (Audit of Phase 6 Negative Results)  
> **Date:** 2026-11-09  
> **Status:** `Verified`  
> **Scientific Mandate:** Do not claim that history does not matter. The verified conclusion is:  
> *“The pilot did not detect history dependence, but the policies may lack sufficient recovery capability to reveal it.”*

---

## 1. Executive Summary of Phase 6 Outcome

Phase 6 executed a pre-registered evaluation across 1,140 rollouts (38 scenarios $\times$ 5 counterfactual history conditions $\times$ 3 seeds $\times$ 2 policies). The primary causal history effect was observed to be:
$$H_R(\pi_{\text{MLP}}) = 0.0000 \quad (95\%\text{ CI: } [0.0000, 0.0000], p = 1.0000)$$
$$H_R(\pi_{\text{GRU}}) = 0.0000 \quad (95\%\text{ CI: } [0.0000, 0.0000], p = 1.0000)$$

While for [`ReactiveMLPPolicy`](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/src/causal_history_recovery/policies/reactive_mlp.py) this null effect is mathematically guaranteed by its memoryless architecture ($k=0$), for [`HistoryGRUPolicy`](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/src/causal_history_recovery/policies/history_gru.py) this was an unexpected empirical invariance.

This audit investigates the structural, algorithmic, and data-distributional causes underlying this result.

---

## 2. Policy-by-Policy Metric Report

| Metric Dimension | Reactive MLP Baseline | History-Aware GRU Baseline | Privileged Geometric Oracle |
|---|---|---|---|
| **Nominal Success Rate (Phase 3/4)** | 20.0% (10 / 50 demos) | 30.0% (15 / 50 demos) | 100.0% (50 / 50 demos) |
| **Recovery Success Rate (Phase 6)** | **2.63%** (3 / 114 rollouts) | **5.26%** (6 / 114 rollouts) | **100.0%** (38 / 38 admitted) |
| **Recovery Success by Condition (B0)** | 2.63% (3 / 114) | 5.26% (6 / 114) | 100.0% |
| **Recovery Success by Condition (B1)** | 2.63% (3 / 114) | 5.26% (6 / 114) | 100.0% |
| **Recovery Success by Condition (B2)** | 2.63% (3 / 114) | 5.26% (6 / 114) | 100.0% |
| **Recovery Success by Condition (B3)** | 2.63% (3 / 114) | 5.26% (6 / 114) | 100.0% |
| **Recovery Success by Condition (B4)** | 2.63% (3 / 114) | 5.26% (6 / 114) | 100.0% |
| **Recovery Success by Seed (42)** | 2.63% (1 / 38) | 5.26% (2 / 38) | 100.0% |
| **Recovery Success by Seed (500)** | 2.63% (1 / 38) | 5.26% (2 / 38) | 100.0% |
| **Recovery Success by Seed (2000)** | 2.63% (1 / 38) | 5.26% (2 / 38) | 100.0% |
| **Small Severity Tier ($N=36$)** | 0.00% (0 / 36) | 8.33% (3 / 36) | 100.0% |
| **Medium Severity Tier ($N=60$)** | 0.00% (0 / 60) | 0.00% (0 / 60) | 100.0% |
| **Large Severity Tier ($N=18$)** | 16.67% (3 / 18) | 16.67% (3 / 18) | 100.0% |
| **Recovery Success: Horizon $< 90$** | 0.00% (0 / 18) | 0.00% (0 / 18) | 100.0% |
| **Recovery Success: Horizon $90 - 105$** | 0.00% (0 / 60) | 5.00% (3 / 60) | 100.0% |
| **Recovery Success: Horizon $> 105$** | 8.33% (3 / 36) | 8.33% (3 / 36) | 100.0% |
| **Initial Object Pose Sensitivity** | Center-biased ($\sigma_x \approx 0$) | Center-biased ($\sigma_x \approx 0$) | Robust to $\pm 5\text{ cm}$ |
| **Contact Configuration** | Single-face planar push | Single-face planar push | Multi-face realignment |
| **Failure Detection Rate** | 100.0% (automated slip rule) | 100.0% (automated slip rule) | N/A (Privileged) |
| **Diagnosis Rate (Slip Classification)** | 100.0% ($38 / 38$) | 100.0% ($38 / 38$) | N/A (Privileged) |
| **Corrective-Action Rate** | **0.0%** (No active turning) | **0.0%** (No active turning) | 100.0% (Active realignment) |
| **Physical Recovery Rate** | 2.63% (incidental) | 5.26% (incidental) | 100.0% (True realignment) |
| **Final Task Success Rate** | 2.63% | 5.26% | 100.0% |
| **Mean Control Effort** | 0.001095 | 0.001076 | 0.001250 |
| **Action Saturation ($|a| > 0.019$)** | 0.0% | 0.0% | 5.2% |
| **Action Variance ($\sigma_a^2$)** | $3.1 \times 10^{-6}$ | $3.1 \times 10^{-6}$ | $2.4 \times 10^{-4}$ |
| **Recurrent Hidden State Variance** | N/A ($k=0$) | **$0.0000$** | N/A |
| **GRU Hidden State Norm ($\|\mathbf{h}\|$)** | N/A | **$0.0000$** | N/A |
| **GRU Hidden Change ($\Delta \mathbf{h}$)** | N/A | **$0.0000$** | N/A |

---

## 3. Deep Root-Cause Analysis: Why History Dependence Was Not Detected

A forensic audit of model checkpoints and execution logs revealed two decisive structural mechanisms:

### 3.1 Network Degeneracy via Nominal Behavioral Cloning
Inspection of [`history_gru_best.pt`](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/models/checkpoints/history_gru_best.pt) revealed that the trained GRU layer weights collapsed to near-zero machine precision:
- `gru.weight_ih_l0` mean absolute magnitude: $3.25 \times 10^{-38}$
- `gru.weight_hh_l0` mean absolute magnitude: $3.23 \times 10^{-38}$
- `fc_head.2.bias`: $+0.0594$ (yielding a constant forward push $a_x \approx 0.0034\text{ m/step}$)

**Mechanism:** Because the policy was trained exclusively on 50 nominal expert trajectories where the block moves monotonically along the $+x$ axis without deviation, minimizing MSE over the nominal demonstrations incentivized the optimizer to bypass the recurrent weights and rely entirely on static forward bias. Consequently, the GRU hidden state $\mathbf{h}(t)$ remained uniformly near zero throughout the entire rollout ($\|\mathbf{h}\| \approx 0.0000$).

### 3.2 Total Absence of Corrective Maneuvering Behaviors
When an off-center contact perturbation occurs, the block rotates ($> 25^\circ$ yaw) and drifts laterally ($> 3\text{ cm}$). A recovery-capable policy must:
1. Retract the pusher or slide laterally around the rotated block.
2. Re-establish contact on the opposite lateral face.
3. Apply counter-torque to eliminate yaw misalignment.
4. Drive the block into the goal radius ($0.06\text{ m}$) and maintain contact for $\ge 5$ dwell steps.

Neither the Reactive MLP nor the History GRU possessed these behaviors. When perturbed, both policies continued executing open-loop forward pushes straight ahead. In 108 out of 114 cases, this constant forward push simply pushed past the block or pushed it further off-axis. Only in 6 cases (large perturbations where the rotated block rotated back into the pusher's forward path) did the forward push accidentally knock the block into the goal zone.

---

## 4. Evidence Analysis

### Evidence that Recovery is Physically Possible:
- The Privileged Oracle achieved **100% recovery** ($38 / 38$ admitted scenarios, $R_{\text{oracle}} == 1.0$) from the identical physical failure snapshots $s(t_d)$, proving that failure states were physically recoverable within remaining horizons ($T_{\text{rem}} \ge 70$ steps).

### Evidence that the Policy Fails Due to Incapacity (Not Physical Impossibility):
- The policy action variance was $3.1 \times 10^{-6}$, indicating almost zero behavioral adaptation between nominal and post-failure states.
- The corrective-action rate was $0.0\%$: neither policy ever reversed direction ($a_x < 0$) or initiated lateral correction ($|a_y| > 0.005$).

### Evidence of History Neglect in Nominal GRU:
- Because the GRU recurrent weights vanished during nominal behavioral cloning, the recurrent hidden state remained invariant ($\|\mathbf{h}\| \approx 0$), making the GRU functionally indistinguishable from a memoryless bias controller.
- Ablating history (B1, B2, B3, B4) produced zero change in action outputs because the policy was not reading from history.

---

## 5. Audit Conclusion

The scientific conclusion of this audit is:

> **“The pilot did not detect history dependence, but the policies may lack sufficient recovery capability to reveal it.”**

To measure whether history causally aids or hinders recovery, the evaluated policies must possess the **capacity to attempt recovery**. Phase 7 therefore requires implementing and training a **Recovery-Augmented Policy Suite** conditioned on recovery-specific demonstration data.

