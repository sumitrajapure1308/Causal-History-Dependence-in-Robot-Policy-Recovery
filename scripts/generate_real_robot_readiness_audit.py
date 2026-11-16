#!/usr/bin/env python3
"""
Generate docs/audit/real_robot_readiness_audit.md
Assess feasibility and requirements for transferring the Paired Replay-Injection protocol to physical robot hardware.
Strictly adheres to directive: Do not claim real-robot validity unless it has been tested.
"""

import os

def generate_audit():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    out_dir = os.path.join(repo_root, 'docs', 'audit')
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'real_robot_readiness_audit.md')

    content = """# Real-Robot Readiness and Hardware Transfer Audit

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Document:** `docs/audit/real_robot_readiness_audit.md`  
**Milestone:** Phase 17 — Submission-Readiness Hardening and Final Go/No-Go Gate  
**Date:** 2026-11-10  
**Verification Status:** `Verified` | `Exploratory` | `Planned`  

---

## 1. Executive Summary & Epistemological Boundary

> [!IMPORTANT]
> **Strict Non-Claim Boundary:** This work does **NOT** claim real-world robot hardware validity. All experiments were conducted in simulation. 
> 
> Real-world physical robots involve unobservable internal states, non-repeatable contact micro-mechanics, sensor latency, optical tracking noise, and irreversible physical damage risks. This audit provides an exhaustive feasibility analysis and concrete blueprint for future hardware replication on a physical manipulator arm.

---

## 2. 16-Dimension Hardware Readiness Evaluation

| # | Evaluation Dimension | Specification / Assessment |
|---|---|---|
| **1** | **Current Simulator** | **MuJoCo 3.10.0** physics simulation (3-DoF Cartesian pusher, 6-DoF free cube/puck, Coulomb contact solver). |
| **2** | **Target Robot Hardware** | **Franka Emika Panda (7-DoF)** or **Universal Robots UR5e (6-DoF)** equipped with a rigid cylindrical 3D-printed pusher end-effector, high-precision overhead camera, and optoelectronic motion capture (e.g., OptiTrack / Vicon). |
| **3** | **Required Changes** | Interface with real-time robot controller (e.g., `libfranka` / `ur_rtde` at 100 Hz-1000 Hz). Replace simulation step calls with hardware control packets. |
| **4** | **Required Abstractions** | Abstract robot hardware behind a ROS 2 / Python Gym interface adhering to `BaseRecoveryEnv`. Implement automatic reset routines (e.g., automated object resetting via dual-arm or pneumatic slide). |
| **5** | **Required State-Serialization Changes** | On hardware, internal physical states cannot be saved/restored via pointer copies. Physical state injection requires **Active Physical Placement**: robot moves to Cartesian pose $x_{ee}$, and an auxiliary robotic gripper or human operator places the cube at measured 6D pose $(x, y, z, \\theta_{yaw})$. |
| **6** | **Required Contact-Model Changes** | Real-world surface interaction involves non-uniform friction, microscopic table irregularities, surface wear, and stick-slip chatter. Real friction $\\mu$ must be empirically calibrated using force-torque sensor drag tests. |
| **7** | **Required Action-Space Changes** | End-effector Cartesian velocity commands must pass through an inverse kinematics (IK) solver with joint acceleration and jerk limits to ensure hardware safety. |
| **8** | **Required Observation-Space Changes** | In simulation, ground-truth object poses are extracted directly from `mjData.qpos`. On hardware, object poses must be estimated using motion capture rigid-body markers or visual fiducials (AprilTags) / 6D object pose trackers (e.g., BundleSDF / FoundationPose) at $\\ge 60$ Hz. |
| **9** | **Required Seed Handling** | Physical hardware lacks pseudo-random number generator seeding. Initial scenario conditions must be generated via physical randomization jigs or scripted grid-based object placement. |
| **10** | **Required Deterministic-Replay Changes** | Physical replays are strictly non-deterministic due to motor backlash, thermal drift, sensor jitter, and chaotic contact bifurcations. Exact trajectory repeatability is limited to $\\approx 1.0$ mm - $2.0$ mm error. |
| **11** | **Required Matching-Threshold Changes** | The simulation threshold of $D \\le 1.0 \\times 10^{-10}$ m is physically impossible on real hardware. The physical matching threshold must be relaxed to: $\\Delta x_{\\text{pos}} \\le 2.0$ mm, $\\Delta \\theta_{\\text{yaw}} \\le 1.0^\\circ$, verified by motion capture before releasing the policy. |
| **12** | **Required Safety Constraints** | Implement Cartesian workspace geofences ($x \\in [0.1, 0.6]$, $y \\in [-0.3, 0.3]$, $z \\ge 0.0$ m), contact force limits ($F_z \\le 25$ N via Panda torque sensors), and automated emergency stop (E-stop) upon erratic velocity commands. |
| **13** | **Required Hardware Validation** | Validate that identical open-loop action sequences reproduce off-center slip deviations consistently ($>15^\\circ$ yaw deflection) within a bounded spatial envelope across 20 trials. |
| **14** | **Required Human-Subject Validation** | **Not applicable.** The task evaluates autonomous robot manipulation of passive inanimate objects. No human subjects are involved. |
| **15** | **Estimated Engineering Effort** | 8-12 person-weeks of dedicated robotics lab engineering (motion capture setup, automatic reset mechanism, ROS 2 integration, and calibration). |
| **16** | **Technical Risk & Bottleneck** | **High Technical Risk:** Physical state reset on real hardware is labor-intensive and subject to reset hysteresis. Without an automated reset mechanism, running even 500 physical trials requires tens of hours of manual object placement. |

---

## 3. Scientific Recommendation & Venue Strategy

```
+--------------------------------------------------------------------------------------------------+
|                                    VENUE COMPLIANCE AUDIT                                        |
+--------------------------------------------------------------------------------------------------+
| Venue Type                    | Examples                 | Hardware Requirement | Strategy       |
+-------------------------------+--------------------------+----------------------+----------------+
| Premier Benchmark Tracks      | NeurIPS D&B Track,       | Simulation Only is   | **SUBMIT**     |
| & AI Systems Conferences      | RSS, CoRL, IEEE RA-L     | Standard & Accepted  | (Recommended)  |
+-------------------------------+--------------------------+----------------------+----------------+
| Flagship Hardware Journals    | IEEE T-RO,               | Mandatory Hardware   | **DO NOT SUBMIT|
|                               | IJRR                     | Trials Required      | (High Risk)    |
+-------------------------------+--------------------------+----------------------+----------------+
```

### Recommendation:
1. **Target Benchmark and Robotics Systems Venues First:** Submit the simulation benchmark as a pristine, pre-registered release candidate to **NeurIPS Datasets & Benchmarks Track**, **Robotics: Science and Systems (RSS)**, or **IEEE RA-L**.
2. **Explicitly Document Real-Robot Bounding:** In the manuscript Section 5.1 (Scope of Validity) and Section 6 (Limitations), state:
   > *"All experiments are conducted in rigid-body physics simulation. While simulation permits sub-atomic matched-state injection impossible on physical hardware, real-robot verification under motion-capture state matching remains an essential future work."*
3. **Hardware Extension Roadmap:** Reserve physical Franka Panda hardware trials for a follow-up extended journal archival paper after the foundational benchmark methodology is peer-reviewed.

---
*Audit certified by Autonomous Agent System.*
"""

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")
    print(f"Generated {out_file}")

if __name__ == '__main__':
    generate_audit()

