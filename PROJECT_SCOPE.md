# Project Scope & Scientific Boundaries

## 1. Project Overview & Working Identity
- **Working Project Name:** `causal-history-recovery`
- **Working Paper Title:** *Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures*
- **Primary Scientific Problem:** Whether recovery performance in robot manipulation policies is determined solely by the instantaneous physical state or whether it is fundamentally contingent on the causal execution history that led to that failure state.

---

## 2. In-Scope Scientific Questions & Capabilities

1. **Matched-State Causal-History Protocol:**
   - Defining and evaluating four rigorous conditions:
     - **Condition A (Natural Policy-Induced Failure):** Spontaneous execution deviation from normal policy control.
     - **Condition B (Prefix-Replay Failure):** Exact replay of the initial state and action prefix leading to the deviation point.
     - **Condition C (Matched-State Injection):** Exact physical state restoration without replaying the preceding action prefix.
     - **Condition D (Observation-History Masking / Ablation):** Explicitly controlling temporal context ($k=1, 2, 5, 10, \dots, \text{all}$).
2. **Physical State Matching:**
   - Rigorous distance metric $d(s_1, s_2)$ defined over generalized coordinates $q$, velocities $\dot{q}$, end-effector pose $p_{ee}, R_{ee}$, object 6D poses $p_{obj}, R_{obj}$, object velocities $v_{obj}, \omega_{obj}$, discrete contact graph $c$, and goal $g$.
   - Multi-threshold sensitivity analysis (strict $\epsilon_1$, moderate $\epsilon_2$, loose $\epsilon_3$).
3. **Decomposed Recovery Metrics:**
   - Formal probabilistic decomposition:
     $$P(F) = P(D) \cdot P(Z \mid D) \cdot P(C \mid Z, D) \cdot P(P \mid C, Z, D) \cdot P(F \mid P, C, Z, D)$$
     where $D$ is deviation detection, $Z$ is failure diagnosis, $C$ is corrective action selection, $P$ is physical recovery, and $F$ is final task completion.
   - History dependence metrics: $H_R = R_{\text{replay}} - R_{\text{injected}}$ and $H_R^{\text{abs}} = |R_{\text{replay}} - R_{\text{injected}}|$.
   - Policy-ranking stability across protocols (Kendall's $\tau$, Spearman's $\rho$, ranking reversals).
4. **Targeted Policy Classes:**
   - Reactive policy baselines (state MLP, image CNN).
   - History-aware policy baselines (temporal stacking, LSTM/GRU/Transformer).
   - Recovery-augmented policy baselines (trained on failure/correction data).
   - Privileged oracle / scripted controller (for recoverability filtering).
5. **Statistical Rigor:**
   - Multi-seed runs (minimum 3 seeds for pilots, 5 seeds for main benchmarks).
   - Paired Wilcoxon signed-rank tests across identical matched failure scenarios.
   - Bootstrap 95% confidence intervals and Holm-Bonferroni correction for multiple hypothesis testing.

---

## 3. Explicit Out-of-Scope Boundaries (What We Do NOT Do)

1. **No Claims of Universal Real-World Causality:**
   - The causal claims are bounded strictly to the defined simulator intervention and matching protocol. We do not claim universal metaphysical causality in open-world physical systems.
2. **No Hardware Validity Claims Without Hardware Experiments:**
   - Initial conclusions are strictly simulation-based (MuJoCo). Sim-to-real gap, tactile sensor differences, and actuator backlash are acknowledged as limitations.
3. **Not "Another Recovery Benchmark":**
   - The goal is **not** to produce simply another large dataset of perturbed trajectories (which RoboRecover and LIBERO-Recover already do). The goal is a **causal-history validity audit** that determines whether state-based recovery benchmarks mischaracterize policy capability.
4. **No Merging with MIND-Contact or MIND-Contact++:**
   - This project is completely distinct. No code, data, or experimental logs from MIND-Contact are assumed or imported without independent justification, documentation, and testing.
5. **No Visual-Only Matching:**
   - State matching will never rely on image pixel similarity alone. Physical states must match in full configuration space.

---

## 4. Q1 Target Deliverables

1. Formal causal-history protocol specification document.
2. Scenario generation and state-matching toolkit with deterministic MuJoCo serialization.
3. Open-source benchmark suite with unit tests and smoke tests.
4. Statistical results evaluating $H1$ through $H5$.
5. LaTeX manuscript ready for submission to a leading robotics journal (e.g., IEEE Transactions on Robotics [T-RO], Autonomous Robots [AURO], or Robotics and Autonomous Systems [RAS]).

