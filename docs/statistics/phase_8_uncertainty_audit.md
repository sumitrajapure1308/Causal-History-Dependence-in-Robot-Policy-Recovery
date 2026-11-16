# Phase 8 Statistical Uncertainty and Power Audit

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Status:** VALIDATED AUDIT  
**Document:** `docs/statistics/phase_8_uncertainty_audit.md`  
**Date:** 2026-11-09  

---

## 1. Forensic Audit of the [0, 0] Bootstrap Confidence Interval

In Phases 6 and 7, paired bootstrap analysis for the difference between B0 and B4 success rates returned:
$$\Delta \text{Success}_{B0 - B4} = 0.0, \quad 95\% \text{ CI } = [0.000, 0.000]$$

### The Mathematical Mechanism Behind [0, 0]:
Let $d_i = y_{i, B0} - y_{i, B4} \in \{-1, 0, +1\}$ denote the paired outcome difference for scenario $i \in \{1, \dots, N\}$.
When every observed pair in the sample has identical outcomes ($y_{i, B0} = y_{i, B4}$), the empirical sample of differences is degenerate:
$$\mathcal{D} = \{0, 0, \dots, 0\}$$
Under non-parametric empirical bootstrap resampling:
- Any resample $\mathcal{D}^*$ of size $N$ drawn with replacement from $\mathcal{D}$ consists exclusively of zeros.
- The resampled mean is $\bar{d}^* = 0.0$ with probability $1.0$.
- The 2.5th and 97.5th percentiles of the bootstrap distribution are identically $[0.0, 0.0]$.

### The Scientific Fallacy:
Reporting $[0, 0]$ as evidence of "population equivalence" or "zero causal history effect" is a severe statistical fallacy:
1. It conflates **sample degeneracy** with **population certainty**.
2. With a finite sample of $N=20$ scenarios, observing zero discordant outcomes is entirely consistent with a true population discordance rate as high as **16.1%**.
3. Therefore, non-parametric bootstrap percentiles must never be reported on degenerate binary difference samples without explicit qualification.

---

## 2. Rigorous Uncertainty Bounds for Discordance Rate ($N=20$)

To quantify the true uncertainty on the independent scenario pool ($N=20$), we use exact binomial inference (Wilson Score Interval and Clopper-Pearson Exact Interval) rather than naive bootstrap resampling.

### Distinct Quantities Formally Disentangled:
1. **Signed Average Paired Difference ($\bar{d}$):**
   $$\bar{d} = \frac{1}{N} \sum_{i=1}^N (y_{i, B0} - y_{i, B4}) \in [-1.0, +1.0]$$
2. **Absolute Value of Average Paired Difference ($|\bar{d}|$):**
   $$|\bar{d}| = \left| \frac{1}{N} \sum_{i=1}^N (y_{i, B0} - y_{i, B4}) \right| \in [0.0, 1.0]$$
3. **Discordance Rate ($p_{\text{disc}}$):**
   $$p_{\text{disc}} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(y_{i, B0} \neq y_{i, B4}) \in [0.0, 1.0]$$
   *(Note: $\bar{d}$ can be zero even if $p_{\text{disc}} > 0$ when discordant outcomes cancel symmetrically).*

---

## 3. Reconciled Statistical Metrics Table

The table below reports exact empirical metrics across all 4 evaluated policy checkpoints on the 20 frozen development scenarios with properly computed uncertainty intervals:

| Policy Checkpoint | Sample Size ($N_{\text{indep}}$) | Success B0 ($k/N$) | Success B4 ($k/N$) | Signed Mean Diff ($\bar{d}$) | Abs Mean Diff ($|\bar{d}|$) | Discordant Scenarios ($k$) | Discordance Rate ($\hat{p}_{\text{disc}}$) | Wilson 95% CI on Discordance Rate | Clopper-Pearson Exact 95% CI |
|---|---|---|---|---|---|---|---|---|---|
| `recovery_augmented_gru_seed42` | 20 | 2 / 20 (10.0%) | 2 / 20 (10.0%) | 0.00 (0.0%) | 0.00 (0.0%) | 0 / 20 | 0.0% | **[0.0%, 16.1%]** | [0.0%, 16.8%] |
| `recovery_augmented_gru_seed123` | 20 | 4 / 20 (20.0%) | 4 / 20 (20.0%) | 0.00 (0.0%) | 0.00 (0.0%) | 0 / 20 | 0.0% | **[0.0%, 16.1%]** | [0.0%, 16.8%] |
| `recovery_augmented_gru_seed456` | 20 | 3 / 20 (15.0%) | 5 / 20 (25.0%) | -0.10 (-10.0%) | 0.10 (10.0%) | 2 / 20 | **10.0%** | **[2.8%, 29.8%]** | [1.2%, 31.7%] |
| `recovery_augmented_mlp_seed42` | 20 | 5 / 20 (25.0%) | 5 / 20 (25.0%) | 0.00 (0.0%) | 0.00 (0.0%) | 0 / 20 | 0.0% | **[0.0%, 16.1%]** | [0.0%, 16.8%] |

---

## 4. Key Takeaways for Future Experimental Power

1. **Independent Unit of Analysis:** The independent unit of analysis is the unique physical failure scenario ($N$), **not the product of scenarios and deterministic evaluation repeats**. In Phase 7, logging 3 identical seeds artificially gave the appearance of $N=60$. In reality, $N=20$.
2. **True Uncertainty Bounds:** For `recovery_augmented_gru_seed456`, the observed discordance rate is $10.0\%$ with a 95% Wilson confidence interval of $[2.8\%, 29.8\%]$. This definitively proves that history interventions can produce non-zero behavioral and outcome divergences when memory reconstruction is properly executed.
3. **Confirmatory Testing Boundary:** No confirmatory hypothesis testing is performed in this phase. The 20 scenarios remain strictly development data.

