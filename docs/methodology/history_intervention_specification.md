# History Intervention Specification & Taxonomy

> **Specification Standard:** Multi-Stream History Disentanglement & Experimental Intervention  
> **Status:** Formal Specification Frozen  
> **Scope:** Disentangles and explicitly defines all constituent components of "history" in robot manipulation and formalizes what is preserved, altered, or reset across evaluation conditions.

---

## 1. Disentangled Definitions of History Streams

In robot learning and closed-loop control, the term "history" is frequently overloaded. We explicitly separate eleven distinct state and temporal history streams:

### 1.1 Physical Simulator State ($s_t$)
- **Definition:** The complete Markovian ground-truth physical state of the simulation at time $t$. In MuJoCo, this consists of generalized coordinates $q \in \mathbb{R}^{n_q}$, generalized velocities $\dot{q} \in \mathbb{R}^{n_v}$, actuator activations $\text{act}$, and solver warmstart momentum caches.
- **Role:** Governs future physical transitions: $s_{t+1} = T(s_t, a_t)$.

### 1.2 Observation History ($H_t^o$)
- **Definition:** The sequence of complete multimodal observations received by the agent up to time $t$: $H_t^o = (o_0, o_1, \dots, o_t)$.
- **Sub-streams:**
  - **Proprioceptive History ($H_t^{\text{prop}}$):** Past joint angles, joint velocities, and end-effector poses: $(q_{0:t}, \dot{q}_{0:t}, p_{ee,0:t})$.
  - **Visual History ($H_t^{\text{vis}}$):** Past camera frames, depth maps, or visual embeddings: $(I_0, I_1, \dots, I_t)$.

### 1.3 Action History ($H_t^a$)
- **Definition:** The sequence of control commands issued by the agent or replay controller up to time $t-1$: $H_t^a = (a_0, a_1, \dots, a_{t-1})$.
- **Role:** Represents the causal action path executed by the manipulator leading to the current configuration.

### 1.4 Contact History ($H_t^c$)
- **Definition:** The temporal sequence of physical contact events, contact normal impulses, and friction stick/slip transitions: $H_t^c = (c_0, c_1, \dots, c_t)$ where $c_k \in \{0, 1\}^{N_{\text{contacts}}}$.
- **Role:** Encodes micro-slip accumulation, surface sticking hysteresis, and contact normal force evolution.

### 1.5 Policy Hidden State ($h_t^{\pi}$)
- **Definition:** The internal recurrent or memory state of the policy network (e.g., GRU/LSTM hidden state $h_t$, transformer KV cache, or frame-buffer stack).
- **Role:** Memory carrier within the policy architecture. For a reactive policy, $h_t^{\pi} = \emptyset$.

### 1.6 Reward & Progress History ($H_t^r, H_t^g$)
- **Definition:** The historical sequence of scalar task rewards and progress indicators (e.g., distance to goal $\Delta d_{\text{goal}}(t)$).
- **Role:** Monitored externally for evaluation; not directly exposed to low-level control policies.

### 1.7 Random-Number Generator (RNG) State ($\xi_t$)
- **Definition:** The state of the pseudo-random number generator governing sensor noise, simulation jitter, and stochastic policy sampling.
- **Role:** Controlled across conditions to enforce common random numbers (CRN).

### 1.8 Failure-Detection & Diagnosis History ($H_t^{\text{diag}}$)
- **Definition:** The historical log of anomaly detection scores and diagnostic classification outputs produced by the policy or monitoring subsystem up to time $t$.

---

## 2. Condition-by-Condition Intervention Matrix

The table below specifies precisely what is preserved, altered, or reset across all evaluation conditions at candidate recovery time $t_d$:

| condition | physical_state | observation_history | action_history | policy_hidden_state | contact_history | random_state | remaining_horizon | purpose |
|---|---|---|---|---|---|---|---|---|
| **Condition A (Natural Execution)** | Natural $s(t_d)$ reached by live policy | Continuous $o_{0:t_d}$ accumulated by policy | Continuous $a_{0:t_d-1}$ issued by policy | Continuous $h_{t_d}^{\pi}$ evolved during rollout | Continuous $c_{0:t_d}$ from rollout | Preserved running seed $\xi_{t_d}$ | $T - t_d$ | **Natural baseline validation:** Serves as the ecological benchmark reference for closed-loop execution. |
| **Condition B (Prefix Replay)** | Matched $s(t_d)$ reached by replaying prefix | Reconstructed $o_{0:t_d}$ from replayed trajectory | Replayed action prefix $a_{0:t_d-1}$ | Reconstructed by unrolling policy or initialized from prefix | Preserved $c_{0:t_d}$ via identical replay | Synchronized to prefix replay RNG | $T - t_d$ | **Preserved history baseline (RoboRecover equivalent):** Preserves the full causal action prefix and physical trajectory. |
| **Condition C (Matched Injection)** | Matched $s_c$ ($d(s_c, s(t_d)) \le \epsilon$) directly injected | Reset: Instantaneous observation $o_{t_d}$ only (prior $o_{0:t_d-1}$ padded/empty) | Reset: Zero/empty ($a_{0:t_d-1} = \emptyset$) | Reset: Initialized to default blank state $h_0$ | Reset: Prior contact events erased; instantaneous contact active | Synchronized to seed $\xi(t_d)$ | $T - t_d$ | **Causal intervention condition:** Isolates instantaneous physical state from preceding causal action/observation history. |
| **Condition D (Observation Masking / Ablation)** | Matched $s(t_d)$ (from Replay B) | Windowed: Exactly $k$ recent steps $(o_{t_d-k+1:t_d})$ | Windowed: Exactly $k-1$ recent actions | Windowed: Unrolled only across the $k$-step window | Instantaneous active contact | Synchronized to seed $\xi(t_d)$ | $T - t_d$ | **Temporal ablation:** Quantifies how recovery depends on observation window length $k \in \{1, 2, 5, 10\}$. |

---

## 3. The Primary Causal Comparison

### Formalization of the Primary Contrast:
The fundamental scientific comparison in this research is:
$$\mathbf{\Delta_{\text{causal}}} = \text{Condition B} \quad \text{vs.} \quad \text{Condition C}$$

- **Under Condition B (Preserved History):**
  The robot policy is placed at physical failure state $s(t_d)$ after experiencing the exact causal prefix that generated that failure. Its observation buffer contains $(o_0, \dots, o_{t_d})$ and its action history contains $(a_0, \dots, a_{t_d-1})$.
- **Under Condition C (Altered / Reset History):**
  The robot policy is placed at a physically matched state $s_c$ where $d(s_c, s(t_d)) \le \epsilon$ via direct simulator injection. However, all preceding observation history, action history, and recurrent policy memory are reset.
- **The Core Scientific Outcome:**
  $$H_R = R_{\text{replay}} - R_{\text{injected}} = R(\text{Condition B}) - R(\text{Condition C})$$
  - If $H_R \approx 0$: Recovery capability is strictly **state-governed**. The state-sufficiency assumption holds, validating existing replay-only benchmarks like RoboRecover.
  - If $H_R \neq 0$: Recovery capability is **history-dependent**. Replay-based benchmarks mischaracterize recovery because they fail to disentangle state from causal history.

### Role of Condition A:
Condition A is treated strictly as **natural-execution ecological validation**. In a deterministic simulation environment without sensor noise or policy divergence, Condition A and Condition B are structurally identical because replaying the exact action sequence of a deterministic policy reproduces the exact same trajectory. Condition A differs only when stochastic policy sampling or environment noise causes closed-loop rollouts to diverge from open-loop replays.

