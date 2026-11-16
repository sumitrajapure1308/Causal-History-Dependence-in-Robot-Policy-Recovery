# Scientific Methodology Specification: Second Failure Mode (Contact-Loss / Premature Push Termination)

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Phase:** 10 — Outcome-Sensitivity Audit, Second-Task Pilot, and Final Benchmark Design Freeze  
**Document:** `docs/methodology/second_failure_mode_specification.md`  
**Status:** COMPLETED & SCIENTIFICALLY VALIDATED  
**Author:** Lead Robotics Researcher & Environment Architect  
**Date:** 2026-11-09  

---

## 1. Physical Motivation and Problem Definition

In contact-rich robotic manipulation, execution failures fall into two fundamentally distinct physical categories:
1. **Geometric Slip / Kinematic Pivot Failures (Failure Mode 1):** The manipulator maintains contact with the object, but an off-center contact force induces rotational torque, causing the object to rotate ($|\text{yaw}| \ge 15^\circ$) and drift laterally away from the pusher axis while contact persists.
2. **Contact-Loss / Premature Push Termination Failures (Failure Mode 2):** The manipulator loses physical contact with the object prematurely ($N_{\text{active\_contacts}} = 0$, air gap $\ge 2.0\text{ cm}$), leaving the object stranded in an uncompleted state ($d_{\text{goal}} > 8.0\text{ cm}$) with near-zero velocity.

Failure Mode 2 represents a ubiquitous failure pattern in real robot manipulation caused by motor torque limits, transient controller stalls, surface friction dips, or sensor latency.

---

## 2. Physical Contrast: Off-Center Slip vs Contact-Loss

The table below contrasts the physical, kinematic, and sensory signatures of the two failure modes:

| Dimension | Failure Mode 1: Off-Center Slip | Failure Mode 2: Contact-Loss / Premature Stall |
|---|---|---|
| **Contact Status ($N_{\text{contacts}}$)** | Active contact maintained ($N \ge 1$) | Complete contact loss ($N \equiv 0$) |
| **Object Yaw Deflection ($|\theta_{\text{yaw}}|$)** | Large rotational deviation ($15^\circ \dots 40^\circ$) | Minimal yaw deflection ($< 8^\circ$) |
| **Manipulator-Object Gap** | Zero ($d_{\text{ee, obj}} \le 0.001\text{ m}$) | Significant air gap ($d_{\text{ee, obj}} \ge 0.020\text{ m}$) |
| **Object Dynamic State** | Sliding/rotating under pusher contact force | Stationary or decelerating freely ($\|v_{\text{obj}}\| \approx 0$) |
| **Failure Inducer** | Lateral offset push ($y_{\text{offset}} \in [0.014, 0.020]$ m) | Transient deceleration / retraction pulse |
| **Primary Recovery Maneuver Required** | Lateral standoff + rotational re-alignment | Forward re-acquisition + gap closure + resumed push |

---

## 3. Physical Generation Protocol (Strict No-Teleportation Guarantee)

In strict adherence to the project rules:
> **The failure must NOT be created by teleporting the object.**

Contact-loss is induced entirely through continuous physical forward simulation:
1. **Nominal Push Phase:** The robot advances forward toward the object, establishing normal contact and pushing along the approach trajectory for $t \in [0, t_{\text{perturb}}-1]$.
2. **Transient Deceleration Injection:** At step $t_{\text{perturb}}$ (typically step 20–30), a physical deceleration control delta ($a_x \in [-0.015, -0.020]\text{ m/step}$, $a_y = 0$) is applied to the Cartesian servos for $K = 2\text{ to }3$ simulation steps.
3. **Natural Momentum & Separation:** The robot slows and halts, while the object slides forward by a few millimeters under Coulomb friction and comes to rest.
4. **Air-Gap Emergence:** The robot and object physically separate through standard MuJoCo forward integration (`mj_step`), establishing an air gap of $2.0\text{ to }3.5\text{ cm}$ with zero artificial discontinuity in coordinates or velocities.

---

## 4. Automated Detection and Measurement Criteria

A state is classified as an admitted **Contact-Loss Failure** if and only if all of the following conditions are simultaneously verified:
1. **Zero Active Contacts:** $N_{\text{contacts}}(\text{pusher}, \text{object}) \equiv 0$ for $\ge 3$ consecutive steps.
2. **Spatial Separation:** Air gap between pusher surface and object surface exceeds $0.020\text{ m}$ ($2.0\text{ cm}$).
3. **Incomplete Task:** Distance to goal exceeds completion threshold ($d_{\text{goal}} \ge 0.080\text{ m}$).
4. **Dynamic Equilibrium:** Object linear speed is below threshold ($\|v_{\text{obj}}\| \le 0.010\text{ m/s}$).
5. **Table Containment:** Object remains securely on the table surface ($z_{\text{obj}} \ge 0.015\text{ m}$, $|x_{\text{obj}}| \le 0.40\text{ m}$, $|y_{\text{obj}}| \le 0.40\text{ m}$).

---

## 5. Privileged Oracle Recoverability Verification

To guarantee that failure scenarios are mechanically solvable within the remaining horizon:
- A privileged geometric recovery controller (`ContactLossOracleController`) computes the vector from pusher to object center, closes the gap at maximum safe speed, establishes centered contact, and executes a closed-loop push to the target.
- If the privileged oracle solves the recovery within the remaining horizon ($R_{\text{oracle}} = 1$), the failure scenario is admitted.
- If the privileged oracle fails (e.g. remaining horizon $< 30$ steps or object past workspace bounds), the failure is rejected from the evaluation denominator.

