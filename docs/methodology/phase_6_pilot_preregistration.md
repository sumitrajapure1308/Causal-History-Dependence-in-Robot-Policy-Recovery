# Phase 6 Pilot Recovery Experiment: Pre-Registration Protocol

> **Document Type:** Pre-Registered Research Protocol & Experimental Freeze  
> **Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
> **Phase:** 6 (Pre-Registered Pilot Recovery Experiment)  
> **Pre-Registration Date:** 2026-11-09  
> **Protocol Status:** `FROZEN & PRE-REGISTERED`  
> **Mandatory Rule:** All hypotheses, scenarios, seeds, conditions, stopping criteria, and analysis pipelines are frozen prior to observing recovery outcomes. Zero post-hoc scenario modifications permitted.

---

## 1. Research Objectives & Hypotheses

The central scientific question of this pilot experiment is:
> When physically equivalent robot failure states ($D \le 1.0 \times 10^{-6}$) are reached through different execution histories, do robot policies show differential recovery success, detection latency, diagnosis accuracy, or control effort?

### Pre-Registered Hypotheses:
1. **Primary Null Hypothesis ($H_{0,1}$):** Across physically matched recoverable failure states, the recovery success rate under preserved execution history (B0) is identical to recovery success under full history removal (B4):
   $$H_{0,1}: R_{\text{B0}} = R_{\text{B4}} \iff H_R \equiv 0$$
2. **Memoryless Control Invariance ($H_{0,\text{MLP}}$):** For the Reactive MLP policy, because the architecture is strictly Markovian with zero recurrent hidden state, recovery outcomes across B0, B2, B3, and B4 will be identically concordant:
   $$R_{\text{B0}}^{(\text{MLP})} = R_{\text{B2}}^{(\text{MLP})} = R_{\text{B3}}^{(\text{MLP})} = R_{\text{B4}}^{(\text{MLP})}$$
3. **History Dependence in Recurrent Policy ($H_{1,\text{GRU}}$):** For the History-Aware GRU policy, counterfactual ablation of observation history (B2), action history (B1), or hidden state (B3, B4) will alter recovery trajectories and success rates.

---

## 2. Frozen Scenario Cohort (38 Validated Paired Scenarios)

The experiment evaluates the exact 38 paired scenarios validated during Phase 5, indexed in `results/paired_scenarios/scenario_manifest.json`:

```
Frozen Scenario Set (N=38):
- Base Seed 42 Cohort (11 scenarios):
  scen_history_gru_s49_t53_a2060d, scen_history_gru_s91_t58_aaa2eb, scen_history_gru_s98_t44_7ab7a5,
  scen_history_gru_s112_t49_ff2be3, scen_history_gru_s133_t40_aec8cd, scen_history_gru_s147_t38_093d6c,
  scen_history_gru_s196_t52_41373d, scen_history_gru_s217_t41_5bfdbf, scen_history_gru_s231_t52_974c53,
  scen_history_gru_s238_t78_e2f899, scen_history_gru_s252_t69_019ca8, scen_history_gru_s287_t60_1fd1a1,
  scen_history_gru_s301_t65_98b140, scen_history_gru_s308_t68_fead8b, scen_history_gru_s385_t50_4ccf26
- Base Seed 500 Cohort (13 scenarios):
  scen_history_gru_s528_t62_0de71c, scen_history_gru_s570_t40_3d7ffb, scen_history_gru_s591_t38_ca1850,
  scen_history_gru_s626_t46_7f48c2, scen_history_gru_s633_t43_4dd0e4, scen_history_gru_s773_t40_1299cf,
  scen_history_gru_s787_t57_d08f87, scen_history_gru_s801_t56_ae1e3e, scen_history_gru_s843_t40_f44552
- Base Seed 2000 Cohort (14 scenarios):
  scen_history_gru_s2007_t55_0e43ec, scen_history_gru_s2021_t37_5b3e3d, scen_history_gru_s2028_t53_1919df,
  scen_history_gru_s2042_t46_f049e3, scen_history_gru_s2056_t44_74fb29, scen_history_gru_s2063_t40_6de7de,
  scen_history_gru_s2070_t37_29f99c, scen_history_gru_s2105_t65_1ad9f5, scen_history_gru_s2133_t74_efc3f5,
  scen_history_gru_s2147_t64_9b32c6, scen_history_gru_s2175_t64_9273f0, scen_history_gru_s2273_t54_230919,
  scen_history_gru_s2287_t52_f5d606, scen_history_gru_s2329_t63_ce2a10
```

- **Severity Distribution:** Small (12 scenarios), Medium (20 scenarios), Large (6 scenarios).
- **Physical Recoverability:** All 38 scenarios passed $R_{\text{oracle}} == 1$ verification.

---

## 3. Frozen Policy Suite & Checkpoints

Two policies evaluated under deterministic inference mode ($\mu$):
1. **Reactive MLP Policy:**
   - Checkpoint: `models/checkpoints/reactive_mlp_best.pt`
   - Architecture: 20-dim observation $\to 128 \to 128 \to 3$-dim Cartesian action delta.
   - Memory capacity: $k = 0$ (memoryless baseline).
2. **History-Aware GRU Policy:**
   - Checkpoint: `models/checkpoints/history_gru_best.pt`
   - Architecture: 23-dim token ($o_t \oplus a_{t-1}$) $\to \text{GRU}_{128} \to 64 \to 3$-dim action delta.
   - Memory capacity: recurrent hidden state $\mathbf{h} \in \mathbb{R}^{128}$ + 10-step observation window ($k=10$).

---

## 4. Frozen Counterfactual Conditions

For each scenario $i$, five conditions are evaluated from the identical physical state snapshot $s(t_d)$:

| Condition ID | Description | Observation History | Action History | Contact History | Policy Hidden State | Physical State Source |
|---|---|---|---|---|---|---|
| **B0** | Full Preserved History | Intact $(\mathbf{o}_{t_d-k:t_d})$ | Intact $(\mathbf{a}_{0:t_d-1})$ | Intact | Intact $\mathbf{h}(t_d)$ | Exact Replay to $s(t_d)$ |
| **B1** | Action History Removed | Intact $(\mathbf{o}_{t_d-k:t_d})$ | Zero-Masked ($\mathbf{a} \gets \mathbf{0}$) | Intact | Intact $\mathbf{h}(t_d)$ | Exact Replay to $s(t_d)$ |
| **B2** | Observation History Removed | Padded $(\mathbf{o}_{\text{curr}})$ | Intact $(\mathbf{a}_{0:t_d-1})$ | Intact | Intact $\mathbf{h}(t_d)$ | Exact Replay to $s(t_d)$ |
| **B3** | Policy Hidden State Reset | Intact $(\mathbf{o}_{t_d-k:t_d})$ | Intact $(\mathbf{a}_{0:t_d-1})$ | Intact | Reset ($\mathbf{h} \gets \mathbf{0}$) | Exact Replay to $s(t_d)$ |
| **B4** | All History Removed | Padded $(\mathbf{o}_{\text{curr}})$ | Zero-Masked ($\mathbf{a} \gets \mathbf{0}$) | Reset | Reset ($\mathbf{h} \gets \mathbf{0}$) | Injected Snapshot $s(t_d)$ |

---

## 5. Frozen Evaluation Matrix & Stopping Rule

- **Scenarios Evaluated:** 38 scenarios.
- **Conditions per Scenario:** 5 conditions (B0, B1, B2, B3, B4).
- **Evaluation Seeds:** 3 seeds (`[42, 500, 2000]`).
- **Policy Architectures:** 2 policies (Reactive MLP, History GRU).
- **Total Required Recovery Rollouts:**
  $$N_{\text{total}} = 38 \text{ scenarios} \times 5 \text{ conditions} \times 3 \text{ seeds} \times 2 \text{ policies} = \mathbf{1,140 \text{ rollouts}}$$
- **Stopping Rule:** Execution stops immediately upon completion of rollout 1,140. Zero selective exclusions.

---

## 6. Frozen Primary & Secondary Outcomes

### 6.1 Primary Outcome
- **Causal History Recovery Effect ($H_{R,\text{B4}}$):**
  $$H_{R,\text{B4}}(\pi) = \frac{1}{N} \sum_{i=1}^N \left( R_i^{(\text{B0})} - R_i^{(\text{B4})} \right) = \bar{R}_{\text{B0}} - \bar{R}_{\text{B4}}$$
  where $R \in \{0, 1\}$ is binary task completion: block center inside $r_{\text{goal}} = 0.060\text{ m}$, yaw deflection $\le 0.35\text{ rad}$ ($20^\circ$), and consecutive dwell time $\ge 5$ steps.

### 6.2 Secondary Outcomes
1. **Component-Specific Effects:**
   - Action History Effect: $H_{R,\text{B1}} = R_{\text{B0}} - R_{\text{B1}}$
   - Observation History Effect: $H_{R,\text{B2}} = R_{\text{B0}} - R_{\text{B2}}$
   - Recurrent State Effect: $H_{R,\text{B3}} = R_{\text{B0}} - R_{\text{B3}}$
2. **Continuous Positioning & Effort Metrics:**
   - Final goal distance: $D_{\text{goal}} = \|\mathbf{p}_{\text{obj}} - \mathbf{g}\|_2$.
   - Goal distance effect: $H_D = D_{\text{goal}}^{(\text{B4})} - D_{\text{goal}}^{(\text{B0})}$.
   - Control effort: $\sum_{t=t_d}^T \|a_t\|_2^2$.
   - Action smoothness: $\sum_{t=t_d}^T \|a_t - a_{t-1}\|_2^2$.
3. **Safety & Physical Recovery:**
   - Excessive force events: count of steps with contact force $> 50.0\text{ N}$.
   - Table boundary excursions: boolean object exit.
   - Yaw error reduction: $\Delta \theta_{\text{start}} - \Delta \theta_{\text{final}}$.

---

## 7. Frozen Statistical Testing & Multiple-Comparison Correction

1. **Paired Binary Test:** Two-sided McNemar test with Edwards continuity correction for all paired comparisons.
2. **Paired Continuous Test:** Two-sided Wilcoxon signed-rank test for continuous distances and control effort.
3. **Bootstrap Estimation:** 10,000 paired bootstrap resamples for all 95% confidence intervals.
4. **Family-Wise Error Rate Control:** Holm-Bonferroni correction applied across the family of 7 pairwise condition comparisons:
   $$\{\text{B0 vs B1}, \text{B0 vs B2}, \text{B0 vs B3}, \text{B0 vs B4}, \text{B1 vs B4}, \text{B2 vs B4}, \text{B3 vs B4}\}$$
5. **Significance Level:** $\alpha = 0.05$ (two-sided).

---

## 8. Protocol Governance & Sign-Off

This document serves as the immutable experimental contract for Phase 6. Any modification after script launch constitutes a protocol violation.

