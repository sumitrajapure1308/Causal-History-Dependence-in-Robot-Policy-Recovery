# Phase 9 Pre-Registration Protocol: Fresh Held-Out Pilot Evaluation

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Document:** `docs/methodology/phase_9_pilot_preregistration.md`  
**Registration Status:** PRE-REGISTERED & FROZEN (Registered PRIOR to held-out rollout execution)  
**Date of Freeze:** 2026-11-09  
**Lead Scientist & Auditor:** Lead Robotics Researcher & Reproducibility Auditor  

---

## 1. Administrative Boundaries and Scientific Scope

This document pre-registers the experimental design, scenario cohort, policy checkpoints, evaluation seeds, intervention semantics, primary outcomes, statistical tests, and decision rules for Phase 9.

### Explicit Methodological Commitments:
1. **Pre-Registration Freeze:** All design choices, scenario IDs, metric formulas, and statistical thresholds documented herein are permanently frozen prior to the execution of any held-out recovery rollout.
2. **Held-Out Status:** The 45 scenarios registered herein were newly generated from fresh seed space ($\ge 5000$) and have never been inspected, evaluated, or tuned upon in any prior phase.
3. **No Retrospective Modification:** No matching tolerance, success threshold, or statistical plan may be adjusted post-hoc after inspecting rollout outcomes.
4. **Non-Confirmatory Framing:** All findings from this phase are formally classified as:  
   *“Pre-registered held-out pilot analysis — exploratory, not confirmatory.”*

---

## 2. Frozen Experimental Cohorts

### 2.1 Frozen Held-Out Scenarios ($N=45$)
The pilot evaluates exactly 45 admitted and verified paired scenarios generated in `results/heldout_pilot/scenarios/`:
```
heldout_s5003_t45_46e586, heldout_s5004_t46_ff166f, heldout_s5010_t43_ebcd74, heldout_s5015_t36_658825,
heldout_s5021_t37_898e82, heldout_s5022_t52_d40b31, heldout_s5033_t36_874235, heldout_s5035_t59_728e4f,
heldout_s5043_t73_eb4141, heldout_s5045_t41_fe001e, heldout_s5049_t49_d04ecd, heldout_s5053_t61_7f6b74,
heldout_s5063_t39_8c692e, heldout_s5066_t55_eab0ad, heldout_s5072_t63_f50b7b, heldout_s5073_t57_f26dff,
heldout_s5076_t51_f18ac5, heldout_s5078_t54_88bfd0, heldout_s5088_t37_ae05d3, heldout_s5091_t36_853624,
heldout_s5093_t42_ed9491, heldout_s5094_t47_c72ee6, heldout_s5101_t50_178cd0, heldout_s5112_t56_62628e,
heldout_s5114_t61_b14294, heldout_s5115_t78_1f2331, heldout_s5117_t54_f7de5b, heldout_s5121_t38_1748d9,
heldout_s5132_t56_1ac7ad, heldout_s5133_t62_608f04, heldout_s5141_t64_ee12c9, heldout_s5145_t55_3dece3,
heldout_s5147_t35_af9487, heldout_s5155_t63_8e832d, heldout_s5156_t40_fd1cc1, heldout_s5162_t58_6e63cf,
heldout_s5171_t37_3913eb, heldout_s5189_t42_936307, heldout_s5197_t63_b1314c, heldout_s5199_t45_9b60aa,
heldout_s5203_t52_1e18b0, heldout_s5219_t53_57d533, heldout_s5225_t47_2c4066, heldout_s5231_t40_5c689b,
heldout_s5234_t33_790c5b
```
- **Severity Stratification:** Small (23), Medium (16), Large (6).
- **Mean Failure Yaw:** $22.47^\circ$.
- **Mean Lateral Drift:** $0.0262\text{ m}$.
- **Mean Remaining Horizon:** 99.2 steps.

### 2.2 Frozen Evaluated Policy Architectures & Checkpoints
Only existing pre-trained checkpoints are evaluated. Zero training or hyperparameter tuning is permitted.

1. **Reactive MLP (`reactive_mlp`):**
   - Checkpoint: `models/checkpoints/reactive_mlp_best.pt` (SHA-256: `f99beb840b878d34...`)
   - Training Seed: 42. Non-recurrent baseline.
2. **Nominal History-Aware GRU (`history_gru`):**
   - Checkpoint: `models/checkpoints/history_gru_best.pt` (SHA-256: `5fcf94e2410efca8...`)
   - Training Seed: 42. Nominal BC baseline.
3. **Recovery-Augmented MLP (`recovery_augmented_mlp`):**
   - Primary Checkpoint: `results/recovery_training/checkpoints/recovery_augmented_mlp_seed42.pt` (SHA-256: `1aba926f4ad7bbd1...`)
   - Replicate Checkpoints: `seed123.pt`, `seed456.pt`.
4. **Recovery-Augmented GRU (`recovery_augmented_gru`):**
   - Primary Checkpoint: `results/recovery_training/checkpoints/recovery_augmented_gru_seed456.pt` (SHA-256: `7888cc1fc63b7d2d...`)
   - Replicate Checkpoints: `seed42.pt`, `seed123.pt`.

### 2.3 Frozen Evaluation Seeds
To evaluate execution repeatability, exactly three distinct seeds are pre-registered:
$$\text{Seeds} = [7001, 7002, 7003]$$
These seeds are completely disjoint from all training seeds (1000–1049, 3000–3059) and scenario seeds (5000–5234).

### 2.4 Frozen History Interventions
The 5 standard counterfactual conditions are evaluated:
- **Condition B0:** Full preserved history (reconstructed policy-specific memory via prefix unrolling).
- **Condition B1:** Action history masked ($a_{\text{prev}} = \mathbf{0}_3$; recurrent memory intact).
- **Condition B2:** Observation history window masked (padded with repeat of current observation; recurrent memory intact).
- **Condition B3:** Recurrent memory reset ($h(t_{\text{dev}}) = \mathbf{0}_{128}$; explicit buffers intact).
- **Condition B4:** Full history removed / direct matched-state injection ($h = \mathbf{0}_{128}$, $a_{\text{prev}} = \mathbf{0}_3$, obs buffer padded, duration counter reset to 0).

*Total Rollouts Planned:*  
45 scenarios $\times$ 5 conditions $\times$ 3 evaluation seeds $\times$ 4 policies = **2,700 recovery rollouts**.

---

## 3. Frozen Outcome Metrics and Statistical Analysis Plan

### 3.1 Primary Outcome Metric
**Paired Recovery-Success Difference ($\Delta R_{B0 - B4}$):**
$$\Delta R_{B0 - B4} = \frac{1}{N} \sum_{i=1}^N \big( y_{i, B0} - y_{i, B4} \big) \in [-1.0, +1.0]$$
where $y_{i, c} \in \{0, 1\}$ is binary task success for scenario $i$ under condition $c$.

### 3.2 Secondary Outcome Metrics
1. **First-Action Divergence ($\|a_{B0}(0) - a_c(0)\|$):** Euclidean distance between initial actions emitted at $t_{\text{dev}}$.
2. **Action-Sequence Trajectory MAE ($\frac{1}{T} \sum_{t} |a_{B0}(t) - a_c(t)|$):** Mean absolute error across motor channels.
3. **Physical Object Position Drift ($\frac{1}{T} \sum_{t} \|p_{B0}^{\text{obj}}(t) - p_c^{\text{obj}}(t)\|$):** Cumulative path divergence.
4. **Discordance Rate ($p_{\text{disc}}$):** Proportion of scenarios where $y_{B0} \neq y_c$.
5. **Continuous Goal Distance Error:** Final Euclidean distance from cube to target.
6. **Recovery Time ($t_{\text{rec}}$):** Timesteps required to reach goal boundary.

### 3.3 Statistical Testing Framework
For each paired comparison ($B0$ vs. $B1, B2, B3, B4$ and $B1, B2, B3$ vs. $B4$):
- **Exact McNemar's Test:** Computed on the $2 \times 2$ contingency table of binary discordant pairs $(n_{01}, n_{10})$.
- **Paired Wilcoxon Signed-Rank Test:** Computed on continuous final goal distance differences.
- **Confidence Intervals:** 95% Wilson Score Confidence Interval for discordance rates; 95% BCa bootstrap CI for continuous differences.
- **Multiple Comparisons:** Holm-Bonferroni step-down correction applied across the family of hypotheses ($\alpha = 0.05$).

---

## 4. Pre-Registered Stopping & Interpretation Rules

1. **Stopping Rule:** Execution halts immediately upon completion of the 2,700 rollouts and diagnostic reports. No hyperparameter adjustment, data filtering, or benchmark expansion is permitted.
2. **Interpretation Rules:**
   - If $\Delta R_{B0 - B4} \neq 0$ with $p_{\text{adj}} < 0.05$, the pilot rejects behavioral equivalence for that checkpoint.
   - If $\Delta R_{B0 - B4} = 0$ but first-action or trajectory divergence $> 0$, the pilot confirms behavioral divergence obscured by binary outcome insensitivity.
   - If both action divergence and outcome divergence are zero, the pilot confirms behavioral invariance under the tested architecture.
   - Non-significance shall **never** be reported as proof of zero effect without explicitly bounding the result with the Wilson 95% confidence interval.

