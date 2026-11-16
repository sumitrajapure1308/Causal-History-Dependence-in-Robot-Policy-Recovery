# Staged History Interventions & Ablation Protocol

> **Specification Standard:** Fine-Grained History Disentanglement  
> **Status:** Formal Specification Frozen (Methodology Specification Only; Not Implemented in Phase 1)  
> **Scope:** Defines progressive ablation tiers to isolate which specific history component drives recovery differences.

---

## 1. Disentanglement Principles & Causal Hygiene

When comparing a replayed failure state with an injected failure state, a naive reset of "all history" constitutes a **bundled, multi-factor intervention**. If performance differs between full-history replay and a bare state reset, the divergence could stem from:
1. Loss of previous action sequence information ($H^a$).
2. Loss of previous visual/proprioceptive observation buffers ($H^o$).
3. Loss of internal recurrent memory / hidden activations ($h^{\pi}$).
4. Disruption of contact normal/shear force evolution ($H^c$).

To prevent confounding, we structure the causal interventions into **staged, single-stream ablation conditions** ($B0 \to B4$).

> **Critical Methodological Rule:** Condition $B4$ is explicitly defined as a **combined multi-stream intervention**. It must NEVER be interpreted as evidence regarding any single history component in isolation.

---

## 2. Condition-by-Condition Staged Intervention Specification

### Condition B0: Full Preserved History (Reference Baseline)
- **Physical state ($s_t$):** Reached via exact prefix replay $a_{0:t_d-1}$ from seed $\xi_0$.
- **Observation history ($H^o$):** Full original observation sequence $(o_0, o_1, \dots, o_{t_d})$.
- **Action history ($H^a$):** Full original action prefix $(a_0, a_1, \dots, a_{t_d-1})$.
- **Contact history ($H^c$):** Continuous physical contact progression accumulated during replay.
- **Policy hidden state ($h^{\pi}$):** Unrolled continuously through the prefix: $h_{t_d}^{\pi} = \text{RNN}(h_{t_d-1}^{\pi}, o_{t_d}, a_{t_d-1})$.
- **Random-number state ($\xi$):** Synchronized to RNG state at $t_d$.
- **Remaining horizon ($\Delta t_{\text{remain}}$):** Strictly enforced as $T - t_d$.
- **Goal state ($g$):** Identical task goal $g$.
- **Purpose:** Represents the natural history baseline (RoboRecover equivalent).
- **Possible confounds:** Policy might overfit to the specific action prefix timing rather than true failure cues.

---

### Condition B1: Action History Removed (Ablation: No Action Memory)
- **Physical state ($s_t$):** Identical matched physical state $s(t_d)$ reached via prefix replay.
- **Observation history ($H^o$):** Preserved: $(o_0, o_1, \dots, o_{t_d})$.
- **Action history ($H^a$):** **REMOVED / ZEROED:** Action buffer is masked or zeroed ($a_{\text{hist}} = \mathbf{0}$).
- **Contact history ($H^c$):** Preserved physical contacts.
- **Policy hidden state ($h^{\pi}$):** Unrolled using observations only (with zeroed action inputs if model is conditioned on actions).
- **Random-number state ($\xi$):** Synchronized to seed at $t_d$.
- **Remaining horizon ($\Delta t_{\text{remain}}$):** $T - t_d$.
- **Goal state ($g$):** Identical task goal $g$.
- **Purpose:** Tests whether awareness of *what the robot did* (proprioceptive motor commands) aids recovery beyond seeing what happened.
- **Possible confounds:** For policies trained with action-conditioning, feeding zeroed actions represents an out-of-distribution input shift.

---

### Condition B2: Observation History Removed (Ablation: No Visual/Proprioceptive Buffer)
- **Physical state ($s_t$):** Identical matched physical state $s(t_d)$ reached via prefix replay.
- **Observation history ($H^o$):** **REMOVED:** History buffer is cleared or repeated; only instantaneous observation $o_{t_d}$ is provided ($k=1$).
- **Action history ($H^a$):** Preserved: $(a_0, \dots, a_{t_d-1})$.
- **Contact history ($H^c$):** Preserved physical contacts.
- **Policy hidden state ($h^{\pi}$):** Initialized from blank $h_0$ and fed only instantaneous $o_{t_d}$.
- **Random-number state ($\xi$):** Synchronized to seed at $t_d$.
- **Remaining horizon ($\Delta t_{\text{remain}}$):** $T - t_d$.
- **Goal state ($g$):** Identical task goal $g$.
- **Purpose:** Isolates the contribution of perceptual temporal context (optical flow, velocity trends, slip onset).
- **Possible confounds:** Instantaneous single frames cannot convey object velocity unless explicitly provided in low-dim states.

---

### Condition B3: Policy Hidden State Reset (Ablation: Memory Blanking)
- **Physical state ($s_t$):** Identical matched physical state $s(t_d)$ reached via prefix replay.
- **Observation history ($H^o$):** Short window $k$ provided, but internal recurrent hidden activations $h_t^{\pi}$ are forcefully reset to $\mathbf{0}$.
- **Action history ($H^a$):** Preserved.
- **Contact history ($H^c$):** Preserved.
- **Policy hidden state ($h^{\pi}$):** **RESET:** $h_{t_d}^{\pi} \leftarrow h_{\text{init}} = \mathbf{0}$.
- **Random-number state ($\xi$):** Synchronized to seed at $t_d$.
- **Remaining horizon ($\Delta t_{\text{remain}}$):** $T - t_d$.
- **Goal state ($g$):** Identical task goal $g$.
- **Purpose:** Tests whether long-horizon recurrent memory contains critical diagnostic state not reconstructible from recent observations.
- **Possible confounds:** Resetting $h$ abruptly induces a transient activation shock to the neural network.

---

### Condition B4: All Recoverable History Removed (Combined Counterfactual Injection)
- **Physical state ($s_t$):** Directly injected physical state $s_c$ matching $s(t_d)$ within tolerance $\epsilon$ ($d(s_c, s(t_d)) \le \epsilon$).
- **Observation history ($H^o$):** **REMOVED:** Instantaneous observation $o_{t_d}$ only.
- **Action history ($H^a$):** **REMOVED:** $a_{\text{hist}} = \emptyset$.
- **Contact history ($H^c$):** Prior dynamic contact trajectory erased; only instantaneous contact normal force active.
- **Policy hidden state ($h^{\pi}$):** **RESET:** $h_{\text{init}} = \mathbf{0}$.
- **Random-number state ($\xi$):** Synchronized to seed at $t_d$.
- **Remaining horizon ($\Delta t_{\text{remain}}$):** $T - t_d$.
- **Goal state ($g$):** Identical task goal $g$.
- **Purpose:** The macroscopic causal contrast: tests total history dependence vs. pure state sufficiency ($H_R = R(B0) - R(B4)$).
- **Critical Methodological Note:** This is a **bundled multi-factor intervention**. Any performance difference reflects the combined impact of all historical channels, not an individual channel.

---

## 3. Summary Comparison Table

| Condition | Physical State | Observation History | Action History | Contact History | Policy Hidden State | Random State | Horizon | Analytical Purpose |
|---|---|---|---|---|---|---|---|---|
| **B0** | Matched via replay | Full $(o_{0:t_d})$ | Full $(a_{0:t_d-1})$ | Continuous | Evolved $h_{t_d}^{\pi}$ | Seed $\xi(t_d)$ | $T - t_d$ | Natural replay reference (RoboRecover equivalent) |
| **B1** | Matched via replay | Full $(o_{0:t_d})$ | **Reset ($\mathbf{0}$)** | Continuous | Evolved $h_{t_d}^{\pi}$ | Seed $\xi(t_d)$ | $T - t_d$ | Isolates action history effect |
| **B2** | Matched via replay | **Reset ($k=1$)** | Full $(a_{0:t_d-1})$ | Continuous | Reset $h_0$ | Seed $\xi(t_d)$ | $T - t_d$ | Isolates observation history effect |
| **B3** | Matched via replay | Windowed | Full $(a_{0:t_d-1})$ | Continuous | **Reset ($\mathbf{0}$)** | Seed $\xi(t_d)$ | $T - t_d$ | Isolates policy memory state effect |
| **B4** | Directly injected ($s_c$) | **Reset ($k=1$)** | **Reset ($\emptyset$)** | Instantaneous | **Reset ($\mathbf{0}$)** | Seed $\xi(t_d)$ | $T - t_d$ | Combined macroscopic causal intervention ($H_R$) |

