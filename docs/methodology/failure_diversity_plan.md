# Failure Diversity & Perturbation Sampling Plan

> **Document Type:** Research Methodology Specification  
> **Project:** Causal-History Dependence in Robot Policy Recovery  
> **Phase:** 5 (Paired Scenario Generation & Matching-Yield Optimization)  
> **Status:** `Verified & Operational`  
> **Compliance:** Strict adherence to continuous physical mechanics; zero object teleportation.

---

## 1. Scientific Motivation & Problem Statement

In the Phase 3 pilot evaluation, failure injection was restricted to a single fixed parameter: a lateral offset of $\Delta y = +0.016\text{ m}$ injected at step $t=25$. While this validated the basic mechanics of contact slip detection, a single failure severity introduces several scientific limitations:
1. **Floor and Ceiling Artifacts:** If a perturbation is uniformly severe, all policies fail regardless of history; if uniformly mild, all recover trivially.
2. **Narrow Regime Confounding:** History dependence may exhibit non-linear thresholds: subtle contact slips may be easily absorbed by memoryless feedback, whereas moderate slips may require temporal context to diagnose and correct.
3. **Distributional Generalization:** A benchmark claiming to evaluate recovery must reflect diverse real-world failure configurations (e.g., varying contact eccentricity, timing along the trajectory, directionality, and initial poses).

---

## 2. Multi-Dimensional Perturbation Sampling Space

The Phase 5 protocol systematically samples across five controlled physical dimensions:

### 2.1 Contact Eccentricity (Severity Tiers)
- **Small Offset ($\Delta y \in [0.008, 0.011]\text{ m}$):** Mild contact asymmetry. Induces subtle yaw deflections ($\theta \in [10^\circ, 18^\circ]$) and slight lateral slip ($\Delta y \in [1.2, 1.8]\text{ cm}$). Easily recoverable by closed-loop controllers.
- **Medium Offset ($\Delta y \in [0.014, 0.017]\text{ m}$):** Moderate contact asymmetry. Produces pronounced yaw rotation ($\theta \in [18^\circ, 28^\circ]$) and lateral displacement ($\Delta y \in [1.8, 2.5]\text{ cm}$).
- **Large Offset ($\Delta y \in [0.019, 0.022]\text{ m}$):** Severe contact asymmetry near the geometric edge of the cube facet. Induces sharp rotational slip ($\theta \in [28^\circ, 40^\circ]$) and large displacement ($\Delta y > 2.5\text{ cm}$). Challenges manipulator reachability and recovery horizon.

### 2.2 Perturbation Timing Along Execution Horizon ($t_{\text{pert}}$)
- **Early Stage ($t_{\text{pert}} = 20$):** High remaining horizon ($T - t_d \approx 120$ steps). Allows maximum time for corrective maneuvers, but errors have longer to compound.
- **Mid-Early Stage ($t_{\text{pert}} = 25$):** Established steady-state pushing phase.
- **Mid-Late Stage ($t_{\text{pert}} = 30$):** Approaching intermediate transit region.
- **Late Stage ($t_{\text{pert}} = 35$):** Lower remaining horizon ($T - t_d \approx 80-95$ steps). Demands rapid recovery reaction.

### 2.3 Directional Symmetry ($\pm y$)
- Perturbations are applied with randomized sign: $\text{sign}(y) \in \{+1.0, -1.0\}$.
- Tests directional invariance and confirms that policies do not harbor directional bias or asymmetrical control drift.

### 2.4 Impulse Duration
- Single-step impulse ($\Delta t = 1$ step, $50\text{ ms}$) vs two-step burst ($\Delta t = 2$ steps, $100\text{ ms}$).
- Varies the kinetic momentum transferred to the block prior to detection.

### 2.5 Initial Pose & Target Variability
- Small initial cube placement jitter ($y_0 \in [-0.010, +0.010]\text{ m}$) ensuring diverse approach angles.
- Varied target goal locations ($y_{\text{goal}} \in \{-0.01, 0.00, +0.01\}\text{ m}$).

---

## 3. Physical Realism & Zero-Teleportation Invariance

To guarantee scientific validity, the protocol enforces strict physical realism:
1. **Dynamic Generation:** All deviations arise through closed-loop manipulator-object contact forces governed by MuJoCo's Coulomb friction model ($\mu = 0.35$).
2. **No Object Teleportation:** At no point during failure generation is the object's position, velocity, or orientation overwritten or teleported.
3. **Smooth Actuator Dynamics:** Robot actions remain within standard torque/velocity limits ($\|u\|_\infty \le 0.02\text{ m/step}$).

---

## 4. Recoverability Assessment via Privileged Oracle

Every generated deviation state $s(t_d)$ is evaluated by the analytical Privileged Oracle Controller:
- **Kinematic Workspace Check:** Object position $x \in [0.05, 0.50]$, $y \in [-0.20, 0.20]$.
- **Dynamic Stability Check:** Cube pitch/roll $\le 0.15\text{ rad}$, object not falling off table.
- **Horizon Feasibility Check:** Remaining horizon $T - t_d \ge 25$ steps.
- **Empirical Demonstration:** Oracle controller executes from $s(t_d)$ and must reach goal with dwell time $\ge 5$ steps.

Only failures satisfying all four criteria are admitted as valid source scenarios for counterfactual paired generation.

---

## 5. Implementation Status

- **Sampling Configuration:** `configs/scenarios/paired_scenario_sampling.yaml` (`Verified`).
- **Methodology Documentation:** `docs/methodology/failure_diversity_plan.md` (`Verified`).
- **Generator Integration:** Operational in `src/causal_history_recovery/counterfactuals/paired_scenario_generator.py` (`Verified`).

