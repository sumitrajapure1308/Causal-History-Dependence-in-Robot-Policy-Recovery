# Phase 9 Condition Semantics and Intervention Matrix

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Document:** `docs/methodology/phase_9_condition_semantics.md`  
**Status:** VALIDATED SPECIFICATION  
**Date:** 2026-11-09  

---

## 1. Specification Matrix Across Policies and Conditions

This specification defines the exact tensor and state configuration passed into policy inference at deviation time $t_{\text{dev}}$ across all five experimental conditions ($B0$ through $B4$) for each of the four evaluated policy architectures.

---

### Policy 1: Reactive MLP (`reactive_mlp`)
*Architectural nature:* Non-recurrent feedforward network conditioned strictly on current observation $o_t \in \mathbb{R}^{20}$.

| Condition | Physical State ($qpos, qvel$) | Obs History Buffer | Action History Buffer | Contact History | Policy Hidden State | History-Derived Features | Meaningful? | Implementable? |
|---|---|---|---|---|---|---|---|---|
| **B0** | Exact matched snapshot | N/A | N/A | N/A | None ($\emptyset$) | None ($\emptyset$) | Yes (Baseline) | Yes |
| **B1** | Exact matched snapshot | N/A | N/A | N/A | None ($\emptyset$) | None ($\emptyset$) | **No** (No action input) | NOT APPLICABLE |
| **B2** | Exact matched snapshot | N/A | N/A | N/A | None ($\emptyset$) | None ($\emptyset$) | **No** (No obs buffer) | NOT APPLICABLE |
| **B3** | Exact matched snapshot | N/A | N/A | N/A | None ($\emptyset$) | None ($\emptyset$) | **No** (No hidden state) | NOT APPLICABLE |
| **B4** | Exact matched snapshot | N/A | N/A | N/A | None ($\emptyset$) | None ($\emptyset$) | **Identical to B0** | Yes (Identical) |

---

### Policy 2: Nominal History-Aware GRU (`history_gru`)
*Architectural nature:* Recurrent GRU conditioned on token $[o_t, a_{t-1}] \in \mathbb{R}^{23}$ and hidden state $h_t \in \mathbb{R}^{128}$.

| Condition | Physical State | Obs History Buffer | Action History Buffer | Contact History | Policy Hidden State ($h$) | History-Derived Features | Meaningful? | Implementable? |
|---|---|---|---|---|---|---|---|---|
| **B0** | Exact matched snapshot | Unrolled prefix ($k=10$) | Unrolled prefix ($a_{t_{\text{dev}}-1}$) | N/A | Reconstructed $h(t_{\text{dev}})$ via prefix unroll | None | Yes | Yes |
| **B1** | Exact matched snapshot | Unrolled prefix ($k=10$) | Masked: $a_{t-1} = \mathbf{0}_3$ | N/A | Reconstructed $h(t_{\text{dev}})$ intact | None | Yes (Explicit action mask) | Yes |
| **B2** | Exact matched snapshot | Padded with $o(t_{\text{dev}})$ repeat | Unrolled prefix ($a_{t_{\text{dev}}-1}$) | N/A | Reconstructed $h(t_{\text{dev}})$ intact | None | Yes (Buffer mask) | Yes |
| **B3** | Exact matched snapshot | Unrolled prefix ($k=10$) | Unrolled prefix ($a_{t_{\text{dev}}-1}$) | N/A | **Reset to zero:** $\mathbf{0}_{128}$ | None | Yes (Latent reset) | Yes |
| **B4** | Exact matched snapshot | Padded with $o(t_{\text{dev}})$ repeat | Masked: $a_{t-1} = \mathbf{0}_3$ | N/A | **Reset to zero:** $\mathbf{0}_{128}$ | None | Yes (Direct state injection) | Yes |

---

### Policy 3: Recovery-Augmented MLP (`recovery_augmented_mlp`)
*Architectural nature:* Non-recurrent feedforward network conditioned on augmented vector $x_t \in \mathbb{R}^{24}$ containing base observation $o_t$ (20) plus auxiliary features: failure flag $f_t$ (1), deviation duration $\tau_t$ (1), deviation magnitude $\delta_t$ (1), remaining horizon $H_t$ (1).

| Condition | Physical State | Obs Buffer | Action Buffer | Contact History | Policy Hidden State | History-Derived Features ($f_t, \tau_t, \delta_t$) | Meaningful? | Implementable? |
|---|---|---|---|---|---|---|---|---|
| **B0** | Exact matched snapshot | N/A | N/A | N/A | None ($\emptyset$) | $\tau_t = \tau(t_{\text{dev}})$, $f_t=1$, $\delta_t=\delta_{\text{dev}}$ | Yes | Yes |
| **B1** | Exact matched snapshot | N/A | N/A | N/A | None ($\emptyset$) | Intact | **No** (No action input) | NOT APPLICABLE |
| **B2** | Exact matched snapshot | N/A | N/A | N/A | None ($\emptyset$) | Intact | **No** (No obs buffer) | NOT APPLICABLE |
| **B3** | Exact matched snapshot | N/A | N/A | N/A | None ($\emptyset$) | Intact | **No** (No hidden state) | NOT APPLICABLE |
| **B4** | Exact matched snapshot | N/A | N/A | N/A | None ($\emptyset$) | **Duration reset:** $\tau_t = 0.0$; $f_t, \delta_t$ evaluated on current physical state | Yes (Cold start at matched state) | Yes |

---

### Policy 4: Recovery-Augmented GRU (`recovery_augmented_gru`)
*Architectural nature:* Recurrent GRU conditioned on token $[o_t^{\text{aug}}, a_{t-1}, c_t] \in \mathbb{R}^{28}$ and hidden state $h_t \in \mathbb{R}^{128}$.

| Condition | Physical State | Obs Buffer | Action Buffer | Contact Indicator | Policy Hidden State ($h$) | History-Derived Features | Meaningful? | Implementable? |
|---|---|---|---|---|---|---|---|---|
| **B0** | Exact matched snapshot | Unrolled prefix ($k=10$) | Unrolled prefix ($a_{t_{\text{dev}}-1}$) | Unrolled prefix ($c_{t_{\text{dev}}-1}$) | Reconstructed $h(t_{\text{dev}})$ via prefix unroll | $\tau_t = \tau(t_{\text{dev}})$, $f_t=1$, $\delta_t=\delta_{\text{dev}}$ | Yes (Full preserved memory) | Yes |
| **B1** | Exact matched snapshot | Unrolled prefix ($k=10$) | Masked: $a_{t-1} = \mathbf{0}_3$ | Intact | Reconstructed $h(t_{\text{dev}})$ intact | Intact | Yes (Explicit action mask) | Yes |
| **B2** | Exact matched snapshot | Padded with $o(t_{\text{dev}})^{\text{aug}}$ repeat | Unrolled prefix ($a_{t_{\text{dev}}-1}$) | Intact | Reconstructed $h(t_{\text{dev}})$ intact | Intact | Yes (Obs buffer mask) | Yes |
| **B3** | Exact matched snapshot | Unrolled prefix ($k=10$) | Unrolled prefix ($a_{t_{\text{dev}}-1}$) | Intact | **Reset to zero:** $\mathbf{0}_{128}$ | Intact | Yes (Latent reset) | Yes |
| **B4** | Exact matched snapshot | Padded with $o(t_{\text{dev}})^{\text{aug}}$ repeat | Masked: $a_{t-1} = \mathbf{0}_3$ | Masked: $c_t = 0.0$ | **Reset to zero:** $\mathbf{0}_{128}$ | **Duration reset:** $\tau_t = 0.0$; $f_t, \delta_t$ from current state | Yes (Direct state injection) | Yes |

---

## 2. Invariance and Verification Guarantees

1. **Physical Invariance:** Under all conditions B0–B4, MuJoCo `qpos` and `qvel` are bitwise identical at the onset of recovery, verified by assertion `qpos_err == 0.0` and `qvel_err == 0.0`.
2. **Horizon and Goal Invariance:** Task goal coordinates and remaining steps are strictly invariant across conditions.
3. **Single Consumption Rule:** In condition B0, the prefix unroll processes timesteps $0 \dots t_{\text{dev}}-1$. The first recovery action consumes observation $o(t_{\text{dev}})$ exactly once.

