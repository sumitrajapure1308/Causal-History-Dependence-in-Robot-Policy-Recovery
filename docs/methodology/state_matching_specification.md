# Physical State-Matching Specification

> **Specification Standard:** Multi-Component Weighted Distance with Explicit Physical Constraints  
> **Status:** Formal Specification Frozen  
> **Scope:** Defines mathematical equivalence between robotic recovery states across replay and injection conditions.

---

## 1. Principles of State Matching

1. **Physical Completeness:** A state cannot be declared equivalent based on geometry alone. Generalized velocities, contact graphs, actuator dynamics, and remaining horizons must be accounted for.
2. **Rejection of Image-Only Matching:** Image pixel similarity (e.g. L2 pixel difference or latent cosine similarity) is explicitly forbidden as the primary matching criterion. Visually identical scenes may possess wildly divergent momentum vectors or contact normal forces.
3. **Multi-Tier Sensitivity:** To prevent bias from an arbitrary single tolerance threshold, evaluation must be conducted and reported across three predefined tiers: **Strict** ($\epsilon_1$), **Moderate** ($\epsilon_2$), and **Loose** ($\epsilon_3$).
4. **Primary Counterfactual Comparison Context:** State matching operates strictly to guarantee physical equivalence between **Condition B (Prefix Replay Recovery State $s_B(t_d)$)** and **Condition C (Matched Injection State $s_C(t_d)$)**. In deterministic simulations, Condition A (Natural Execution) and Condition B yield $s_A(t_d) \equiv s_B(t_d)$ with $d(s_A, s_B) = 0$. Condition A is therefore an ecological verification baseline, while Condition B vs Condition C forms the primary causal intervention.

---

## 2. Formal State Vector Representation

Let a robot manipulation state $s$ at candidate recovery time $t_d$ be represented as the composite vector:

$$s = \left[ q, \, \dot{q}, \, p_{ee}, \, R_{ee}, \, p_{\text{obj}}, \, R_{\text{obj}}, \, v_{\text{obj}}, \, \omega_{\text{obj}}, \, c, \, g, \, m, \, \Delta t_{\text{remain}} \right]$$

where:
- $q \in \mathbb{R}^{n_q}$: Generalized joint positions of the robot manipulator.
- $\dot{q} \in \mathbb{R}^{n_v}$: Generalized joint velocities.
- $p_{ee} \in \mathbb{R}^3$: Cartesian end-effector position.
- $R_{ee} \in \mathcal{SO}(3)$ (or unit quaternion $q_{ee} \in \mathbb{S}^3$): End-effector orientation.
- $p_{\text{obj}} \in \mathbb{R}^{3 \times N_{\text{obj}}}$: Cartesian positions of all task-relevant objects.
- $R_{\text{obj}} \in \mathcal{SO}(3)^{N_{\text{obj}}}$ (or unit quaternions $q_{\text{obj}}$): Orientations of task objects.
- $v_{\text{obj}} \in \mathbb{R}^{3 \times N_{\text{obj}}}$: Linear velocities of task objects.
- $\omega_{\text{obj}} \in \mathbb{R}^{3 \times N_{\text{obj}}}$: Angular velocities of task objects.
- $c \in \{0, 1\}^{N_{\text{contacts}}}$: Discrete contact manifold indicator graph (robot-object, object-table, object-object).
- $g \in \mathbb{R}^{d_g}$: Task goal specification vector.
- $m \in \{0, 1\}$ (or continuous $w \in [0, 1]$): Gripper state / actuator aperture.
- $\Delta t_{\text{remain}} = T - t_d$: Remaining execution horizon.

---

## 3. Weighted Physical Distance Function

The total state distance $d(s_1, s_2)$ between two candidate recovery states $s_1$ and $s_2$ is defined as:

$$d(s_1, s_2) = w_q d_q + w_{\dot{q}} d_{\dot{q}} + w_p d_p + w_R d_R + w_{\text{obj},p} d_{\text{obj},p} + w_{\text{obj},R} d_{\text{obj},R} + w_{\text{obj},v} d_{\text{obj},v} + w_c d_c + w_g d_g + w_m d_m$$

### Distance Component Definitions:
1. **Joint Position Distance ($d_q$):**
   $$d_q = \frac{1}{n_q} \sum_{j=1}^{n_q} \frac{|q_{1,j} - q_{2,j}|}{q_{\max,j} - q_{\min,j}}$$
2. **Joint Velocity Distance ($d_{\dot{q}}$):**
   $$d_{\dot{q}} = \frac{1}{n_v} \sum_{j=1}^{n_v} \frac{|\dot{q}_{1,j} - \dot{q}_{2,j}|}{\dot{q}_{\max,j}}$$
3. **End-Effector Position Distance ($d_p$):**
   $$d_p = \|p_{ee,1} - p_{ee,2}\|_2 \quad (\text{in meters})$$
4. **End-Effector Orientation Distance ($d_R$):**
   $$d_R = 2 \arccos(|\langle q_{ee,1}, q_{ee,2} \rangle|) \quad (\text{geodesic angle on } \mathcal{SO}(3), \text{in radians})$$
5. **Object Position Distance ($d_{\text{obj},p}$):**
   $$d_{\text{obj},p} = \frac{1}{N_{\text{obj}}} \sum_{i=1}^{N_{\text{obj}}} \|p_{\text{obj},1}^{(i)} - p_{\text{obj},2}^{(i)}\|_2 \quad (\text{in meters})$$
6. **Object Orientation Distance ($d_{\text{obj},R}$):**
   $$d_{\text{obj},R} = \frac{1}{N_{\text{obj}}} \sum_{i=1}^{N_{\text{obj}}} 2 \arccos(|\langle q_{\text{obj},1}^{(i)}, q_{\text{obj},2}^{(i)} \rangle|)$$
7. **Object Velocity Distance ($d_{\text{obj},v}$):**
   $$d_{\text{obj},v} = \frac{1}{N_{\text{obj}}} \sum_{i=1}^{N_{\text{obj}}} \left( \|v_{\text{obj},1}^{(i)} - v_{\text{obj},2}^{(i)}\|_2 + 0.1 \|\omega_{\text{obj},1}^{(i)} - \omega_{\text{obj},2}^{(i)}\|_2 \right)$$
8. **Contact Graph Distance ($d_c$):**
   $$d_c = \frac{1}{N_{\text{contacts}}} \sum_{k=1}^{N_{\text{contacts}}} \mathbb{1}[c_{1,k} \neq c_{2,k}]$$
9. **Goal Distance ($d_g$):**
   $$d_g = \|g_1 - g_2\|_2$$
10. **Gripper State Distance ($d_m$):**
    $$d_m = |m_1 - m_2|$$

---

## 4. Default Weights & Normalization

| Component | Variable | Weight $w_i$ | Normalization / Units |
|---|---|---|---|
| Robot Joint Angles | $q$ | 0.15 | Joint limits normalized $[0, 1]$ |
| Robot Joint Velocities | $\dot{q}$ | 0.10 | Velocity limits normalized $[0, 1]$ |
| End-Effector Position | $p_{ee}$ | 0.20 | Meters (scale factor $10.0 \text{ m}^{-1}$) |
| End-Effector Orientation | $R_{ee}$ | 0.10 | Radians (scale factor $1.0 \text{ rad}^{-1}$) |
| Object Position | $p_{\text{obj}}$ | 0.20 | Meters (scale factor $10.0 \text{ m}^{-1}$) |
| Object Orientation | $R_{\text{obj}}$ | 0.10 | Radians (scale factor $1.0 \text{ rad}^{-1}$) |
| Object Velocities | $v_{\text{obj}}$ | 0.05 | Meters/second |
| Contact Graph | $c$ | 0.05 | Binary match $\{0, 1\}$ |
| Task Goal State | $g$ | Hard Constraint | Must be identical ($d_g = 0$) |
| Gripper Aperture | $m$ | 0.05 | Aperture normalized $[0, 1]$ |

$$\sum_{i} w_i = 1.0$$

---

## 5. Absolute Rejection Rules (Hard Filters)

Before computing the weighted scalar distance $d(s_1, s_2)$, a candidate matched pair is **immediately rejected** if any of the following hard constraints are violated:

1. **Goal Invariant:** $d_g > 0$ (The task goal must be identical).
2. **Remaining Horizon Invariant:** $\Delta t_{\text{remain},1} \neq \Delta t_{\text{remain},2}$ (Remaining steps must match exactly).
3. **Contact Mode Invariant:** $d_c > 0$ (If the robot has established contact with the object in State 1, State 2 must also be in contact; a slipping contact cannot be matched with an open-air non-contact state).
4. **Gripper Closure Mode:** Binary gripper state must match ($\mathbb{1}[m_1 > 0.5] == \mathbb{1}[m_2 > 0.5]$).
5. **Reachable Workspace:** Both states must lie within valid workspace limits (no penetration into floor/walls).

---

## 6. Tolerance Tiers for Sensitivity Analysis

A scenario pair $(s_1, s_2)$ is accepted if hard constraints pass and $d(s_1, s_2) \le \epsilon$. We establish three tolerance tiers:

| Metric / Threshold | Strict Tier ($\epsilon_1$) | Moderate Tier ($\epsilon_2$) | Loose Tier ($\epsilon_3$) |
|---|---|---|---|
| **Max Composite Distance $\epsilon$** | **0.010** | **0.030** | **0.075** |
| Max End-Effector Position Error | $< 2.0$ mm | $< 5.0$ mm | $< 15.0$ mm |
| Max End-Effector Orientation Error | $< 0.03$ rad ($1.7^\circ$) | $< 0.08$ rad ($4.6^\circ$) | $< 0.20$ rad ($11.5^\circ$) |
| Max Object Position Error | $< 2.0$ mm | $< 5.0$ mm | $< 15.0$ mm |
| Max Object Orientation Error | $< 0.03$ rad ($1.7^\circ$) | $< 0.08$ rad ($4.6^\circ$) | $< 0.20$ rad ($11.5^\circ$) |
| Max Joint Velocity Error | $< 0.02$ rad/s | $< 0.05$ rad/s | $< 0.15$ rad/s |
| Contact Graph Difference | 0 (Exact match) | 0 (Exact match) | $\le 1$ minor contact point |

---

## 7. Multimodal Visual Observation Validation

When visual policies (CNN/ViT) are evaluated, physical state matching is supplemented by perceptual consistency validation:
- **Camera Extrinsics & Intrinsics:** Fixed camera matrix $\mathbf{K}$ and pose $[\mathbf{R} \mid \mathbf{t}]$ locked across conditions.
- **Lighting & Rendering Parameters:** Ambient, diffuse, and specular lighting parameters locked.
- **Background & Asset Textures:** Procedural seed frozen.
- **Visual Similarity Metric (Sanity Check Only):** We record the structural similarity index (SSIM) and peak signal-to-noise ratio (PSNR) of the rendered frames:
  $$\text{SSIM}(I_1, I_2) \ge 0.95$$
  *Visual similarity serves to verify rendering consistency; it does not replace the physical state matching criterion.*

