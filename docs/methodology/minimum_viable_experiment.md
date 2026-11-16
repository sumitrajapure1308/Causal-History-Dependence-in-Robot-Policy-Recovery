# Minimum Viable Experiment (MVE) Specification

> **Status:** Defined & Frozen for Phase 1–2 Initial Implementation  
> **Simulation Engine:** MuJoCo (`mujoco 3.10.0`)  
> **Core Objective:** Establish the smallest, most rigorously controlled experiment validating the causal-history evaluation protocol before scaling to the full multi-task benchmark.

---

## 1. Selected Task: Contact-Rich Block Pushing & Alignment (`planned_custom_push_target_env`)

### Description
A robotic manipulator (calibrated 3-DoF planar Cartesian manipulator or 7-DoF Franka Emika Panda end-effector) pushes a square target block from an initial workspace location $(x_0, y_0)$ to a designated circular target zone $(x_g, y_g)$ across a surface with Coulomb friction.

*(Note: In accordance with Phase 0.5 audit standards, this is a planned custom environment to be implemented and tested in Phase 1; it is not assumed to be pre-existing).*

### Why This Task is Suitable
1. **Full State Accessibility:** In MuJoCo, the complete generalized coordinates $q \in \mathbb{R}^{n_q}$, generalized velocities $\dot{q} \in \mathbb{R}^{n_v}$, end-effector pose, block 6D pose, linear/angular velocity, and contact forces can be extracted with zero approximation.
2. **Bitwise Deterministic Reset and Restoration:** MuJoCo allows bitwise saving and restoration of `mjData` (`qpos`, `qvel`, `act`, `warmstart`), ensuring zero state drift during resets and replays.
3. **Contact-Rich Physics:** Pushing is fundamentally governed by sticking and slipping friction modes, normal contact forces, and rotational moments. These dynamics provide a realistic testbed where history (momentum, sliding velocity) interacts with instantaneous geometry.
4. **Fast Rollout Velocity:** Operates at $>1000$ Hz in CPU simulation, enabling rapid generation of hundreds of matched pairs and statistically significant Monte Carlo evaluations.

---

## 2. Selected Failure Mode: Off-Center Contact Slip (`Slip-Deviation`)

### Physical Mechanism
During normal pushing, the end-effector maintains contact along the face of the block. A failure occurs when:
1. An action error causes a lateral end-effector offset relative to the block's center of mass.
2. Contact mode transitions from static stick to dynamic slip.
3. The block pivots unexpectedly, yawing by $\Delta \theta > \theta_{\text{thresh}}$ and drifting lateral to the intended push vector.
4. The pusher slips off the face or makes glancing contact, leaving the block stalled off-target.

### Why This Failure is Measurable
- **Deviation Time ($t_d$):** Detected objectively when the lateral displacement error $|y_{\text{block}} - y_{\text{nominal}}| > 1.5$ cm or yaw angle deviation $|\Delta \theta| > 15^\circ$ while pusher velocity is non-zero.
- **Physical Metrics:** Slip velocity, contact point drift, and angle error are directly observable in physical units (meters and radians).

---

## 3. Definition of Recoverability & Oracle Filter

An episode at deviation time $t_d$ is classified as **Recoverable** if and only if:
1. **Workspace Boundary:** The block remains inside the reachable workspace ($x_{\min} \le x_{\text{block}} \le x_{\max}$ and $y_{\min} \le y_{\text{block}} \le y_{\max}$).
2. **Terminal Condition Avoidance:** The block has not fallen off the table or jammed into a rigid barrier.
3. **Oracle Feasibility Check:** A scripted or privileged oracle controller (which repositions the pusher perpendicular to the block's current heading and executes a re-aligned push) can complete the task from state $s(t_d)$ within the remaining horizon $T - t_d$.

If the oracle succeeds ($R_{\text{oracle}} = 1$), the failure state is marked `recoverable: true` and admitted to the benchmark. If the oracle fails, it is marked `recoverable: false` and strictly excluded from the policy recovery denominator.

---

## 4. Evaluated Policy Baselines

We implement two contrasting baseline policies:

1. **Reactive Policy (`BC-Reactive`):**
   - Architecture: Compact Multi-Layer Perceptron (MLP) (3 layers, 128 hidden units, ReLU activations).
   - Input: Instantaneous observation $o_t = [p_{ee}, \dot{p}_{ee}, p_{\text{obj}}, R_{\text{obj}}, v_{\text{obj}}, g]$.
   - Memory: None ($k = 1$).
2. **History-Aware Policy (`BC-History`):**
   - Architecture: Recurrent neural network (GRU with 128 hidden units) or observation stack of the last $k=5$ timesteps $[o_{t-4:t}]$.
   - Input: Sequence of recent observations and actions $(o_{t-k:t}, a_{t-k:t-1})$.
   - Memory: Explicit temporal context over recent interaction history.

---

## 5. Experimental Comparison Conditions & Disentanglement Analysis

### Critical Verification: Condition A vs. Condition B Equivalence Under Determinism
Under deterministic physics simulation (MuJoCo with fixed solver settings) and deterministic policy execution (greedy/mean action output with no stochastic sampling):
- **Condition A (Natural Policy Execution)** runs closed-loop from $t=0$, issuing actions $a_0, a_1, \dots, a_{t_d-1}$ and experiencing deviation at $t_d$.
- **Condition B (Prefix-Replay)** initializes at the identical initial state $s_0$ and executes the exact recorded action prefix $a_0, a_1, \dots, a_{t_d-1}$.

**Mathematical Identity:** Because the simulation transition function $T(s, a)$ is deterministic and state initialization is identical:
$$s_B(t_d) \equiv s_A(t_d) \quad \text{and} \quad o_{0:t_d}^{(B)} \equiv o_{0:t_d}^{(A)}$$
Therefore, **Condition A and Condition B are structurally identical under deterministic conditions**. They produce identical states, identical contact manifolds, and identical policy hidden states.

**Scientific Role of Condition A:** Condition A is retained **not as an independent causal condition**, but as an **ecological fidelity baseline**. It verifies that:
1. The replay harness introduces zero state drift ($d(s_A(t_d), s_B(t_d)) = 0$).
2. The prefix replay faithfully reproduces the natural execution deviation without replay artifacts.
Only if stochastic sensor noise, non-deterministic physics, or stochastic policy exploration were introduced would Condition A and Condition B diverge.

### The Primary Causal Contrast: Condition B vs. Condition C
Because Condition A and B are identical in deterministic settings, the **true and primary causal comparison** is between:
$$\text{Condition B (Preserved History)} \quad \text{versus} \quad \text{Condition C (Matched Injection without History)}$$

### Specification of Conditions:

#### Condition A: Natural Policy-Induced Failure (Ecological Validation)
- Policy $\pi$ runs closed-loop from $t=0$.
- Sub-optimal control leads naturally to slip deviation at $t_d$.
- The policy continues uninterrupted from $t_d$ to horizon $T$.
- Role: Ecological verification baseline.

#### Condition B: Prefix-Replay Failure (Preserved Causal History)
- The exact action prefix $a_{0:t_d-1}$ recorded from Condition A is replayed deterministically in the simulator.
- At $t=t_d$, control transfers to policy $\pi$.
- Observation buffer $o_{0:t_d}$ and action buffer $a_{0:t_d-1}$ are fully populated.
- Preserves the full causal trajectory, physical momentum, and action history.

#### Condition C: Matched-State Injection (History-Free Intervention)
- The simulator is reset directly to physical state $s_c$ matched to $s_B(t_d)$:
  $$d(s_c, s_B(t_d)) \le \epsilon$$
- No preceding actions are executed in this rollout ($a_{0:t_d-1} = \emptyset$).
- Observation history is reset (prior frames blank/padded); recurrent hidden state is initialized to default $h_0$.
- Control begins immediately at $t_d$ with remaining horizon $T - t_d$.
- Isolates instantaneous physical state from preceding causal history.

#### Optional Condition D: Observation-History Masking (Temporal Window Ablation)
- From the replayed recovery state (Condition B), evaluate the history-aware policy while varying its observation window $k \in \{1, 2, 5, 10\}$.

---

## 6. State-Matching Method for MVE
For the block push task, the state vector is:
$$s = [p_{ee}, \dot{p}_{ee}, p_{\text{obj}}, \theta_{\text{obj}}, v_{\text{obj}}, \omega_{\text{obj}}, c, g]$$
The weighted Euclidean distance is computed as:
$$d(s_1, s_2) = w_p \|p_{ee,1} - p_{ee,2}\|_2 + w_v \|\dot{p}_{ee,1} - \dot{p}_{ee,2}\|_2 + w_{obj} \|p_{\text{obj},1} - p_{\text{obj},2}\|_2 + w_{\theta} |\theta_{\text{obj},1} - \theta_{\text{obj},2}| + w_c \mathbb{1}[c_1 \neq c_2]$$
Default MVE acceptance threshold:
$$\epsilon_{\text{MVE}} = 0.005 \text{ (meters/radians normalized)}$$

---

## 7. Main Outcome Variables & Dependent Metrics
- **Primary Outcome:** Recovery Success Rate ($RSR_A, RSR_B, RSR_C$).
- **History Dependence Metric:** $H_R = RSR_B - RSR_C$.
- **Detection Delay:** $D_{\text{delay}} = t_{\text{detection}} - t_d$.
- **Corrective Effort:** Additional path length $\Delta L$ and additional steps $\Delta T$ to complete the push.

---

## 8. Confounding Factors & Controlled Mitigation
1. **Velocity / Momentum Drift:** Direct resets often zero out velocities. *Mitigation:* `mjData.qvel` is explicitly restored to match the non-zero velocities of the replayed state.
2. **Contact Point Discontinuities:** A slight geometric discrepancy can cause the contact solver to register an impulse. *Mitigation:* MuJoCo warmstart cache and contact manifolds are verified, and matching requires identical contact indicators ($c_1 = c_2$).
3. **Horizon Asymmetry:** Injecting at $t_d$ without setting the step counter could allow a full episode horizon. *Mitigation:* The remaining step budget is strictly enforced as $T_{\text{remain}} = T - t_d$ across all conditions.

