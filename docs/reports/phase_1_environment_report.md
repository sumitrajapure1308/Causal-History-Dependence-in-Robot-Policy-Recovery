# Phase 1 Environment & Simulator Validation Report

> **Execution Milestone:** Phase 1 (Restricted to Environment and Simulator Validation)  
> **Auditors:** Lead Robotics Researcher, Software Architect & Reproducibility Auditor  
> **Status:** **VALIDATION COMPLETE — EXPERIMENTS PAUSED**  
> **Mandate:** No official experiments executed; no policy training started.

---

## 1. Candidate Environment Comparison

An 18-dimension empirical audit comparing Gymnasium `Pusher-v5` against the `planned_custom_push_target_env` is documented in [`docs/methodology/environment_selection_decision.md`](file:///D:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/methodology/environment_selection_decision.md) and [`docs/methodology/pusher_v5_compatibility_report.md`](file:///D:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/methodology/pusher_v5_compatibility_report.md).

### Summary Audit Matrix:
| Dimension | Candidate A: Gymnasium `Pusher-v5` | Candidate B: `planned_custom_push_target_env` | Status |
|---|---|---|---|
| **Physics Engine** | MuJoCo 3.10.0 (Native) | MuJoCo 3.10.0 (Custom MJCF) | **Verified** |
| **Object Mobility** | 2D Slide Joints (`obj_slidex`, `obj_slidey`) | 6-DoF Free Joint (`type="free"`) | **Verified (A) / Planned (B)** |
| **Rotational Slip ($\Delta \theta > 15^\circ$)** | Physically Impossible (No angular DoF) | Physically Realistic (Full Coulomb yaw moments) | **Not verified (A) / Planned (B)** |
| **Task Success Metric** | Missing natively (continuous distance only) | Explicit binary threshold ($\|p_{\text{obj}} - p_{\text{goal}}\| \le r$) | **Not verified (A) / Planned (B)** |
| **State Serialization & Replay** | Bitwise deterministic ($0.0$ drift) | Bitwise deterministic | **Verified (A) / Planned (B)** |
| **Contact Manifold Visibility** | Accessible via `d.contact` | Accessible with explicit contact sensors | **Verified (A) / Planned (B)** |
| **Q1 Research Suitability** | Insufficient alone for general manipulation claims | High suitability for top-tier publication | **Audited** |

---

## 2. Selected Environment Decision & Justification

- **Decision:** **SELECTION DEFERRED TO TWO-TIER ARCHITECTURE**
- **Justification:**
  1. **Tier 1 (Foundation & Smoke-Test Harness): Gymnasium `Pusher-v5`**  
     *Role:* Operational baseline. Validates wrapper architecture, determinism, state snapshots, prefix replay, and test automation on a standard, third-party benchmark.
  2. **Tier 2 (Primary Research Environment): `planned_custom_push_target_env`**  
     *Role:* Primary experimental platform for Phase 2+. Required because `Pusher-v5` kinematically locks object rotation via prismatic slide joints, making off-center rotational slip deviations physically impossible.

---

## 3. State Snapshot Specification & Completeness Audit

Full audit documented in [`docs/methodology/state_snapshot_audit.md`](file:///D:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/methodology/state_snapshot_audit.md).

### Restorable Fields (Bitwise Verified):
1. `qpos`: Generalized coordinates `float64 (11,)` — **Verified**
2. `qvel`: Generalized velocities `float64 (11,)` — **Verified**
3. `act`: Actuator internal state — **Verified**
4. `qacc_warmstart`: Constraint solver acceleration initial guess — **Verified**
5. `qfrc_applied` & `xfrc_applied`: Applied external forces/torques — **Verified**
6. `ctrl`: Control signal buffer — **Verified**
7. `time`: Simulation time — **Verified**
8. `step_count`: Elapsed episode steps — **Verified**
9. `remaining_horizon`: Remaining recovery step budget ($T - t_d$) — **Verified**
10. `task_goal`: Goal spatial target vector — **Verified**

### Fields Generated Dynamically:
- `contact information` (`d.contact`): In MuJoCo, contact structures bind to internal solver pointers. Restoring `qpos` and `qvel` followed by `mujoco.mj_forward(model, data)` regenerates the identical contact manifold without phantom impulses — **Verified**.

### Non-Restorable Fields:
- None. No relevant Markovian simulator state is omitted or unverified.

---

## 4. Empirical Test Results & Verification Summary

All 17 automated unit tests passed cleanly via `pytest causal-history-recovery/tests/` (Execution time: 1.66s):

| Test Suite | Tests | Result | Verification Status |
|---|---|---|---|
| **Determinism (`test_determinism.py`)** | `test_reset_determinism`, `test_stepping_determinism`, `test_distinct_seeds_produce_variation` | **PASS (3/3)** | **Verified** ($0.0$ divergence) |
| **State Snapshot (`test_state_snapshot.py`)** | `test_snapshot_restore_exactness`, `test_serialization_roundtrip_npz`, `test_restore_and_step_no_accumulated_drift`, `test_state_distance_metric_consistency` | **PASS (4/4)** | **Verified** ($0.0$ drift) |
| **Contact Extraction (`test_contact_extraction.py`)** | `test_contact_extraction_repeatability`, `test_contact_filtering_table_and_object`, `test_restoration_no_unreported_impulses` | **PASS (3/3)** | **Verified** (no phantom impulses) |
| **Prefix Replay (`test_prefix_replay.py`)** | `test_prefix_replay_bounded_error`, `test_prefix_replay_goal_preservation` | **PASS (2/2)** | **Verified** (error $< 10^{-10}$) |
| **State Injection (`test_state_injection.py`)** | `test_state_injection_goal_preservation`, `test_state_injection_horizon_preservation`, `test_state_injection_observation_consistency` | **PASS (3/3)** | **Verified** (error $< 10^{-8}$) |
| **Package Imports (`test_imports.py`)** | `test_main_package_import`, `test_submodule_imports` | **PASS (2/2)** | **Verified** |

---

## 5. Technical Discoveries & Mitigations in MuJoCo

### Discovery: Kinematic Synchronization in Gymnasium MuJoCo
During injection testing, an apparent observation divergence of $0.00071$ m ($0.7$ mm) in `tips_arm` body Cartesian position was diagnosed:
- **Root Cause:** In Gymnasium's legacy `MujocoEnv.step()`, `mj_step` integrates `qpos` and `qvel` to time $t+dt$, but does not run the forward kinematics pass (`mj_forward`) at the conclusion of the step. Consequently, reading `d.body.xpos` immediately after `step()` yields Cartesian positions from time $t$, whereas reading `d.qpos` yields generalized coordinates from time $t+dt$.
- **Architectural Solution:** `MuJoCoWrapperEnv.step()` explicitly calls `mujoco.mj_forward(self.model, self.data)` before observation extraction, ensuring body COM, Cartesian kinematics, and contact manifolds are bitwise synchronized with generalized coordinates.
- **Verification:** Re-evaluating post-injection observation difference after forward synchronization yielded exact $0.0$ divergence.

---

## 6. Staged History Intervention Readiness

Documented in [`docs/methodology/staged_history_ablation.md`](file:///D:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/methodology/staged_history_ablation.md), five distinct intervention conditions ($B0$ through $B4$) are formalized:
- **$B0$ (Full Replay):** Full observation, action, contact, and policy hidden state preserved.
- **$B1$ (Action History Removed):** Action buffer zeroed; observation and contact preserved.
- **$B2$ (Observation History Removed):** Observation buffer reduced to instantaneous $k=1$.
- **$B3$ (Policy Memory Reset):** Recurrent hidden state $h_t^{\pi}$ reset to zero.
- **$B4$ (Combined Matched Injection):** Physical state injected; all prior history streams reset.
- *Readiness Status:* Interfaces implemented in `MuJoCoWrapperEnv`; official evaluations deferred to Phase 6.

---

## 7. Novelty Boundaries Protected

Documented in [`docs/literature/novelty_boundary.md`](file:///D:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/literature/novelty_boundary.md):
- **Prior Art Grounding:** Replayed prefix deviations (RoboRecover), multi-level recovery (LIBERO-Recover), and runtime interventions (LIBERO-Pro2.0) are formally credited and barred from being claimed as project contributions.
- **Central Contribution Statement Frozen:**
  > *“A physically matched-state evaluation protocol for measuring the effect of controlled causal-history interventions on robot recovery.”*

---

## 8. Exact Files Created & Modified in Phase 1

### Files Created:
1. `src/causal_history_recovery/environments/base_env.py`
2. `src/causal_history_recovery/environments/state_snapshot.py`
3. `src/causal_history_recovery/environments/contact_extractor.py`
4. `src/causal_history_recovery/environments/mujoco_wrapper.py`
5. `configs/matching/determinism.yaml`
6. `docs/methodology/environment_selection_decision.md`
7. `docs/methodology/pusher_v5_compatibility_report.md`
8. `docs/methodology/state_snapshot_audit.md`
9. `docs/methodology/staged_history_ablation.md`
10. `docs/literature/novelty_boundary.md`
11. `docs/reports/phase_1_environment_report.md`
12. `tests/test_determinism.py`
13. `tests/test_state_snapshot.py`
14. `tests/test_contact_extraction.py`
15. `tests/test_prefix_replay.py`
16. `tests/test_state_injection.py`

### Files Modified:
1. `PROJECT_STATUS.md` (Updated Phase 1 status from `planned` to `validated`)

---

## 9. Remaining Blockers
- **None.** Simulator foundation, determinism, contact extraction, state serialization, and prefix replay are 100% verified.

---

## 10. Recommendation for Phase 2
- When approved, proceed to **Phase 2: One Task and Baseline Policy Implementation**.
- Implement the custom 6-DoF free-joint cube pushing task (`planned_custom_push_target_env`), train standard reactive and recurrent baseline policies to establish nominal task competence ($\ge 90\%$), and implement the privileged oracle controller.

---

Phase 1 environment validation is complete. Official experiments remain paused pending explicit user approval.

