# Task Success Specification: Binary Goal Completion & Dwell Criteria

> **Environment Target:** `planned_custom_push_target_env`  
> **Evaluation Standard:** Strict Binary Success Metric ($R \in \{0, 1\}$)  
> **Methodological Mandate:** Dense distance rewards are explicitly prohibited as a success proxy. Success must be binary, verifiable, and physically grounded.

---

## 1. Formal Definition of Binary Task Success

An episode is declared a **Success ($R = 1$)** if and only if, upon termination or completion, all five of the following physical criteria are simultaneously satisfied:

$$\text{Task Success } R = \mathbb{1}\left[ \mathcal{C}_{\text{pos}} \land \mathcal{C}_{\text{yaw}} \land \mathcal{C}_{\text{dwell}} \land \mathcal{C}_{\text{safe}} \land \mathcal{C}_{\text{workspace}} \right]$$

### 1.1 Position Criterion ($\mathcal{C}_{\text{pos}}$)
- The Euclidean distance between the Cartesian center of mass of the target cube $p_{\text{obj}, xy} = (x_{\text{obj}}, y_{\text{obj}})$ and the target zone center $p_{\text{goal}, xy} = (x_{\text{goal}}, y_{\text{goal}}) = (0.25, 0.0)$ must be within the target radius $r_{\text{target}}$:
  $$\|p_{\text{obj}, xy} - p_{\text{goal}, xy}\|_2 \le r_{\text{target}} = 0.060 \text{ meters (6.0 cm)}$$

### 1.2 Yaw Orientation Criterion ($\mathcal{C}_{\text{yaw}}$)
- The absolute yaw deflection angle $|\theta_{\text{obj}}|$ relative to the intended forward axis ($+X$) must remain within the angular alignment tolerance:
  $$|\theta_{\text{obj}}| \le \theta_{\text{max}} = 0.35 \text{ radians } (\approx 20.0^\circ)$$
  *Physical Justification:* Pushing an object into a target zone while severely misaligned or tumbled does not constitute an orderly placement.

### 1.3 Consecutive Dwell Time Criterion ($\mathcal{C}_{\text{dwell}}$)
- The target object must remain continuously inside the target zone satisfying $\mathcal{C}_{\text{pos}}$ and $\mathcal{C}_{\text{yaw}}$ for a minimum of $N_{\text{dwell}}$ consecutive simulation steps:
  $$N_{\text{dwell}} \ge 5 \text{ consecutive steps (at 200 Hz = 0.025 seconds)}$$
  *Physical Justification:* Prevents transient glancing trajectories (where the cube sweeps across the circle at high speed without settling) from falsely registering as successful placements.

### 1.4 Safety & Collision Force Criterion ($\mathcal{C}_{\text{safe}}$)
- During the episode, the maximum contact normal force between the pusher and the cube must not exceed the structural damage threshold:
  $$F_{\text{contact}} \le F_{\text{max}} = 50.0 \text{ N}$$
- The object must not penetrate the table surface ($z_{\text{obj}} \ge 0.015$ m) nor tip over ($z_{\text{obj}} \le 0.050$ m).

### 1.5 Workspace Constraint Criterion ($\mathcal{C}_{\text{workspace}}$)
- Both the robotic pusher and the target cube must remain strictly within the allowable physical workspace:
  $$x \in [-0.45, 0.45] \text{ m}, \quad y \in [-0.45, 0.45] \text{ m}$$

---

## 2. Parameter Specification Table

| Parameter | Symbol | Numerical Value | Physical Unit | Measurement Method |
|---|---|---|---|---|
| Target Zone Center | $p_{\text{goal}}$ | $(0.25, 0.0, 0.025)$ | meters | Static environment coordinate |
| Target Zone Radius | $r_{\text{target}}$ | $0.060$ | meters (6 cm) | Euclidean distance in $XY$ plane |
| Maximum Yaw Deflection | $\theta_{\text{max}}$ | $0.35$ | radians ($20.0^\circ$) | Computed from quaternion $q_{6:10}$ |
| Minimum Dwell Steps | $N_{\text{dwell}}$ | $5$ | consecutive steps | Internal environment integer counter |
| Maximum Normal Force | $F_{\text{max}}$ | $50.0$ | Newtons (N) | Extracted from `mjData.contact` |
| Workspace X Bounds | $[x_{\min}, x_{\max}]$ | $[-0.45, +0.45]$ | meters | Pusher and object coordinates |
| Workspace Y Bounds | $[y_{\min}, y_{\max}]$ | $[-0.45, +0.45]$ | meters | Pusher and object coordinates |
| Minimum Table Clearance | $z_{\min}$ | $0.015$ | meters | Object height above ground |
| Evaluation Frequency | $f_{\text{check}}$ | Every step | N/A | Monitored dynamically inside `step()` |
| Partial Credit Policy | N/A | **Disallowed** | Binary $\{0, 1\}$ | Strict 0 or 1 indicator |

---

## 3. Disallowance of Dense Reward as Success Metric

In reinforcement learning, reward functions frequently reward proximity (e.g. $r = -\|p_{\text{obj}} - p_{\text{goal}}\|$). In this research:
1. **Reward is an optimization signal, not an evaluation metric.**
2. A policy that moves the block close to the target but leaves it unstable or spinning out of control receives a negative success label ($R = 0$).
3. All primary recovery metrics ($RSR$, $H_R$, $P(F)$) depend strictly on the binary success indicator $R$.

