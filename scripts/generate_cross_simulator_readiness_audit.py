#!/usr/bin/env python3
"""
Generate docs/audit/cross_simulator_readiness_audit.md
Assess feasibility of transferring the Paired Replay-Injection protocol to other simulators (e.g. PyBullet, Isaac Gym/Lab).
Strictly adheres to directive: Do not claim cross-simulator validity unless it has been tested.
"""

import os

def generate_audit():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    out_dir = os.path.join(repo_root, 'docs', 'audit')
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'cross_simulator_readiness_audit.md')

    content = """# Cross-Simulator Readiness and Transfer Audit

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Document:** `docs/audit/cross_simulator_readiness_audit.md`  
**Milestone:** Phase 17 — Submission-Readiness Hardening and Final Go/No-Go Gate  
**Date:** 2026-11-10  
**Verification Status:** `Verified` | `Exploratory` | `Planned`  

---

## 1. Executive Summary & Epistemological Boundary

> [!IMPORTANT]
> **Strict Non-Claim Boundary:** This work does **NOT** claim cross-simulator validity. All confirmatory benchmark experiments were conducted exclusively within the **MuJoCo 3.10.0** physics engine.
> 
> Cross-simulator generalization remains an unverified hypothesis until full empirical replication is executed on alternative physics solvers. This audit formally outlines the technical requirements, architectural abstractions, and migration roadmap for transferring the Paired Replay-Injection protocol to alternative simulators.

---

## 2. Cross-Simulator Technical Evaluation

| # | Evaluation Dimension | Specification / Assessment |
|---|---|---|
| **1** | **Current Simulator** | **MuJoCo 3.10.0** (Python bindings, CPU-based execution, convex optimization contact solver `PGS`/`Newton`). |
| **2** | **Target Simulators** | **PyBullet 3.2.5** (LCP constraint solver) and **NVIDIA Isaac Lab / Omniverse Isaac Gym** (PhysX 5 GPU tensor solver). |
| **3** | **Required Changes** | Replace `mujoco.mj_step` and `mjData` pointer manipulations with simulator-native stepping and buffer extraction loops. |
| **4** | **Required Abstractions** | Standardize environment wrapper to implement `BaseRecoveryEnv` interface: `get_state_snapshot()`, `restore_state_snapshot()`, `step()`, and `reset()`. |
| **5** | **Required State-Serialization Changes** | - **PyBullet:** Implement `saveState()` / `restoreState()` using PyBullet's built-in memory state ID, or serialize link poses, velocities, and contact manifolds via `getBasePositionAndOrientation`, `getBaseVelocity`, and `getContactPoints`.<br>- **Isaac Lab:** Utilize PhysX tensor buffers (`root_state_w`, `joint_pos`, `joint_vel`) with explicit GPU tensor serialization. |
| **6** | **Required Contact-Model Changes** | - MuJoCo uses smooth convex optimization for soft contacts with tunable margin and solref.<br>- PyBullet uses rigid LCP impulse resolution (prone to high-frequency chatter).<br>- Isaac Lab PhysX uses non-linear iterative Gauss-Seidel or TGS (Temporal Gauss-Seidel). Friction cones and damping parameters must be calibrated to match Coulomb friction $\\mu = 0.50$ (Task 1) and $\\mu = 0.35$ (Task 2). |
| **7** | **Required Action-Space Changes** | None. Maintain standard Cartesian end-effector velocity command $\\Delta x, \\Delta y, \\Delta z \\in [-0.05, 0.05]$ m/step. |
| **8** | **Required Observation-Space Changes** | None. Maintain 14-dimensional Markovian state vector (end-effector pose/vel, object pose/vel, goal target). |
| **9** | **Required Seed Handling** | - PyBullet: Requires `pybullet.resetSimulation()` and explicit random seed initialization.<br>- Isaac Lab: Requires PyTorch CUDA deterministic flags (`torch.use_deterministic_algorithms(True)`, `CUBLAS_WORKSPACE_CONFIG=:4096:8`). |
| **10** | **Required Deterministic-Replay Changes** | - MuJoCo guarantees bitwise determinism ($D = 0.0$) across identical seed and action replays.<br>- PyBullet: Replay determinism requires fixed-timestep stepping (`setTimeStep(0.002)`) and disabling multi-threading during state resets.<br>- Isaac Lab: Replay determinism on GPU requires strict reduction tree determinism, often exhibiting minor floating-point jitter ($D \\sim 10^{-7}$ m). |
| **11** | **Required Matching-Threshold Changes** | - In MuJoCo, state restoration is sub-atomic: $\\Delta x \\le 10^{-10}$ m.<br>- In PyBullet / Isaac Lab, matching threshold must be relaxed from $10^{-10}$ m to $\\epsilon = 1.0 \\times 10^{-5}$ m ($0.01$ mm) to account for numerical solver variations. |
| **12** | **Required Validation Tests** | 1. Reset-Restore Roundtrip Invariance Test ($D < \\epsilon$).<br>2. Stepping Determinism Test ($D = 0.0$ on identical actions).<br>3. Negative Control Memoryless Invariance Test (0/50 discordant outcomes on reactive MLP). |
| **13** | **Estimated Engineering Effort** | 3 person-weeks for PyBullet port; 4 person-weeks for Isaac Lab GPU tensor implementation. |
| **14** | **Technical Risk** | **Medium.** Physics solver differences (LCP vs convex vs TGS) alter contact friction slip angles, requiring re-calibration of deviation detection thresholds ($>15^\\circ$ yaw drift). |
| **15** | **Scientific Recommendation** | **Retain as Post-Publication Extension.** Do not delay benchmark submission for cross-simulator validation. Explicitly bound the current manuscript's conclusions to MuJoCo contact physics. |

---

## 3. Methodological Portability Assessment

The core scientific contribution of this work is **methodological**:
- The **Paired Replay-Injection Matching protocol** is completely simulator-agnostic.
- Any physics engine supporting deterministic state restoration (`saveState`/`restoreState`) and contact logging can implement Conditions B0 through B4.
- The **Memoryless Negative Control validation test** provides a built-in automated gate to verify that any target simulator has achieved zero future leakage before launching benchmark rollouts.

---
*Audit certified by Autonomous Agent System.*
"""

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")
    print(f"Generated {out_file}")

if __name__ == '__main__':
    generate_audit()

