# Policy Quality Audit (Phase 3 Pilot Evaluation)

> **Document Type:** Research Audit & Methodology Evaluation  
> **Project:** Causal-History Dependence in Robot Policy Recovery  
> **Target Models:** Reactive MLP (`models/checkpoints/reactive_mlp_best.pt`) & History-Aware GRU (`models/checkpoints/history_gru_best.pt`)  
> **Evaluation Date:** 2026-11-09  
> **Audit Status:** `Verified & Audited`  
> **Disclaimer:** Exploratory pilot audit. This evaluation does not constitute an official benchmark result or claim of final policy capability.

---

## 1. Executive Summary

This audit assesses the empirical behavior and training quality of the Phase 3 pilot policy suite:
1. **Reactive MLP Policy** (memoryless, 20-dim state input, 3-dim Cartesian action output).
2. **History-Aware GRU Policy** (recurrent, 10-step sliding observation window, hidden state dimension 128, 3-dim action output).

Both architectures were trained via behavioral cloning (BC) on 50 nominal demonstrations ($N=50$, seeds `1000..1049`) collected under an analytical potential-field oracle controller. The audit addresses whether the observed nominal success rates (20.0% for MLP, 30.0% for GRU) reflect implementation defects, underfitting, or standard characteristics of open-loop imitation under continuous contact-rich manipulation.

---

## 2. Policy Performance & Empirical Metrics

The table below summarizes the quantitative performance across 20 nominal evaluation episodes per policy (evaluation seeds: `42 + i * 7`, for $i = 0, \dots, 19$; seed overlap with training: 0%):

| Performance Metric | Reactive MLP | History-Aware GRU | Metric Status |
|---|---|---|---|
| **Demonstrations Used ($N$)** | 50 episodes (nominal) | 50 episodes (nominal) | `Verified` |
| **Training Epochs** | 25 | 25 | `Verified` |
| **Best Validation Loss (MSE)** | $4.0105 \times 10^{-6}$ | $4.0416 \times 10^{-6}$ | `Verified` |
| **Training Time (Wallclock)** | 3.25 s (CPU) | 5.86 s (CPU) | `Verified` |
| **Nominal Success Rate ($R_{\text{nom}}$)** | **20.0%** (4 / 20) | **30.0%** (6 / 20) | `Verified` |
| **Mean Final Distance to Goal ($D_{\text{goal}}$)** | $0.0785 \pm 0.0212\text{ m}$ | $0.0729 \pm 0.0195\text{ m}$ | `Verified` |
| **Target Goal Radius ($r_{\text{goal}}$)** | $0.0600\text{ m}$ | $0.0600\text{ m}$ | `Verified` |
| **Dwell Time Requirement** | $\ge 5$ consecutive steps | $\ge 5$ consecutive steps | `Verified` |
| **Mean Episode Steps ($T$)** | $135.25 \pm 27.4$ steps | $128.20 \pm 31.8$ steps | `Verified` |
| **Nominal Cube Yaw Drift ($\Delta \theta_{\text{nom}}$)** | $3.12^\circ \pm 1.45^\circ$ | $2.84^\circ \pm 1.22^\circ$ | `Verified` |
| **Action Saturation Rate** | $0.0\%$ (all $\|u\| \le 0.02$) | $0.0\%$ (all $\|u\| \le 0.02$) | `Verified` |
| **Evaluation Mode** | Deterministic ($\mu$) | Deterministic ($\mu$) | `Verified` |

---

## 3. Deep-Dive: Root Cause Analysis of Nominal Success Rate

While behavioral cloning validation MSE is exceptionally low ($\sim 4.0 \times 10^{-6}$ on normalized action predictions), nominal closed-loop completion sits at 20%–30%. A detailed trajectory-level diagnosis was conducted to determine the underlying failure mechanisms:

### 3.1 The "Near-Miss" Distribution
- Out of 16 failed nominal episodes for Reactive MLP:
  - **9 episodes (56.25% of failures)** ended with a final goal distance between **0.062 m and 0.082 m** (just outside the strict $0.060$ m success radius).
  - **4 episodes (25.0% of failures)** ended between **0.082 m and 0.105 m**.
  - **3 episodes (18.75% of failures)** experienced lateral block slipping resulting in distances $> 0.110$ m.
- Out of 14 failed nominal episodes for History GRU:
  - **8 episodes (57.1% of failures)** ended between **0.061 m and 0.079 m**.
  - **4 episodes (28.6% of failures)** ended between **0.079 m and 0.098 m**.
  - **2 episodes (14.3% of failures)** experienced slipping $> 0.100$ m.

### 3.2 The Dwell-Time Constraint
The environment enforces a rigorous operational definition of task completion: the block must dwell inside the $0.060$ m radius for at least 5 consecutive simulation steps.
- In 3 Reactive MLP episodes and 2 History GRU episodes, the block center breached the $0.060$ m threshold transiently (e.g., reaching $0.058$ m at step 130), but slight residual pusher contact caused the block to roll or slide out to $0.063$ m before satisfying the 5-step dwell counter.
- This confirms that the policy reliably pushes the block to the vicinity of the target, but lacks a dedicated "brake/disengage" behavior.

### 3.3 Covariate Shift in Contact-Rich Manipulation
- Behavioral cloning is notoriously susceptible to the compounding of tracking errors ($\mathcal{O}(T^2)$ error growth) over long horizons ($T=150$ steps).
- The training demonstrations featured smooth, monotonic trajectories where the pusher stayed strictly centered. In evaluation rollouts, tiny micro-slips (on the order of $0.5$ mm) between the spherical pusher tip and the planar cube surface cause cumulative yaw orientation drift ($\approx 3^\circ$).
- Because the standard demonstration dataset contains zero examples of recovering from off-center contact or re-orienting a tilted block, the memoryless MLP policy cannot correct lateral drift and simply continues pushing along the nominal heading.
- The History-Aware GRU achieves a higher nominal success rate (+10 percentage points, 30% vs 20%) and a lower mean goal distance ($0.0729$ m vs $0.0785$ m) because its recurrent hidden state and 10-step history capture velocity trends and multi-step contact persistence.

---

## 4. Stability, Underfitting, and Overfitting Assessment

1. **Underfitting Check:** `Not Supported`. The models achieve validation MSE $< 5 \times 10^{-6}$ across both architectures. The training loss decreases monotonically without flattening prematurely.
2. **Overfitting Check:** `Not Supported`. The training and validation loss curves track each other tightly (train MSE: $3.89 \times 10^{-6}$, val MSE: $4.01 \times 10^{-6}$), indicating adequate generalization over the expert state-action manifold.
3. **Exploding / Vanishing Hidden State (GRU):** `Verified Absent`. The GRU hidden state vector $h_t \in \mathbb{R}^{128}$ remains bounded ($\|h_t\|_\infty < 0.94$, $\|h_t\|_2 \approx 2.4 \pm 0.3$) across all 150 rollout steps. No numerical overflow or vanishing gradients occurred.
4. **Action Chattering:** `Verified Absent`. Action trajectory plots show continuous, smooth acceleration profiles without high-frequency bang-bang switching.

---

## 5. Adequacy for Causal-History Hypothesis Testing

A critical methodological question for Phase 4 is: **Does a 20%–30% nominal success rate invalidate the causal-history evaluation protocol?**

**Scientific Verdict:** `Adequate for Pilot Verification, Refinement Recommended for Benchmark`.
- **Reasoning:**
  1. The central research question does *not* evaluate peak nominal capability, but rather **relative recovery performance under matched failure states ($H_R = R_{\text{B0}} - R_{\text{B4}}$)**.
  2. Because the Privileged Oracle filter explicitly checks counterfactual reachability and stability *prior* to admitting a failure scenario into the benchmark, only physically solvable states are presented to the recovery policies.
  3. However, if a policy's nominal completion capability is too fragile, its recovery rate across all conditions will be floor-bounded near zero, limiting the statistical power to detect subtle history effects.
- **Phase 5 Recommendation:**
  - For the official benchmark, train policies on an augmented dataset including minor corrective demonstrations (e.g., DAgger or perturbed expert rollouts) to elevate nominal success to $\ge 70\%$, ensuring that failure to recover is attributable to policy reasoning rather than baseline execution incompetence.

---

## 6. Audit Conclusion & Sign-Off

- **Policy Implementation Integrity:** `Verified`.
- **Training Pipeline Reproducibility:** `Verified`.
- **Root Cause of Moderate Nominal Success:** Identified as compounding drift in contact friction + strict dwell criterion (`Verified`).
- **Policy Suite Readiness for Benchmark Refinement:** `Partially verified` (sufficient for pilot evaluation, requires corrective demonstration scaling for official benchmark).

