# Task Availability & Environment Status Audit

> **Status:** AUDITED & CLARIFIED  
> **Task Planning Reference:** `planned_custom_push_target_env`  
> **Classification:** **Planned Custom Environment (Not Yet Implemented / Tested)**

---

## 1. Truth in Environment Classification

| Environment Identifier | Classification | Explanation |
|---|---|---|
| `Push-to-Target-v0` | **INVENTED PLANNING PLACEHOLDER** | This was an ad-hoc placeholder used in preliminary drafting. It is **not** an existing installed environment in Gymnasium or MuJoCo, nor does it currently exist in local codebase. |
| `Pusher-v4` / `Pusher-v5` | **INSTALLED GYMNASIUM MUJOCO BENCHMARK** | Native Gymnasium environment (`gymnasium.make('Pusher-v5')`). Available in the installed `gymnasium` package. |
| `planned_custom_push_target_env` | **PLANNED CUSTOM RESEARCH ENVIRONMENT** | The planned contact-rich manipulation environment to be implemented and validated in Phase 1. Designed specifically to support deterministic state serialization, exact contact manifold logging, and sub-millimeter matched-state injection. |

---

## 2. Environment Specification & Implementation Status (`planned_custom_push_target_env`)

| Property | Status | Technical Details |
|---|---|---|
| **Environment Source** | Planned Custom | To be implemented in `src/causal_history_recovery/environments/push_task.py` with standalone MJCF model. |
| **Implementation Status** | **UNAVAILABLE / NOT YET IMPLEMENTED** | Implementation is scheduled for Phase 1. No claims of operational status are made prior to implementation. |
| **Action Space** | Planned | Continuous Cartesian displacement $[\Delta x, \Delta y, \Delta z] \in [-0.05, 0.05]^3$ (or joint position deltas for 3-DoF arm). |
| **Observation Space** | Planned | Composite low-dimensional vector: $[p_{ee}, \dot{p}_{ee}, p_{\text{obj}}, R_{\text{obj}}, v_{\text{obj}}, \omega_{\text{obj}}, c, g, \Delta t_{\text{remain}}] \in \mathbb{R}^{24}$. |
| **Reset Behavior** | Planned | Deterministic seeded reset sampling initial block pose $p_0 \sim \mathcal{U}([-0.05, 0.05]^2)$ and locking robot start pose. |
| **State Serialization Support** | Planned | Full `mjData` serialization via `mj_getState` / `mj_setState` (including `qpos`, `qvel`, `act`, `warmstart`). |
| **Contact Extraction Support** | Planned | Extraction of contact geom IDs, normal contact forces, and slip vectors from `mjData.contact`. |
| **Rendering Support** | Planned | MuJoCo off-screen EGL/OSMesa/GLFW renderer generating $256 \times 256$ RGB frames from fixed front and top cameras. |
| **Determinism Test Status** | **NOT YET TESTED (PLANNED FOR PHASE 1)** | Gate criterion: Stepping identical action sequences twice from the same seed must produce $< 10^{-12}$ $L_2$ state drift. |

---

## 3. Alternative Existing Fallback Option: Standard `Pusher-v5`

If custom MJCF environment development encounters unexpected physics solver delays during Phase 1, the installed Gymnasium environment `Pusher-v5` is available as a verified fallback:
- **Package:** `gymnasium[mujoco]` (Installed: Gymnasium 1.3.0, MuJoCo 3.10.0).
- **Robot:** 7-DoF arm pushing a cylindrical object to a target on a flat surface.
- **State Serialization:** Supports MuJoCo `qpos` and `qvel` state extraction.
- **Limitation of Fallback:** `Pusher-v5` uses simplified cylindrical geometries and generalized coordinates without rich square block pivot slip or contact force logging interfaces. Therefore, the custom `planned_custom_push_target_env` remains the strongly preferred primary design.

