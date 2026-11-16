# Implementable Intervention Semantics (Version 2.0)

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Status:** VALIDATED SPECIFICATION  
**Document:** `docs/methodology/intervention_semantics_v2.md`  
**Date:** 2026-11-09  

---

## 1. Mathematical Formulation of Interventions

Let an execution prefix prior to failure deviation at step $t_{\text{dev}}$ consist of the sequence of physical observations and actions:
$$\mathcal{H}_{t_{\text{dev}}} = \big( (o_0, a_0), (o_1, a_1), \dots, (o_{t_{\text{dev}}-1}, a_{t_{\text{dev}}-1}), o_{t_{\text{dev}}} \big)$$
At step $t_{\text{dev}}$, the robot enters a failure state $S_{\text{fail}} = \text{MuJoCo}(qpos, qvel)$.

A policy with recurrent hidden state and sliding buffers computes the next recovery action $a_{\text{rec}}$ via:
$$a_{t_{\text{dev}}} = \pi_\theta \big( x_t, h_t \big)$$
where $x_t = [o_t, a_{t-1}, c_t]$ is the input token and $h_t$ is the recurrent memory.

---

## 2. Timing of Hidden-State Capture and Observation Consumption

To prevent double consumption or accidental omission of the deviation observation $o_{t_{\text{dev}}}$:

1. **Prefix Unrolling Phase ($t = 0 \dots t_{\text{dev}} - 1$):**
   - The policy is initialized at $t=0$ with $h_0 = \mathbf{0}$, $a_{-1} = \mathbf{0}$.
   - For each step $s \in [0, t_{\text{dev}} - 1]$, the policy consumes $x_s = [o_s, a_{s-1}]$ and updates $h_{s+1} = \text{GRU}(x_s, h_s)$.
2. **Deviation Time State ($t = t_{\text{dev}}$):**
   - At the instant of matched-state restoration, the environment state is $S_{\text{fail}}$ and emits observation $o_{t_{\text{dev}}}$.
   - The hidden state passed into the first recovery inference is **$h_{t_{\text{dev}}}$** (the state captured *before* consuming $o_{t_{\text{dev}}}$).
   - In the first recovery step, the policy consumes the input token $x_{t_{\text{dev}}} = [o_{t_{\text{dev}}}, a_{t_{\text{dev}}-1}]$ with initial hidden state $h_{t_{\text{dev}}}$.
   - This ensures $o_{t_{\text{dev}}}$ is consumed **exactly once** during the recovery phase.

---

## 3. Intervention Matrix by Architecture

| Architecture | Condition B0 (Preserved History) | Condition B1 (Action Masked) | Condition B2 (Obs Padded) | Condition B3 (Hidden Reset) | Condition B4 (Direct State Injection) |
|---|---|---|---|---|---|
| **Reactive MLP** | $x = [o_t]$ | **NOT APPLICABLE** (No action input) | **NOT APPLICABLE** (No obs buffer) | **NOT APPLICABLE** (No hidden state) | $x = [o_t]$ (Identical to B0) |
| **History GRU** | $x = [o_t, a_{t-1}]$, $h = h(t_{\text{dev}})$ | $x = [o_t, \mathbf{0}_3]$, $h = h(t_{\text{dev}})$ | Obs buffer filled with $o_t$, $h = h(t_{\text{dev}})$ | $x = [o_t, a_{t-1}]$, $h = \mathbf{0}$ | $x = [o_t, \mathbf{0}_3]$, $h = \mathbf{0}$ |
| **Recovery-Augmented MLP** | $x = [o_t, f_t, \tau_t, \delta_t, H_t]$ | **NOT APPLICABLE** (No action input) | **NOT APPLICABLE** (No obs buffer) | **NOT APPLICABLE** (No hidden state) | $x = [o_t, f_t, 0.0, \delta_t, H_t]$ ($\tau_t$ reset to 0) |
| **Recovery-Augmented GRU** | $x = [o_t^{\text{aug}}, a_{t-1}, c_t]$, $h = h(t_{\text{dev}})$ | $x = [o_t^{\text{aug}}, \mathbf{0}_3, c_t]$, $h = h(t_{\text{dev}})$ | Obs buffer filled with $o_t^{\text{aug}}$, $h = h(t_{\text{dev}})$ | $x = [o_t^{\text{aug}}, a_{t-1}, c_t]$, $h = \mathbf{0}$ | $x = [o_t^{\text{aug}}, \mathbf{0}_3, 0.0]$, $h = \mathbf{0}$, $\tau_t = 0.0$ |

---

## 4. Analysis of Information Leakage Across Interventions

### Explicit vs. Latent Channels:
1. **Condition B1:** Zeroing $a_{t-1}$ removes the explicit one-step action feedback. However, because $h(t_{\text{dev}})$ was formed by recursive integration over past actions $a_0 \dots a_{t_{\text{dev}}-2}$, **the recurrent memory $h(t_{\text{dev}})$ already retains action history**. Therefore, B1 tests sensitivity to immediate action feedback, NOT total independence from action history.
2. **Condition B2:** Overwriting the sliding window buffer with repeats of $o_{t_{\text{dev}}}$ removes high-frequency buffer information. However, $h(t_{\text{dev}})$ still retains the temporal trajectory of past observations.
3. **Condition B3:** Zeroing $h(t_{\text{dev}}) \to \mathbf{0}$ while retaining $a_{t-1}$ and observation buffers eliminates deep recurrent memory, but retains 1-step previous action feedback.
4. **Condition B4:** Eliminates both the explicit buffers ($a_{\text{prev}} = \mathbf{0}$, buffer repeats) and the latent recurrent memory ($h = \mathbf{0}$). For policies with temporal counters, $\tau_{\text{dev}}$ is reset to $0.0$. This represents complete history ablation down to the matched instantaneous physical state.

---

## 5. Formal Restrictions on Causal Claims

- Interventions B1 and B2 must **never** be cited as having cleanly decomposed action vs. observation causal effects due to latent entanglement in $h(t)$.
- If an architecture does not possess a specific channel (e.g. MLP lacks action input or hidden state), the condition is marked **NOT APPLICABLE**.

