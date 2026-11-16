# Research Scope & Boundary Definitions

## 1. Scientific Domain
This project operates at the intersection of:
- **Robot Learning & Imitation Learning:** Closed-loop policy execution for robotic manipulation.
- **Robustness & Failure Recovery:** Behavior under off-nominal execution conditions and distribution shifts.
- **Causal Inference & Counterfactual Evaluation:** Controlled intervention on history variables while holding physical confounding states invariant.
- **Reproducible Benchmarking:** Precise statistical reporting, protocol formalization, and open-source validation artifacts.

---

## 2. In-Scope Technical Components

### 2.1 Causal Evaluation Protocol
- **Condition A (Natural Policy-Induced):** Natural execution deviations recorded from unperturbed rollouts where policy sub-optimality triggers a slip, collision, or grasp error.
- **Condition B (Prefix Replay):** Exact replay of the deterministic action prefix that produced the deviation in Condition A, transferring control to the evaluated policy at $t = t_d$.
- **Condition C (Matched-State Injection):** Deterministic simulator reset to a state $s_{\text{inj}}$ such that $d(s_{\text{inj}}, s_{\text{replay}}) \le \epsilon$, without executing the action prefix $a_{0:t_d-1}$.
- **Condition D (Observation History Masking):** Ablations varying the temporal observation window $k \in \{1, 2, 5, 10, \dots\}$.

### 2.2 Manipulation Tasks
- Supported manipulation regimes:
  1. Pick and Place (Free space motion + grasp stability)
  2. Block Pushing / Precision Insertion (Contact-rich friction dynamics)
  3. Drawer Opening / Closing (Articulated kinematics)
  4. Button Pressing / Switch Activation (Discrete state transition)

### 2.3 Policy Baselines
- **BC-Reactive:** Memoryless behavior cloning with Multi-Layer Perceptron (state) or Convolutional Neural Network (vision).
- **BC-History:** Temporal behavior cloning using observation frame-stacking or recurrent units (LSTM/GRU).
- **BC-Recovery:** Multi-task recovery-augmented policy trained on nominal demos plus recovery trajectories.
- **Privileged Oracle:** Kinematically feasible trajectory planner used to establish recoverability ground truth.

### 2.4 Metrics & Statistics
- Decomposed metrics: Detection AUROC/AUPRC, Diagnosis Accuracy, Recovery Success Rate (RSR), Final Task Completion.
- History Dependence: $H_R = R_{\text{replay}} - R_{\text{injected}}$, $H_R^{\text{abs}} = |R_{\text{replay}} - R_{\text{injected}}|$.
- Ranking stability: Kendall's $\tau$, Spearman's $\rho$.
- Statistical framework: Paired Wilcoxon signed-rank tests, 95% bootstrap confidence intervals, Holm-Bonferroni correction.

---

## 3. Explicit Out-of-Scope Elements

1. **Hardware Sim-to-Real Deployment in Phase 0:**
   - Physical hardware robot deployment is out of scope for the initial protocol validation. All experiments are conducted within validated physics simulation (MuJoCo).
2. **Universal Causal Claims:**
   - We do not make claims regarding universal physical causality in unconstrained open-world environments. The scope is strictly bounded to the simulation intervention protocol.
3. **Novel Policy Architecture Design as Primary Contribution:**
   - The primary contribution of this research is the **evaluation protocol and empirical validity audit**, not the introduction of a new proprietary neural architecture.
4. **Ad-Hoc Unbounded Perturbations:**
   - Random noise injection without physical grounding or recoverability filtering is strictly out of scope.
5. **Image-Only State Matching:**
   - Visual pixel similarity without underlying kinematic and dynamic state matching is excluded.
6. **MIND-Contact / MIND-Contact++ Integration:**
   - Strictly forbidden. No dependencies, nomenclature, or unvalidated code from past projects.

