# Methodology Summary: Causal-History Dependence in Robot Policy Recovery

> **Source Document:** `Causal_History_Methodology_Merged.pdf` (Pages 1–29)  
> **Document Status:** Comprehensive Audit & Extraction Complete  
> **Scientific Integrity:** Faithfully extracted without alteration of scientific meaning.

---

## 1. Research Problem
Current evaluations of robot manipulation policies typically assess performance either from clean, unperturbed initial states, from statically perturbed initial scenes, from replayed execution deviations, or after external runtime interventions. However, these paradigms uniformly assume that recovery difficulty is a function of the instantaneous physical state alone:
$$\text{failure state } s \longrightarrow \text{recovery performance } R$$
They do not isolate whether recovery capability is contingent on the **causal execution history** that produced the failure state:
$$\text{causal history } h \longrightarrow \text{matched failure state } s \longrightarrow \text{recovery performance } R$$
A policy may recover successfully from a directly injected physical state disruption (e.g. object displacement) but fail completely when it induces that identical displacement through its own erroneous actions, or vice versa, because observation and action histories carry implicit failure signals, momentum, and causal context.

---

## 2. Primary Research Question
> **When physically equivalent robot failure states are reached through different execution histories, do robot policies show different detection, diagnosis, recovery, and final task-completion performance?**

Formally investigating the non-equivalence:
$$\text{same recovery state } \not\Rightarrow \text{same recovery capability}$$

---

## 3. Secondary Research Questions
1. Does a policy that performs well on externally injected failures also recover well from its own action-induced failures?
2. Does replaying the original action prefix change recovery outcomes compared with direct physical state injection?
3. Does observation history improve recovery when current physical states are matched?
4. Are deviation detection, failure diagnosis, corrective action selection, and final task completion affected differently by causal history?
5. Do existing recovery benchmarks produce the same policy rankings as causal-history evaluation?
6. Does recovery-augmented training reduce causal-history dependence?
7. Does causal-history dependence persist under visual observation and sensor noise?
8. Does the finding generalize across tasks, policies, random seeds, and simulation engines?

---

## 4. Main Hypothesis
- **H1: Causal-History Dependence**
  - **Null Hypothesis ($H_0$):** $R_{\text{replay}} = R_{\text{injected}}$ (Recovery success rate is invariant to whether the failure was reached via prefix replay or direct matched-state injection).
  - **Alternative Hypothesis ($H_1$):** $R_{\text{replay}} \neq R_{\text{injected}}$ (Recovery success rate differs significantly between replay and injection even when physical states are matched within tolerance $\epsilon$).

---

## 5. Secondary Hypotheses
- **H2: Benchmark Ranking Validity**
  - **Null Hypothesis ($H_0$):** Policy rankings are equivalent across standard initial-state task success, existing recovery benchmarks, and causal-history matched-state evaluation ($\tau = 1, \rho = 1$).
  - **Alternative Hypothesis ($H_1$):** Policy rankings differ significantly across evaluation protocols (ranking reversals occur).
- **H3: Temporal Information Effect**
  - **Null Hypothesis ($H_0$):** $R_{\text{current-only}} = R_{\text{history-aware}}$ under matched-state conditions.
  - **Alternative Hypothesis ($H_1$):** $R_{\text{current-only}} \neq R_{\text{history-aware}}$ (Temporal memory significantly alters recovery success).
- **H4: Recovery-Training Effect**
  - **Null Hypothesis ($H_0$):** $H_R^{\text{standard}} = H_R^{\text{recovery-trained}}$ (Recovery training does not alter the history dependence metric $H_R$).
  - **Alternative Hypothesis ($H_1$):** $H_R^{\text{standard}} \neq H_R^{\text{recovery-trained}}$ (Recovery training significantly modulates history dependence).
- **H5: Cross-Task Consistency**
  - **Null Hypothesis ($H_0$):** Causal-history dependence magnitude $H_R$ is uniform across manipulation task families.
  - **Alternative Hypothesis ($H_1$):** Causal-history dependence varies systematically with task type, contact dynamics, or degree of underactuation.

---

## 6. Research Objectives
- **Objective 1:** Build a reproducible causal-history evaluation protocol creating natural policy-induced deviations, prefix-replay episodes, and matched-state injection episodes.
- **Objective 2:** Define physical state equivalence using a multi-component weighted distance metric and rigorous rejection rules.
- **Objective 3:** Decompose recovery capability into deviation detection, failure diagnosis, corrective action selection, physical recovery, and final task completion.
- **Objective 4:** Directly compare the proposed protocol against standard task success, LIBERO-Recover-compatible, RoboRecover-compatible, and LIBERO-Pro2.0-compatible evaluations.
- **Objective 5:** Statistically test causal-history dependence ($H_R$) across diverse policies and tasks.
- **Objective 6:** Release an open-source, fully reproducible benchmark suite and reproducibility package.

---

## 7. Proposed Contribution & Novelty Position
- **What this work is NOT:**
  - Not merely "another robot recovery benchmark" with more perturbation types.
  - Not a claim of introducing the first recovery dataset (RoboRecover and LIBERO-Recover already exist).
  - Not a claim of universal real-world causality from simulation.
- **What this work IS:**
  - A **causal-history validity audit** for robot policy recovery evaluation.
  - A rigorous counterfactual protocol:
    $$\text{same physical state } + \text{different causal history } \longrightarrow \text{compare recovery performance}$$
  - A definitive test of whether conventional benchmark scores hide critical history-dependent vulnerabilities or overstate recovery resilience.

---

## 8. Formal Definitions

### 8.1 Robot Policies
- **Reactive Policy:** $a_t = \pi(o_t)$
- **History-Aware Policy:** $a_t = \pi(o_{0:t}, a_{0:t-1})$

### 8.2 State Transitions
- **Nominal Transition:** $s_{t+1} = T(s_t, a_t)$
- **Execution Deviation Transition:** $s_{t+1} = T_{\delta}(s_t, a_t)$, capturing anomalous physical events (slips, collisions, jams, partial grasps).

### 8.3 Recovery & Success
- **Recovery Policy:** For time $t \ge t_d$ (deviation time), actions are produced by $\pi$ attempting to reach original goal $g$.
- **Recovery Success ($R$):**
  $$R = \mathbb{1}[\text{original task completed after deviation}]$$
- **Recovery Success Rate (RSR):**
  $$\text{RSR} = \frac{\sum \text{episodes completing original task after deviation}}{\sum \text{valid recoverable episodes}}$$
  *(Physically unrecoverable episodes are strictly excluded from the denominator via feasibility/oracle filtering).*

### 8.4 Detection & Diagnosis
- **Detection ($D$):** Binary indicator $\mathbb{1}[\text{policy recognizes abnormal execution}]$, occurring at $t_{\text{detection}}$.
- **Detection Delay ($D_{\text{delay}}$):** $t_{\text{detection}} - t_{\text{deviation}}$.
- **Diagnosis ($Z$):** Categorical prediction of failure class $Z \in \{\text{slip}, \text{collision}, \text{partial grasp}, \text{overshoot}, \text{occlusion}, \text{insertion failure}\}$.

### 8.5 Recovery Probability Decomposition
$$P(F) = P(D) \cdot P(Z \mid D) \cdot P(C \mid Z, D) \cdot P(P \mid C, Z, D) \cdot P(F \mid P, C, Z, D)$$
where $D$ is detection, $Z$ is diagnosis, $C$ is corrective action selection, $P$ is physical recovery, and $F$ is final task completion.

---

## 9. Evaluation Conditions
1. **Condition A: Natural Policy-Induced Failure**
   - Policy executes closed-loop; its own action errors naturally lead to a physical deviation. Closest to natural execution failure.
2. **Condition B: Prefix-Replay Failure**
   - Exact initial state and recorded action prefix $a_{0:t_d-1}$ are replayed in the simulator. At $t_d$, control transfers to the evaluated policy. Preserves exact causal trajectory and action history.
3. **Condition C: Matched-State Injection**
   - The simulator is reset directly to a physical state matched ($d(s_1, s_2) \le \epsilon$) to the state from Condition B, but without executing the action prefix. Isolates physical state from causal history.
4. **Condition D: Observation-History Masking (Ablation)**
   - Policy is evaluated from the recovery state under controlled observation history windows: current observation only ($k=1$), short history ($k=2, 5$), full history, history with failure obscured, or history with failure labeled.

---

## 10. State-Matching Procedure

### 10.1 Physical State Representation
$$s = [q, \dot{q}, p_{ee}, R_{ee}, p_{obj}, R_{obj}, v_{obj}, \omega_{obj}, c, g, m]$$
where $q, \dot{q}$ are joint coordinates and velocities; $p_{ee}, R_{ee}$ are end-effector pose; $p_{obj}, R_{obj}, v_{obj}, \omega_{obj}$ are object 6D pose and spatial velocities; $c$ is discrete contact state / contact manifold; $g$ is task goal; $m$ is gripper/actuator mode.

### 10.2 Weighted Physical Distance
$$d(s_1, s_2) = w_q \|q_1 - q_2\|_2 + w_{\dot{q}} \|\dot{q}_1 - \dot{q}_2\|_2 + w_p \|p_{ee,1} - p_{ee,2}\|_2 + w_R d_R(R_1, R_2) + w_v \|v_{obj,1} - v_{obj,2}\|_2 + w_c \mathbb{1}[c_1 \neq c_2] + w_g \|g_1 - g_2\|_2$$
A pair is accepted if and only if $d(s_1, s_2) \le \epsilon$.

### 10.3 Tolerance Tiers for Sensitivity Analysis
- **Strict ($\epsilon_1$):** Joint tolerance $< 0.01$ rad, position $< 2$ mm, object position $< 2$ mm, velocity $< 0.01$ m/s, exact contact match.
- **Moderate ($\epsilon_2$):** Joint tolerance $< 0.03$ rad, position $< 5$ mm, object position $< 5$ mm, velocity $< 0.05$ m/s, exact contact match.
- **Loose ($\epsilon_3$):** Joint tolerance $< 0.08$ rad, position $< 15$ mm, object position $< 15$ mm.

### 10.4 Multimodal Validation
- Visual validation (camera pose, lighting, background, depth map) is tracked and controlled separately. Pixel matching alone is explicitly rejected as insufficient for physical dynamics.

---

## 11. Required Policy Conditions & Baselines
- **Baseline 1: Reactive Behavior Cloning (BC-Reactive)**
  - Input: Current observation $o_t$ only (state MLP or vision CNN).
- **Baseline 2: History-Aware Behavior Cloning (BC-History)**
  - Input: Stacked observation history $[o_{t-k:t}]$ or recurrent LSTM/GRU network. Tests whether temporal memory mitigates or introduces history dependence.
- **Baseline 3: Recovery-Augmented Policy (BC-Recovery)**
  - Trained on nominal demonstrations augmented with recovery corrections and off-nominal trajectories.
- **Baseline 4: Scripted / Privileged Oracle Controller**
  - Serves as the feasibility upper bound to establish the recoverability filter ($R_{\text{oracle}} = 1$).

---

## 12. Required Baseline Benchmark Comparisons
1. Standard nominal task-success evaluation (initial clean state).
2. Initial-state perturbation evaluation (static scene shifts).
3. LIBERO-Recover-compatible recovery evaluation.
4. RoboRecover-compatible replay evaluation.
5. LIBERO-Pro2.0-compatible runtime intervention evaluation.
6. Proposed matched-state causal-history protocol.

---

## 13. Required Metrics

### 13.1 Detection Metrics
- Detection Accuracy, AUROC, AUPRC, False Positive Rate (FPR), False Negative Rate (FNR).
- Detection Delay: $D_{\text{delay}} = t_{\text{detection}} - t_{\text{deviation}}$.
- Brier Score & Expected Calibration Error (ECE) for policy failure confidence.

### 13.2 Diagnosis Metrics
- Failure-type Classification Accuracy, Macro-F1 score, Confusion Matrix, Contact-mode accuracy.

### 13.3 Recovery & Performance Metrics
- Recovery Success Rate (RSR), Original Task Completion after Recovery, Time to First Corrective Action, Additional Path Length, Action Smoothness, Collision Count during recovery, Constraint Violations.
- Recovery Cost: $C_{\text{recovery}} = \lambda_1 T_{\text{add}} + \lambda_2 L_{\text{add}} + \lambda_3 N_{\text{actions}} + \lambda_4 N_{\text{collisions}}$.

### 13.4 Causal History Dependence Metrics
- **Signed Dependence:** $H_R = R_{\text{replay}} - R_{\text{injected}}$
- **Absolute Dependence:** $H_R^{\text{abs}} = |R_{\text{replay}} - R_{\text{injected}}|$
  - $H_R \approx 0$: Recovery is invariant to causal history.
  - $H_R > 0$: Causal history facilitates recovery.
  - $H_R < 0$: Causal history impedes recovery (e.g., hysteresis, momentum, persistent bias).

### 13.5 Policy Ranking Stability
- Kendall's rank correlation coefficient $\tau$ and Spearman's rank correlation $\rho$ between rankings under conventional benchmarks vs. causal-history evaluation.
- Pairwise ranking reversal frequency and Top-1 agreement.

---

## 14. Statistical Methodology (Provisional — Subject to Pilot Calibration)
> *Note: All seed counts, episode budgets, and statistical tests specified below are provisional guidelines. Final sample sizes and test selections will be formally calibrated in Phase 7 based on pilot variance, matching yield rate ($\eta_{\text{match}}$), and oracle recoverability ($\eta_{\text{recoverable}}$) as detailed in `docs/statistics/provisional_analysis_plan.md`.*

- **Random Seeds (Provisional):** Minimum 3 seeds for initial pilots; 5 seeds targeted for main policy comparisons if computationally feasible and warranted by power calculations.
- **Sample Size (Provisional):** 50–100 episodes per task and condition target, to be validated via power analysis on pilot variance.
- **Uncertainty Quantification:** 95% bootstrap confidence intervals for all success and recovery rates.
- **Paired Hypothesis Tests:** Wilcoxon signed-rank test on matched episode pairs (or McNemar's test if strictly binary paired outcomes without continuous metrics).
- **Multiple Comparison Correction:** Holm-Bonferroni step-down correction for family-wise error rate control.
- **Effect Sizes:** Cliff's delta (non-parametric ordinal), Cohen's $d$, and odds ratios.
- **Mixed-Effects Regression:** Linear/logistic mixed-effects modeling with condition, policy, and task as fixed effects, and scenario ID as a random effect (contingent on sufficient matched pairs and non-singular covariance fits):
  $$y_{ijk} = \beta_0 + \beta_1 \text{Cond}_i + \beta_2 \text{Policy}_j + \beta_3 \text{Task}_k + \beta_4 (\text{Cond}_i \times \text{Policy}_j) + u_{\text{scenario}} + \epsilon$$

---

## 15. Ablation Studies
1. **History Length Ablation:** $k \in \{1, 2, 5, 10, 20, \text{full}\}$.
2. **Recovery Training Ablation:** Nominal only vs. single failure mode vs. multi-failure augmentation.
3. **State-Matching Tolerance Ablation:** Strict ($\epsilon_1$) vs. moderate ($\epsilon_2$) vs. loose ($\epsilon_3$).
4. **Observation Modality Ablation:** Low-dimensional state vs. proprioception-only vs. RGB vision vs. RGB-D.
5. **Dynamics Randomization Ablation:** Deterministic vs. moderate friction/mass jitter vs. strong randomization.
6. **Scenario Source Ablation:** Policy-rollout mined vs. empirically bounded perturbations.

---

## 16. Reproducibility Requirements
- Complete release of:
  - Source code with documented execution CLI and modular packages.
  - Environment specifications (`requirements.txt`, `environment.yml`, Dockerfile).
  - Pinned seeds and exact configuration files (`configs/`).
  - Raw trajectory data, action prefixes, matched states, and metadata manifests.
  - Trained policy checkpoints and training logs.
  - Automated smoke test (`scripts/check_environment.py` and `tests/`).
  - Standardized per-episode logging schema.

---

## 17. Expected Deliverables
1. **Deliverable 1: Formal Protocol Document** (Definitions, conditions, mathematical criteria).
2. **Deliverable 2: Scenario-Generation Toolkit** (Mining, replay, injection, validation).
3. **Deliverable 3: Recovery Scenario Dataset** (Metadata, prefixes, states, recoverability labels).
4. **Deliverable 4: Baseline Policy Implementations** (Reactive, History-aware, Recovery-augmented, Oracle).
5. **Deliverable 5: Evaluation Suite** (Full metrics engine, ranking stability, calibration).
6. **Deliverable 6: Reproducibility Package** (Docker, environment, seeds, logs, smoke test).
7. **Deliverable 7: Manuscript & Supplementary Material** (Targeting Q1 robotics journal).

---

## 18. Limitations to Acknowledge
- Simulation-based study (MuJoCo/PyBullet); physical real-robot dynamics (backlash, compliance, tactile sensor degradation) are not fully captured.
- Finite state-matching tolerance ($\epsilon > 0$).
- Visual observations may incompletely reflect internal physical configurations.
- Policy-mined deviations reflect specific policy architecture weaknesses.
- Some recovery trajectories may require privileged state information not available to standard policies.

---

## 19. Project Timeline
- **Weeks 1–2:** Literature and code audit; research question freeze.
- **Weeks 3–4:** Simulator infrastructure, deterministic reset, serialization, replay verification.
- **Weeks 5–6:** Policy baseline training, nominal success validation.
- **Weeks 7–8:** Failure mining, deviation labeling, oracle recoverability filtering.
- **Weeks 9–10:** State-matching implementation, injection generation, tolerance calibration.
- **Weeks 11–12:** Main experimental evaluation across Conditions A, B, C.
- **Weeks 13–14:** Ablations, sensitivity analysis, statistical testing.
- **Weeks 15–16:** Manuscript authoring, figures, tables, code packaging, internal review.

---

## 20. Go / No-Go Decision Criteria
- **Mandatory Literature Audit Check:** Inspect RoboRecover, LIBERO-Recover, and LIBERO-Pro2.0 in detail. Proceed with causal-history evaluation **only if** they do not already evaluate matched physical state counterfactual injection without replay ($R_{\text{replay}}$ vs. $R_{\text{injected}}$) and decomposed metrics.
- **Outcome Status:**
  - Audit Confirmed: RoboRecover strictly evaluates replayed action prefixes (Condition B) and does not perform matched-state counterfactual injection without history (Condition C), nor does it evaluate $H_R$ or rank-stability across causal conditions.
  - **Decision:** **GO** — Proceed with the unique causal-history validity audit.

