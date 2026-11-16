# Gymnasium Pusher-v5 Compatibility & Scientific Suitability Report

> **Evaluation Standard:** Empirical Inspection of Gymnasium MuJoCo Pusher-v5  
> **Auditors:** Lead Robotics Researcher & Reproducibility Auditor  
> **Verdict:** **SUFFICIENT AS API & REPRODUCIBILITY TEST HARNESS; INSUFFICIENT AS SOLE RESEARCH BENCHMARK**  
> (Retained in Phase 1 for wrapper verification, determinism benchmarking, and prefix-replay unit tests; custom 6-DoF environment required for primary causal-history study).

---

## 1. Item-by-Item Scientific Audit

| Property / Criterion | Empirical Finding & Evidence | Verification Status | Limitation & Scientific Consequence |
|---|---|---|---|
| **1. Meaningful Recoverable Deviation** | **Empirical test:** 7-DoF arm can miss the puck or bump it laterally. If puck remains within the reachable workspace (approx $x \in [-0.3, 0.3], y \in [-0.4, 0.4]$), an agent can re-approach. | **Partially verified.** | Deviations are strictly translational lateral offsets. Angular slip or tilting does not exist. |
| **2. Pusher-Object Contact Extraction** | **Empirical test:** MuJoCo `d.contact` logs contacts between table (`geom 0`), puck (`geom 18`), and arm tips (`tip_arml`, `tip_armr`). Contact normal forces and slip distances are available. | **Verified.** | Object geom name is an unassigned empty string (`''`); extractor must match by geom body ID (`geom_bodyid == 11`). |
| **3. Off-Center Pushing / Slip Induction** | **Empirical test:** Object body has exactly 2 joints: `obj_slidey` (type 2: slide) and `obj_slidex` (type 2: slide). **Zero rotational joints.** | **Not verified (Physically Impossible).** | **Critical limitation:** Rotational slip and yaw deflection ($\Delta \theta > 15^\circ$) cannot occur physically. Object translates without spinning. |
| **4. Post-Deviation Goal Reachability** | **Empirical test:** If the puck is displaced $< 0.15$ m from nominal trajectory, the arm's kinematic workspace can reach and redirect it toward the goal. | **Verified.** | Pusher kinematics are sufficient for translational recovery. |
| **5. Direct State Injection Validity** | **Empirical test:** Setting `set_state(qpos, qvel)` is operational. However, setting arbitrary non-zero velocities on slide joints while resting on the table can cause momentary normal force spikes. | **Partially verified.** | Direct injection must set `qacc_warmstart` and verify zero table penetration to avoid artificial impulse spikes. |
| **6. State Accessibility** | **Empirical test:** Full generalized coordinates $q \in \mathbb{R}^{11}$, velocities $\dot{q} \in \mathbb{R}^{11}$, and tip poses are directly accessible from `env.unwrapped.data`. | **Verified.** | 100% Markovian visibility. |
| **7. Action Space Suitability** | **Empirical test:** 7 continuous joint torque commands $[-2.0, 2.0]^7$ at 20 Hz control frequency (simulation timestep $0.01$ s, frame skip 5). | **Verified.** | Joint torque actions require closed-loop feedback or impedance control for stable baseline recovery. |
| **8. Observation Space Suitability** | **Empirical test:** Default observation is flat 23-dim vector. Contains arm joint angles, tip pos, object pos, goal pos, object-to-goal vector. | **Partially verified.** | Lacks object linear velocities in default observation; wrapper must append velocities to support Markovian observation matching. |
| **9. Native Success Criterion** | **Empirical test:** `env.step()` returns `info = {'reward_dist': ..., 'reward_ctrl': ..., 'reward_near': ...}`. **No `success` key exists. Episode terminates only on max step truncation (100 steps).** | **Not verified (Deficient).** | **Critical limitation:** Standard Pusher-v5 lacks a binary success definition ($R \in \{0, 1\}$); an external task-success criterion must be implemented by the wrapper. |
| **10. Horizon Synchronization** | **Empirical test:** Default episode length is 100 steps. Injected episodes must enforce remaining horizon $\Delta t_{\text{remain}} = 100 - t_d$. | **Verified.** | Easily synchronized via environment wrapper. |
| **11. Beyond-Pixel State Matching** | **Empirical test:** Weighted Euclidean distance over joint coordinates and Cartesian positions is easily computable. | **Verified.** | Fully supports physical state distance matching. |
| **12. Restoration Fidelity** | **Empirical test:** Snapshot and restoration of `qpos, qvel, warmstart, time` yields exact $0.0$ state divergence across 15 post-restore rollout steps. | **Verified.** | Bitwise deterministic state restoration confirmed. |

---

## 2. Synthesis & Methodological Decision

1. **Why Pusher-v5 Cannot Be the Final Q1 Research Benchmark:**
   - **Absence of Rotational Dynamics:** Manipulation failure recovery in top robotics venues (IEEE T-RO, AURO) demands contact-rich physical interaction. A puck constrained to 2D slide rails without rotation, tipping, or Coulomb friction moments cannot represent genuine manipulation failures (e.g. pivoting slip, edge jamming, or grasp instability).
   - **Missing Task Success Semantics:** Lacking an intrinsic task success metric, any recovery success rate would depend on an arbitrary post-hoc distance threshold not recognized by the standard benchmark.
2. **Role of Pusher-v5 in Phase 1:**
   - Pusher-v5 serves as the **validated baseline implementation harness** for the Phase 1 environment wrapper.
   - It validates:
     - Deterministic reset and explicit seed control.
     - State snapshot serialization and restoration.
     - Contact extraction logic.
     - Action-prefix replay and drift quantification.
     - Direct state-injection interfaces.
   - This ensures the entire software infrastructure is proven on an established standard environment before deploying the custom 6-DoF contact environment.

