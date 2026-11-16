# Minimum Viable Benchmark Design Specification (Phase 5/6)

> **Document Type:** Research Methodology & Benchmark Protocol Specification  
> **Project:** Causal-History Dependence in Robot Policy Recovery  
> **Design Status:** `Planned & Specified`  
> **Evaluation Date:** 2026-11-09  
> **Governance:** Pre-Experiment Design Freeze. Requires explicit user approval prior to execution.

---

## 1. Executive Summary & Scientific Purpose

The purpose of the **Minimum Viable Benchmark (MVB)** is to execute the first statistically powered, counterfactually controlled empirical evaluation of causal-history dependence in robot policy recovery.

Unlike existing recovery benchmarks (e.g., RoboRecover, LIBERO-Recover) that evaluate policies either in unperturbed rollouts or under open-loop restarts without physical state matching, this benchmark:
1. Enforces **exact physical state matching** ($D \le 1.0 \times 10^{-6}$) between natural recovery and counterfactual recovery.
2. Filters failure states via an **analytical Privileged Oracle** to guarantee physical recoverability.
3. Provides sufficient statistical sample size ($N \ge 100$ matched pairs per policy) to detect medium effect sizes ($\Delta = 0.15$) with $> 80\%$ power at $\alpha = 0.05$.
4. Measures whether **policy rankings invert** when memory is eliminated, identifying architectural vulnerabilities.

---

## 2. Benchmark Scale and Seed Allocation

| Benchmark Parameter | Specification | Scientific Rationale |
|---|---|---|
| **Simulation Environment** | `planned_custom_push_target_env` | Contact-rich, 6-DoF free-joint cube, Coulomb friction ($\mu=0.35$), 150-step horizon |
| **Demonstration Dataset** | 100 expert demonstrations (seeds `1000..1099`) | Scaled expert demonstrations with corrective recovery samples |
| **Evaluation Seeds** | 50 unique seeds (`seed_start: 2000`, step 7) | Non-overlapping with training, guarantees distributional diversity |
| **Candidate Failure Rollouts** | 600 rollouts per policy architecture | At 20% oracle yield, guarantees $N \ge 120$ admitted recoverable pairs |
| **Admitted Matched Scenarios** | $N = 100 - 120$ per policy | Meets Connor (1987) McNemar sample size requirement for $\Delta \ge 0.15$ |
| **Counterfactual Conditions Evaluated** | 4 primary conditions: B0, B1, B2, B4 | Tests continuation, prefix replay, memory reset, and matched injection |
| **Total Evaluation Rollouts per Policy** | $\approx 1,000$ rollouts ($600$ dev + $4 \times 100$ counterfactual) | Total simulation time $\approx 150,000$ steps ($\approx 75$ seconds CPU) |

---

## 3. Policy Architecture Suite

The benchmark incorporates four distinct policy archetypes spanning the memory spectrum:

1. **Reactive MLP Policy (Memoryless Baseline):**
   - Architecture: Linear(20, 128) $\to$ ReLU $\to$ Linear(128, 128) $\to$ ReLU $\to$ Linear(128, 3).
   - Memory capacity: $k = 0$. Markovian positive control.
2. **History-Aware GRU Policy (Recurrent Baseline):**
   - Architecture: Linear(20, 64) $\to$ GRU(64, 128) $\to$ Linear(128, 64) $\to$ Linear(64, 3).
   - Memory capacity: Continuous recurrent hidden state $h_t \in \mathbb{R}^{128}$ + 10-step observation window.
3. **Causal Temporal Transformer Policy (Attention-Based Memory):**
   - Architecture: Causal self-attention over sequence length $k=20$, positional encoding, feedforward head.
   - Memory capacity: Discrete attention across the preceding 20 steps of observations and actions.
4. **Privileged Oracle Controller (Upper-Bound Reference):**
   - Analytical potential-field feedback controller with direct access to full simulator state, frictionless virtual path planning, and contact re-alignment.

---

## 4. Failure Intervention Suite

To evaluate policy generalization across physical failure archetypes, the benchmark introduces three distinct perturbation mechanisms:

| Perturbation Class | Physical Mechanism | Parameters | Real-World Analog |
|---|---|---|---|
| **Class 1: Lateral Contact Slip** | Lateral displacement of pusher end-effector during steady push | $\Delta y \in [0.008, 0.016]\text{ m}$ at $t=25$ | Object slipping on uneven friction or gripper misalignment |
| **Class 2: Table Friction Spike (Jam/Stall)** | Transient Coulomb friction increase under block facet | $\mu \gets 0.85$ for $\Delta t = 10$ steps | Surface irregularity, sticky patch, or mechanical jamming |
| **Class 3: External Impulse Disturbance** | Lateral force pulse applied to cube center of mass | $F_y = 15.0\text{ N}$ for $\Delta t = 5$ steps | External bump, collision, or human intervention |

---

## 5. Counterfactual Condition Evaluation Protocol

For each admitted failure scenario $i$ occurring at step $t_d$ with physical snapshot $s(t_d)$:

1. **Condition B0 (Continuation):** Uninterrupted rollout from $t_d$ to $T$. Action prefix $a_{0:t_d-1}$ preserved, observation buffer intact, policy hidden state $h(t_d)$ intact.
2. **Condition B1 (Replayed Prefix):** Environment reset to $t_0$. Recorded action prefix $a_{0:t_d-1}$ replayed open-loop to reach $t_d$. Policy evaluates from $t_d$ onward. Tests trajectory-prefix sensitivity.
3. **Condition B2 (Policy Memory Reset):** Environment continues from $t_d$ with physical history intact, but policy recurrent hidden state is zeroed ($h_0 \gets \mathbf{0}$) and observation queue cleared. Isolates internal policy memory.
4. **Condition B4 (Direct Matched Injection):** Environment initialized at $t_0$, state vector $s(t_d)$ injected bitwise losslessly. History queue is empty, policy hidden state $h_0 \gets \mathbf{0}$. Isolates physical state from causal history.

---

## 6. Primary Evaluation Metrics & Verification Protocol

1. **Recovery Success Rate ($R_{\text{cond}}$):** Binary task completion satisfying $\ge 5$ consecutive steps dwell inside $r_{\text{goal}} = 0.060\text{ m}$.
2. **Causal History Recovery Effect ($H_R$):**
   $$H_R(\pi) = \bar{R}_{\text{B0}}(\pi) - \bar{R}_{\text{B4}}(\pi)$$
   Evaluated with McNemar's exact test and 95% bootstrap confidence intervals.
3. **Continuous Goal Distance Effect ($H_D$):**
   $$H_D(\pi) = \bar{D}_{\text{B4}}(\pi) - \bar{D}_{\text{B0}}(\pi)$$
   Evaluated with paired continuous $t$-test and Wilcoxon signed-rank test.
4. **Policy-Ranking Inversion Index ($\rho_{\text{rank}}$):**
   Spearman rank correlation of policy recovery rates between Condition B0 and Condition B4:
   $$\rho_{\text{rank}} = 1 - \frac{6 \sum d_i^2}{K(K^2 - 1)}$$
   Tests whether memory-deprived evaluation flips the apparent superiority of architectures.
5. **Detection Latency ($L_d$):** Steps between perturbation onset ($t_{\text{pert}}$) and automated deviation detection ($t_d$).
6. **Control Smoothness ($S_u$):** Cumulative action derivative norm $\sum_{t=t_d}^T \|a_t - a_{t-1}\|_2^2$.

---

## 7. Storage, Reproducibility, and Compute Budget

- **Complete Data Lineage:** Every single recovery rollout across B0, B1, B2, B4 will save full trajectory NPZ arrays (`obs`, `action`, `state`, `contact`) and metadata JSON.
- **SHA-256 Checksum Validation:** Manifests will log SHA-256 hashes of all configs, checkpoints, and rollout archives.
- **Compute Budget:**
  - Total simulation steps per policy: $\approx 150,000$ steps.
  - Across 3 policies: $\approx 450,000$ steps.
  - Estimated CPU runtime: $< 5$ minutes on standard multi-core CPU.
  - Storage footprint: $\approx 250\text{ MB}$ total compressed NPZ/JSON.

---

## 8. Benchmark Governance

- **Execution Gate:** This design specification is frozen. Implementation and execution of Phase 5/6 benchmark rollouts remain strictly paused until explicit authorization is granted.

