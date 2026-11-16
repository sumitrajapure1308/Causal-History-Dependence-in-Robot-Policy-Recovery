# Principled Equivalence-Analysis Plan: Statistical Testing of Causal-History Invariance

**Document ID:** `docs/design/equivalence_analysis_plan.md`  
**Status:** PRE-REGISTERED DESIGN SPECIFICATION (UNEXECUTED)  
**Project:** Causal-History Dependence in Robot Policy Recovery  
**Directory:** `causal-history-recovery/`  
**Core Statistical Tenet:** "Absence of evidence is not evidence of absence." A failure to reject the standard null hypothesis ($p > 0.05$) does not demonstrate that history dependence is zero. Statistical equivalence requires a pre-registered equivalence margin and formal Two One-Sided Tests (TOST).

---

## 1. The Exact Null Hypothesis ($H_{0,\text{equiv}}$)

In classical hypothesis testing, the null hypothesis posits zero difference ($H_0: \delta = 0$). In equivalence testing, the burden of proof is inverted: the null hypothesis posits that a practically meaningful history effect **does** exist.

Let $\delta = p_{\text{replay}} - p_{\text{inject}}$ denote the true population difference in task recovery success rate between Condition A (`M_REPLAY_PRESERVED`) and Condition B (`M_INJECT_PRESERVED`). Let $\Delta > 0$ denote the pre-registered equivalence margin.

The equivalence null hypothesis is a composite hypothesis asserting non-equivalence:

$$H_{0,\text{equiv}}: |\delta| \ge \Delta \iff \begin{cases} H_{01}: \delta \le -\Delta & (\text{Replay is meaningfully inferior}) \\ H_{02}: \delta \ge +\Delta & (\text{Replay is meaningfully superior}) \end{cases}$$

To conclude equivalence, both $H_{01}$ and $H_{02}$ must be rejected simultaneously at significance level $\alpha$.

---

## 2. The Exact Alternative Hypothesis ($H_{1,\text{equiv}}$)

The alternative hypothesis posits that any true causal difference attributable to execution history lies strictly within the zone of practical equivalence:

$$H_{1,\text{equiv}}: -\Delta < \delta < +\Delta \iff |\delta| < \Delta$$

If $H_{0,\text{equiv}}$ is rejected in favor of $H_{1,\text{equiv}}$, the formal scientific conclusion is that the causal effect of physical execution history is bounded within $[-\Delta, +\Delta]$ at confidence level $100(1 - 2\alpha)\%$.

---

## 3. The Paired Comparison Unit

The statistical unit of observation is the **matched scenario episode replicate**:

$$u = (s, k, \pi)$$

Where:
- $s \in \mathcal{S}$: Unique failure scenario identified by task geometry, object mass, friction, initial pose jitter, and perturbation schedule.
- $k \in \{7001, 7002, 7003\}$: Stochastic rollout evaluation seed controlling post-intervention actuator noise.
- $\pi \in \Pi$: Fixed, frozen policy architecture checkpoint.

Each unit $u$ generates an aligned binary pair $(Y_{\text{replay}}^{(u)}, Y_{\text{inject}}^{(u)}) \in \{0, 1\}^2$, where:
- $Y = 1$ indicates binary task success (target reached with $N_{\text{dwell}} \ge 5$ consecutive steps).
- $Y = 0$ indicates task failure or boundary escape.

Both rollouts in the pair originate from identical simulator snapshots ($D \le 10^{-10}\text{ m}$) and execute under the identical seed $k$.

---

## 4. The Primary Outcome

The primary outcome is the **Paired Risk Difference** ($\hat{\delta}$):

$$\hat{\delta} = \hat{p}_{\text{replay}} - \hat{p}_{\text{inject}} = \frac{1}{M} \sum_{u=1}^{M} \left( Y_{\text{replay}}^{(u)} - Y_{\text{inject}}^{(u)} \right) = \frac{b - c}{M}$$

Where:
- $M = N_{\text{scenarios}} \times K_{\text{seeds}}$: Total number of paired evaluations.
- $b$: Number of discordant pairs where Replay succeeded and Injection failed ($Y_{\text{replay}} = 1, Y_{\text{inject}} = 0$).
- $c$: Number of discordant pairs where Replay failed and Injection succeeded ($Y_{\text{replay}} = 0, Y_{\text{inject}} = 1$).
- $a$: Concordant successes ($Y_{\text{replay}} = 1, Y_{\text{inject}} = 1$).
- $d$: Concordant failures ($Y_{\text{replay}} = 0, Y_{\text{inject}} = 0$).

---

## 5. The Practical Equivalence Margin ($\Delta$)

The pre-registered practical equivalence margin is:

$$\Delta = 0.05 \quad (\pm 5.0\text{ percentage points})$$

The equivalence zone is defined by the symmetric interval:

$$\mathcal{E} = [-\Delta, +\Delta] = [-0.05, +0.05]$$

---

## 6. Why That Margin is Scientifically Meaningful

The selection of $\Delta = 0.05$ is grounded in operational robotics benchmarks rather than post-hoc data inspection:

1. **Stochastic Benchmark Floor in Manipulation:** In contemporary robotic recovery benchmarks (e.g., RoboRecover, LIBERO-Recover), run-to-run stochastic variance across random seed initializations and simulator micro-collisions routinely induces performance fluctuations of $5\%–10\%$. An effect smaller than $5\%$ is within the noise floor of physical manipulation.
2. **Operational Utility:** In autonomous tabletop task recovery, a success rate difference of fewer than 5 episodes per 100 encounters ($|\delta| < 0.05$) does not justify the computational and memory overhead of recording, buffering, and unrolling long historical trajectory prefixes.
3. **Control Sufficiency Criterion:** If instantaneous physical coordinates ($q_{\text{pos}}, q_{\text{vel}}$, contacts) reproduce recovery success within $\pm 5\%$ of full trajectory history, the instantaneous Markov state is established as an operationally sufficient statistic for closed-loop recovery control.

---

## 7. The Confidence-Interval Method

Under the TOST operational framework, equivalence at level $\alpha$ corresponds to establishing that the **$100(1 - 2\alpha)\%$ two-sided confidence interval** for $\delta$ falls entirely within $[-\Delta, +\Delta]$. For $\alpha = 0.05$, this requires calculating the **90% confidence interval** (or conservative 95% confidence interval for $\alpha = 0.025$).

### Primary Method: Tango / Newcombe-Wilson Paired Score Interval
Because manipulation recovery failure rates are often high ($p \to 0$), standard Wald normal approximations fail. The primary interval is computed via the paired score-based Newcombe-Wilson method:

$$\text{CI}_{1-2\alpha}(\delta) = \left[ \hat{\delta} - z_{1-\alpha} \sqrt{\frac{w_1 + w_2 - 2 \hat{\phi} \sqrt{w_1 w_2}}{M}}, \quad \hat{\delta} + z_{1-\alpha} \sqrt{\frac{w_1 + w_2 - 2 \hat{\phi} \sqrt{w_1 w_2}}{M}} \right]$$

where $w_1, w_2$ are Wilson score variances for the marginal proportions, and $\hat{\phi}$ is the empirical inter-condition correlation.

### Secondary Method: Cluster-Preserving Bootstrap CI
To account for potential intra-scenario correlation across the 3 evaluation seeds:
- $B = 10,000$ bootstrap resamples clustered at the scenario level ($s \in \mathcal{S}$).
- Bias-corrected and accelerated (BCa) percentile intervals reported alongside the analytical score interval.

---

## 8. The Paired Test: Two One-Sided Tests (TOST)

The TOST procedure decomposes equivalence into two simultaneous one-sided test statistics:

$$Z_1 = \frac{\hat{\delta} - (-\Delta)}{\text{SE}_{\text{paired}}(\hat{\delta})} = \frac{\hat{\delta} + \Delta}{\sqrt{\frac{b + c - (b - c)^2 / M}{M^2}}}$$

$$Z_2 = \frac{\hat{\delta} - (+\Delta)}{\text{SE}_{\text{paired}}(\hat{\delta})} = \frac{\hat{\delta} - \Delta}{\sqrt{\frac{b + c - (b - c)^2 / M}{M^2}}}$$

### Decision Rule:
- Compute one-sided p-values: $p_1 = 1 - \Phi(Z_1)$ and $p_2 = \Phi(Z_2)$.
- The overall equivalence p-value is:
  $$p_{\text{TOST}} = \max(p_1, p_2)$$
- Reject $H_{0,\text{equiv}}$ and declare equivalence if:
  $$p_{\text{TOST}} < \alpha \quad (\alpha = 0.05)$$

For small discordant counts ($b + c < 20$), exact conditional binomial testing on discordant pairs is applied:
$$p_1 = P(X \ge b \mid X \sim \text{Binomial}(b + c, \pi_L)), \quad p_2 = P(X \le b \mid X \sim \text{Binomial}(b + c, \pi_U))$$

---

## 9. Effect-Size Definition

To provide a complete profile beyond raw proportion difference, four complementary effect-size metrics are tracked:

| Effect-Size Metric | Mathematical Definition | Standard Interpretation Thresholds |
| :--- | :--- | :--- |
| **Risk Difference ($\delta$)** | $\delta = p_{\text{replay}} - p_{\text{inject}}$ | Negligible: $|\delta| < 0.05$; Meaningful: $|\delta| \ge 0.05$ |
| **Relative Risk ($\text{RR}$)** | $\text{RR} = p_{\text{replay}} / p_{\text{inject}}$ | Parity: $\text{RR} = 1.0$; Equivalence bounds: $[0.80, 1.25]$ |
| **Discordance Odds Ratio ($\text{OR}$)** | $\text{OR} = (b + 0.5) / (c + 0.5)$ | Parity: $\text{OR} = 1.0$; Asymmetry: $\text{OR} > 1.5$ or $< 0.67$ |
| **Cohen's $g$ for Paired Proportions** | $g = \frac{b}{b + c} - 0.5$ | Negligible: $|g| < 0.05$; Small: $0.05 \le |g| < 0.15$; Medium: $|g| \ge 0.15$ |

---

## 10. Multiple-Comparison Correction

When testing equivalence across multiple policy architectures ($K_{\text{pol}} = 4$) and benchmark tasks ($K_{\text{task}} = 2$):

1. **Family-Wise Error Rate (FWER) via Holm-Bonferroni:**
   - Applied across the four primary policy architecture comparisons.
   - For $m = 4$ contrasts, ordered p-values $p_{(1)} \le p_{(2)} \le p_{(3)} \le p_{(4)}$ are compared against $\alpha / (m - i + 1)$.
2. **False Discovery Rate (FDR) via Benjamini-Hochberg:**
   - Applied across all secondary exploratory subgroups (failure mode cells, severity tiers, contact modes).
   - Equivalence is declared at $\alpha_{\text{FDR}} = 0.05$ if:
     $$p_{(k)} \le \frac{k}{K_{\text{total}}} \cdot 0.05$$
3. **Independent Positive Control:**
   - Positive-control tests are evaluated in a separate hypothesis family; no alpha-splitting between benchmark equivalence and instrument validation is required.

---

## 11. Sample-Size and Statistical Power Requirements

For paired McNemar/TOST testing of equivalence with margin $\Delta = 0.05$ at significance level $\alpha = 0.05$ and target power $1 - \beta = 0.90$:

$$M_{\text{required}} \ge \frac{\left( z_{1-\alpha} + z_{1-\beta/2} \right)^2 \cdot \sigma_{\text{paired}}^2}{\Delta^2}$$

Where $\sigma_{\text{paired}}^2 = p_{10} + p_{01} - (p_{10} - p_{01})^2$.

- Under matched physical simulation, paired concordance is high ($p_{00} + p_{11} \approx 0.95$), yielding an expected discordant proportion $p_{\text{disc}} = p_{10} + p_{01} \le 0.05$.
- For $p_{\text{disc}} = 0.05$ and true $\delta = 0$:
  $$M_{\text{required}} \approx \frac{(1.645 + 1.645)^2 \cdot 0.05}{(0.05)^2} = \frac{10.82 \cdot 0.05}{0.0025} \approx 216 \text{ paired rollouts}$$
- With $N = 200$ scenarios evaluated across $K = 3$ seeds, the sample size is **$M = 600$ paired rollouts per policy architecture**.
- **Statistical Power:** $M = 600$ provides statistical power **$> 98\%$** to detect equivalence within $\pm 0.05$, ensuring an extremely low false-negative risk.

---

## 12. Tripartite Outcome Categorization

The protocol pre-registers three mutually exclusive, exhaustive outcome classifications:

```
                                [ Observed 90% Confidence Interval ]
                                                 |
         +---------------------------------------+---------------------------------------+
         |                                       |                                       |
  [Case 1: EQUIVALENCE]                   [Case 2: HISTORY EFFECT]                [Case 3: INCONCLUSIVE]
  CI strictly inside [-0.05, +0.05]       CI excludes 0 AND |delta| >= 0.05       CI straddles boundary (-0.05 or +0.05)
  p_TOST < 0.05                           p_McNemar < 0.01                        p_TOST >= 0.05 and p_McNemar >= 0.05
  -> History effect bounded               -> Significant history effect           -> Study underpowered to decide
```

### Outcome Case 1: Equivalence Supported
- **Empirical Criterion:** The $90\%$ CI for $\delta$ lies entirely inside the equivalence zone:
  $$\text{CI}_{90\%}(\delta) \subset [-0.05, +0.05] \quad \text{and} \quad p_{\text{TOST}} < 0.05$$
- **Permissible Scientific Claim:** *"The effect of physical trajectory history on recovery success is statistically bounded within $\pm 5\%$, demonstrating practical history invariance under the tested execution-failure conditions."*

### Outcome Case 2: History Effect Supported
- **Empirical Criterion:** The classical two-sided McNemar test rejects the null ($p < 0.01$) and the estimated effect size exceeds the equivalence threshold:
  $$|\hat{\delta}| \ge 0.05 \quad \text{and} \quad \text{CI}_{95\%}(\delta) \text{ excludes } 0$$
- **Permissible Scientific Claim:** *"Execution history provides a statistically significant, practically meaningful recovery advantage of magnitude $\hat{\delta}$, confirming history dependence."*

### Outcome Case 3: Inconclusive / Underpowered
- **Empirical Criterion:** The confidence interval straddles either equivalence bound:
  $$\text{CI}_{\text{lower}} < -0.05 \quad \text{or} \quad \text{CI}_{\text{upper}} > +0.05$$
  while the classical test fails to reject $p_{\text{McNemar}} \ge 0.05$.
- **Permissible Scientific Claim:** *"The evaluation is inconclusive: while no significant history advantage was detected, the data cannot exclude a history effect of magnitude up to $\text{CI}_{\text{upper}}$."*
- **Strict Prohibition:** It is strictly forbidden to claim equivalence or invariance under Outcome Case 3.

---

## 13. Prevention of Margin Hacking (Post-Hoc HARKing)

To guarantee that equivalence bounds are not selected or adjusted to fit empirical observations:

1. **Pre-Registered Freezing:** The margin $\Delta = \pm 0.05$ is committed in this specification prior to running any held-out evaluations.
2. **Independence from Data:** The value $\Delta = 0.05$ is derived from domain noise considerations ($5\%$ stochastic floor in manipulation benchmarks), completely independent of observed Stage C estimates ($0.0077$).
3. **Transparent Equivalence Curves:** All reports must plot the continuous equivalence curve showing $p_{\text{TOST}}$ across a range of hypothetical margins $\Delta \in [0.01, 0.10]$:
   - This prevents hiding boundary sensitivity and makes the exact threshold at which equivalence is achieved completely transparent to reviewers.
4. **Prohibition of Shifting Margins:** If an evaluation fails to establish equivalence at $\Delta = 0.05$, widening the margin post-hoc (e.g., to $\Delta = 0.08$) to achieve a nominal positive equivalence finding is strictly prohibited.

---

## 14. Universal Invariance Prohibition Notice

- **No Universal Markovian Claims:** Establishing equivalence on this benchmark demonstrates that *in the evaluated tabletop pushing environments under low-dimensional state observability*, execution history provides negligible recovery utility.
- **Explicit Domain Bounding:** The findings cannot be extrapolated to claim that all robotic systems are Markovian. Environments with unmodeled internal dynamics (fluid sloshing, non-rigid deformability, thermal drift, motor winding hysteresis) or partial observability remain prospective domains for history dependence.

---

## 15. Protocol Integrity Notice

- **No Experiment Run:** This document defines the formal pre-registered equivalence analysis plan. No new rollouts or benchmark re-analyses were executed.
- **Original Stage C Results Unmodified:** The empirical records in `results/phase_12_stage_c/` remain strictly immutable.
- **Zero Fabrication:** No empirical p-values or confidence intervals are fabricated or claimed as observed held-out outcomes.

