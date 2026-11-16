# Environment Candidate Audit & Selection Decision

> **Document Status:** Formally Audited & Evaluated  
> **Auditors:** Robotics Research Engineer & Reproducibility Auditor  
> **Decision Verdict:** **SELECTION DEFERRED TO TWO-TIER ARCHITECTURE**  
> (Candidate A: Gymnasium `Pusher-v5` validated as immediate API & determinism testbed; Candidate B: `planned_custom_push_target_env` designated as required primary scientific environment for Q1 study).

---

## 1. Candidate Overview

- **Candidate A: Gymnasium `Pusher-v5`**
  - Standard continuous-control manipulation benchmark included with `gymnasium>=0.29.0`.
  - Robot: 7-DoF articulated arm with two-pronged pusher tip (`tip_arml`, `tip_armr`).
  - Object: Cylindrical puck constrained to 2D translation via two prismatic slide joints (`obj_slidey`, `obj_slidex`).
  - Goal: Target cylinder constrained to 2D translation (`goal_slidey`, `goal_slidex`).
- **Candidate B: `planned_custom_push_target_env`**
  - Planned custom MuJoCo task modeling a 3D robotic pusher interacting with a free-joint 6-DoF cube on a surface with Coulomb friction.
  - Object: Unconstrained rigid body (`type="free"`) with full rotation ($\text{roll, pitch, yaw}$) and 3D contact friction.
  - Goal: Static circular workspace target zone with explicit binary completion condition.

---

## 2. 18-Dimension Comprehensive Comparative Audit

Every entry is evaluated and labeled with its explicit status: `Verified`, `Partially verified`, `Not verified`, `Not applicable`, or `Planned`.

| # | Evaluation Dimension | Candidate A: Gymnasium `Pusher-v5` | Candidate B: `planned_custom_push_target_env` | Consequence for Project |
|---|---|---|---|---|
| **1** | **Task Relevance** | **Partially verified.** 7-DoF arm pushing a puck. Relevant to pushing, but object is kinematically constrained to planar translation without rotation. | **Planned.** Tabletop robotic pushing of a 6-DoF free-joint cube to a target zone. High real-world relevance. | Pusher-v5 represents simplified reaching-pushing; Candidate B matches manipulation physics. |
| **2** | **Failure Controllability** | **Partially verified.** Robot can miss the puck or push it laterally off-target. However, rotational slip ($\Delta \theta > 15^\circ$) is physically impossible due to slide joints. | **Planned.** Direct control over pusher contact angle, enabling measurable off-center contact slips and yaw deflections. | Rotational failure recovery cannot be studied in Pusher-v5. |
| **3** | **Recoverable Failure Availability** | **Partially verified.** Re-approaching a missed puck is possible if within reach; however, recovery is purely translational repositioning. | **Planned.** Clear bifurcation between recoverable off-center pivot slips and terminal workspace departures. | Candidate B provides richer recovery regimes. |
| **4** | **Full Simulator-State Access** | **Verified.** Direct access to MuJoCo `model` and `data` structures (`nq=11, nv=11, nu=7`). | **Verified.** Direct access to MuJoCo `model` and `data` structures. | Both candidates provide 100% Markov state visibility. |
| **5** | **State Serialization** | **Verified.** Complete serialization of `qpos`, `qvel`, `qacc_warmstart`, and `time` empirically validated with 0.0 drift. | **Verified.** Identical MuJoCo serialization pipeline applies. | Both candidates support bitwise serialization. |
| **6** | **State Restoration** | **Verified.** Empirically tested across restore-and-step cycles yielding 0.0 state divergence. | **Verified.** Identical `set_state` architecture. | State restoration is technically robust. |
| **7** | **Contact Extraction** | **Verified.** Contact manifold accessible via `d.contact` (detects table and tip contacts). However, object geom name is blank string `''`. | **Planned.** Contact manifold accessible with named geoms and contact force sensors. | Contact extractor must handle blank geom names in Pusher-v5. |
| **8** | **Deterministic Replay** | **Verified.** 20-step replay from identical seed yields 0.0 max divergence across observations and generalized coordinates. | **Planned.** Expected to achieve identical 0.0 divergence under fixed solver. | Replay fidelity verified on MuJoCo runtime. |
| **9** | **Direct State Injection** | **Partially verified.** Setting $(qpos, qvel)$ is functional, but injecting non-zero momentum on slide joints can induce contact chatter with the table. | **Planned.** Setting free joint pose and generalized velocities requires careful warmstart initialization. | Direct injection requires contact impulse auditing. |
| **10** | **Final Task-Success Measurement** | **Not verified (Deficient).** Pusher-v5 has **no binary success criterion** in `info` or termination; reward is strictly dense continuous distance. | **Planned.** Formal binary success criterion: $\|p_{\text{obj}} - p_{\text{goal}}\| \le 0.04$ m and $\|v_{\text{obj}}\| \le 0.02$ m/s. | Evaluating recovery success rate (RSR) in Pusher-v5 requires adding an external wrapper metric. |
| **11** | **History-Aware Policy Compatibility** | **Verified.** Compatible with observation frame-stacking and recurrent hidden states. | **Planned.** Fully compatible with unified observation buffers. | Unified wrapper supports both environments. |
| **12** | **Rendering Support** | **Verified.** Built-in MuJoCo offscreen and window rendering. | **Planned.** Dual camera views (`top_cam`, `front_cam`) for visual policies. | Both candidates support visual rendering. |
| **13** | **Observation-Space Suitability** | **Partially verified.** Flat 23-dim vector lacks object orientation and velocity, requiring manual extraction from `data`. | **Planned.** Structured 24-dim state vector explicitly containing pose, velocities, contact state, and remaining horizon. | Pusher-v5 observation must be augmented by environment wrapper. |
| **14** | **Action-Space Suitability** | **Verified.** 7-dim continuous torque control $[-2.0, 2.0]^7$. | **Planned.** 3-DoF/4-DoF Cartesian displacement or joint position control. | Position/displacement control simplifies baseline imitation learning. |
| **15** | **Implementation Complexity** | **Verified.** Zero implementation needed; pre-installed in Gymnasium. | **Planned.** Moderate; requires standalone MJCF XML and custom Gymnasium env class. | Pusher-v5 provides instant test harness for Phase 1. |
| **16** | **Risk of Artificial Injection** | **Partially verified.** Slide-joint constraints make the puck move like a planar air-hockey puck rather than a free physical object. | **Planned.** Realistic Coulomb friction and 3D contact manifold reduce artificiality. | Reviewers may reject slide-joint puck as unrepresentative of manipulation. |
| **17** | **Reproducibility** | **Verified.** Public standard package (`gymnasium`). | **Planned.** 100% reproducible via self-contained MJCF XML in repository. | Both candidates meet reproducibility standards. |
| **18** | **Suitability for Q1 Study** | **Not verified (Insufficient alone).** Pusher-v5 alone cannot support claims about general contact manipulation failure recovery. | **Planned.** High suitability; free-joint 3D contact slip is defensible in top-tier venues (T-RO, AURO). | Custom environment is necessary for the primary research paper. |

---

## 3. Selection Decision & Justification

### Formal Decision:
**SELECTION DEFERRED TO TWO-TIER ARCHITECTURE:**
1. **Tier 1 (Foundation & Smoke-Test Harness): Gymnasium `Pusher-v5`**
   - Retained and validated in Phase 1 as the primary operational testbed for determinism, state snapshot serialization, contact extraction, and prefix replay verification.
   - Proves that the core causal-history evaluation wrapper works with standard, unmodified Gymnasium/MuJoCo environments.
2. **Tier 2 (Primary Research Environment): `planned_custom_push_target_env`**
   - Designed to address the fatal physical limitations of Pusher-v5 (absence of object rotation, absence of binary success criteria, slide-joint constraints).
   - Scheduled for implementation once the core wrapper interfaces are verified against Pusher-v5.

### Explicit Justification for Not Relying Solely on Pusher-v5:
- **Kinematic Confinement:** In Pusher-v5, the object cannot rotate ($\theta_{\text{yaw}} \equiv 0$). Real-world manipulation failures (such as the off-center slip deviation identified in Phase 0) fundamentally involve rotational moments and contact pivot dynamics.
- **Metric Deficiencies:** Pusher-v5 provides only a continuous distance reward without an operational definition of task success ($R \in \{0, 1\}$).
- **Reviewer Vulnerability:** Submitting a paper to a Q1 robotics journal based solely on a legacy 2D slide-joint puck would invite immediate rejection for lack of physical manipulation fidelity.

