# Formal Hypotheses & Experimental Hypotheses Matrix

This document defines the formal statistical hypotheses tested in this research. In accordance with rigorous scientific practice, no hypothesis is assumed to have a pre-ordained direction.

---

## Hypothesis 1: Causal-History Dependence ($H1$)

- **Research Question:** Does robot recovery success depend on whether a failure state is reached via action prefix replay or via matched physical state injection?
- **Null Hypothesis ($H_{0,1}$):**
  $$R_{\text{replay}} = R_{\text{injected}}$$
  *The recovery success rate for physically matched failure states is invariant to causal history.*
- **Alternative Hypothesis ($H_{1,1}$):**
  $$R_{\text{replay}} \neq R_{\text{injected}}$$
  *The recovery success rate differs significantly between prefix replay and matched injection.*
- **Statistical Test (Provisional):** Paired Wilcoxon signed-rank test (or McNemar's paired test if strictly binary) across matched scenario pairs ($N \ge 50\text{--}100$ per task, calibrated via pilot power analysis per `docs/statistics/provisional_analysis_plan.md`); reporting Cliff's delta effect size and 95% bootstrap confidence intervals of $H_R = R_{\text{replay}} - R_{\text{injected}}$.

---

## Hypothesis 2: Benchmark Ranking Stability ($H2$)

- **Research Question:** Do conventional recovery benchmarks (which test either injected shifts or replayed prefixes in isolation) produce the same policy quality rankings as causal-history matched evaluation?
- **Null Hypothesis ($H_{0,2}$):**
  $$\tau(\mathbf{r}_{\text{conventional}}, \mathbf{r}_{\text{causal}}) = 1.0 \quad \text{and} \quad \rho(\mathbf{r}_{\text{conventional}}, \mathbf{r}_{\text{causal}}) = 1.0$$
  *Policy rankings are perfectly preserved across evaluation protocols.*
- **Alternative Hypothesis ($H_{1,2}$):**
  $$\tau(\mathbf{r}_{\text{conventional}}, \mathbf{r}_{\text{causal}}) < 1.0$$
  *Policy rankings differ across evaluation protocols, exhibiting rank reversals and altered relative superiority.*
- **Statistical Test:** Kendall's rank correlation $\tau$ and Spearman's rank correlation $\rho$, with permutation test for significance against the identity ranking.

---

## Hypothesis 3: Temporal Information Effect ($H3$)

- **Research Question:** Does history-aware policy architecture improve or impair recovery when evaluating from physically matched failure states?
- **Null Hypothesis ($H_{0,3}$):**
  $$R_{\text{reactive}} = R_{\text{history-aware}}$$
  *Temporal memory in the policy architecture has no significant effect on recovery success under matched states.*
- **Alternative Hypothesis ($H_{1,3}$):**
  $$R_{\text{reactive}} \neq R_{\text{history-aware}}$$
  *Temporal memory significantly affects recovery success (either improving it via failure diagnosis context or degrading it via out-of-distribution sequence hysteresis).*
- **Statistical Test:** Two-sided paired Wilcoxon signed-rank test between BC-Reactive and BC-History on identical failure scenarios.

---

## Hypothesis 4: Recovery Training Modulation ($H4$)

- **Research Question:** Does training policies with recovery demonstrations reduce the magnitude of causal-history dependence?
- **Null Hypothesis ($H_{0,4}$):**
  $$H_R^{\text{standard}} = H_R^{\text{recovery-trained}}$$
  *Recovery-augmented training does not alter the policy's causal-history dependence metric $H_R$.*
- **Alternative Hypothesis ($H_{1,4}$):**
  $$H_R^{\text{standard}} \neq H_R^{\text{recovery-trained}}$$
  *Recovery-augmented training significantly alters the policy's causal-history dependence metric $H_R$.*
- **Statistical Test:** Independent two-sample permutation test or Mann-Whitney $U$ test comparing the distribution of $|H_R|$ across policies trained with and without recovery augmentations.

---

## Hypothesis 5: Cross-Task Invariance ($H5$)

- **Research Question:** Is causal-history dependence uniform across distinct manipulation modalities (free-space vs. contact-rich vs. articulated)?
- **Null Hypothesis ($H_{0,5}$):**
  $$H_R^{(\text{task } a)} = H_R^{(\text{task } b)} = \dots = H_R^{(\text{task } k)}$$
  *History dependence is invariant across manipulation tasks.*
- **Alternative Hypothesis ($H_{1,5}$):**
  $$\exists \, a, b \quad \text{s.t.} \quad H_R^{(\text{task } a)} \neq H_R^{(\text{task } b)}$$
  *History dependence varies significantly across task domains.*
- **Statistical Test:** Kruskal-Wallis non-parametric ANOVA on $H_R$ across tasks, followed by post-hoc Dunn's test with Holm-Bonferroni correction.

