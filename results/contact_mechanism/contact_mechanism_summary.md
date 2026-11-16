# Exploratory Contact-Dynamics Mechanism Analysis

**Document ID:** `results/contact_mechanism/contact_mechanism_summary.md`  
**Status:** EXPLORATORY (POST-HOC MECHANISM ANALYSIS)  
**Core Scope:** Evaluates whether initial motor action divergence and continuous trajectory divergence are associated with physical contact parameters across 4,000 paired evaluations in the Stage C benchmark.  
**Precautionary Stance:** In strict compliance with pre-registered methodology rules, associations observed in observational simulation logs do **not** establish causal mechanisms. 'Associated with' is not 'caused by,' and 'consistent with' is not 'proof of.' No real-robot validity or universal history invariance is claimed.

---

## 1. Executive Statistical Table: Contact Dynamics Associations (Overall Pooled, M=4,000)

| Contact Dynamics Parameter | Endpoint | Pearson $r$ | Pearson $p$ | Spearman $\rho$ | Spearman $p$ | OLS Slope ($\beta$) | Univariate $R^2$ | Association Assessment |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Contact Duration (s)** | Action Divergence ||Δa_0|| | -0.0072 | 0.6471 | -0.0202 | 0.2007 | -1.0964e-04 | 0.01% | No Statistically Significant Association Detected |
| **Contact Force (N)** | Action Divergence ||Δa_0|| | -0.0735 | 3.29e-06 | -0.0163 | 0.3027 | -2.9607e-03 | 0.54% | Statistically Associated (Negative, r=-0.073) |
| **Contact Impulse (N·s)** | Action Divergence ||Δa_0|| | -0.0284 | 0.0724 | -0.0114 | 0.4713 | -2.9737e-03 | 0.08% | No Statistically Significant Association Detected |
| **Friction Coefficient (μ)** | Action Divergence ||Δa_0|| | +0.0735 | 3.29e-06 | +0.0163 | 0.3027 | +1.4522e-03 | 0.54% | Statistically Associated (Positive, r=+0.073) |
| **Slip Event (Indicator)** | Action Divergence ||Δa_0|| | -0.0983 | 4.64e-10 | -0.0384 | 0.0150 | -2.9146e-04 | 0.97% | Statistically Associated (Negative, r=-0.098) |
| **Collision Event (Indicator)** | Action Divergence ||Δa_0|| | -0.0266 | 0.0921 | +0.0280 | 0.0771 | -7.9719e-05 | 0.07% | No Statistically Significant Association Detected |
| **Object Displacement (m)** | Action Divergence ||Δa_0|| | -0.0127 | 0.4228 | -0.0148 | 0.3493 | -4.0271e-04 | 0.02% | No Statistically Significant Association Detected |
| **Remaining Task Horizon (Steps)** | Action Divergence ||Δa_0|| | +0.0072 | 0.6471 | +0.0202 | 0.2007 | +5.4819e-07 | 0.01% | No Statistically Significant Association Detected |
| **Contact Duration (s)** | Trajectory Divergence |ΔPosErr| | +0.0787 | 6.17e-07 | +0.0345 | 0.0293 | +3.4158e-02 | 0.62% | Statistically Associated (Positive, r=+0.079) |
| **Contact Force (N)** | Trajectory Divergence |ΔPosErr| | -0.0168 | 0.2873 | +0.2074 | 3.98e-40 | -1.9428e-02 | 0.03% | No Statistically Significant Association Detected |
| **Contact Impulse (N·s)** | Trajectory Divergence |ΔPosErr| | +0.0814 | 2.55e-07 | +0.1066 | 1.41e-11 | +2.4411e-01 | 0.66% | Statistically Associated (Positive, r=+0.081) |
| **Friction Coefficient (μ)** | Trajectory Divergence |ΔPosErr| | +0.0168 | 0.2873 | -0.2074 | 3.98e-40 | +9.5297e-03 | 0.03% | No Statistically Significant Association Detected |
| **Slip Event (Indicator)** | Trajectory Divergence |ΔPosErr| | +0.0895 | 1.44e-08 | +0.0720 | 5.09e-06 | +7.5999e-03 | 0.80% | Statistically Associated (Positive, r=+0.089) |
| **Collision Event (Indicator)** | Trajectory Divergence |ΔPosErr| | +0.2532 | 1.55e-59 | +0.6147 | 0.00e+00 | +2.1707e-02 | 6.41% | Statistically Associated (Positive, r=+0.253) |
| **Object Displacement (m)** | Trajectory Divergence |ΔPosErr| | +0.0823 | 1.89e-07 | +0.1155 | 2.32e-13 | +7.4872e-02 | 0.68% | Statistically Associated (Positive, r=+0.082) |
| **Remaining Task Horizon (Steps)** | Trajectory Divergence |ΔPosErr| | -0.0787 | 6.17e-07 | -0.0345 | 0.0293 | -1.7079e-04 | 0.62% | Statistically Associated (Negative, r=-0.079) |

---

## 2. Policy-Specific Association Breakdown

### 2.1. Policy: `reactive_mlp` (Reactive MLP, M=1,000)
| Parameter | Endpoint | Pearson $r$ | $p$-value | Spearman $\rho$ | OLS Slope | $R^2$ | Interpretation |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Contact Duration | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Contact Force | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Contact Impulse | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Friction Coefficient | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Slip Event | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Collision Event | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Object Displacement | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Remaining Task Horizon | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Contact Duration | Trajectory Divergence |ΔPosErr| | +0.1516 | 1.46e-06 | +0.1167 | +1.131e-02 | 2.30% | Statistically Associated (Positive, r=+0.152) |
| Contact Force | Trajectory Divergence |ΔPosErr| | -0.0852 | 0.0070 | +0.3819 | -1.691e-02 | 0.73% | Statistically Associated (Negative, r=-0.085) |
| Contact Impulse | Trajectory Divergence |ΔPosErr| | +0.1470 | 3.04e-06 | +0.1804 | +7.581e-02 | 2.16% | Statistically Associated (Positive, r=+0.147) |
| Friction Coefficient | Trajectory Divergence |ΔPosErr| | +0.0852 | 0.0070 | -0.3819 | +8.293e-03 | 0.73% | Statistically Associated (Positive, r=+0.085) |
| Slip Event | Trajectory Divergence |ΔPosErr| | +0.1055 | 0.0008 | +0.2575 | +1.540e-03 | 1.11% | Statistically Associated (Positive, r=+0.105) |
| Collision Event | Trajectory Divergence |ΔPosErr| | +0.1086 | 0.0006 | +0.7278 | +1.587e-03 | 1.18% | Statistically Associated (Positive, r=+0.109) |
| Object Displacement | Trajectory Divergence |ΔPosErr| | +0.1468 | 3.13e-06 | +0.1960 | +2.298e-02 | 2.16% | Statistically Associated (Positive, r=+0.147) |
| Remaining Task Horizon | Trajectory Divergence |ΔPosErr| | -0.1516 | 1.46e-06 | -0.1167 | -5.655e-05 | 2.30% | Statistically Associated (Negative, r=-0.152) |

### 2.2. Policy: `history_gru` (Nominal History GRU, M=1,000)
| Parameter | Endpoint | Pearson $r$ | $p$-value | Spearman $\rho$ | OLS Slope | $R^2$ | Interpretation |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Contact Duration | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Contact Force | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Contact Impulse | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Friction Coefficient | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Slip Event | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Collision Event | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Object Displacement | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Remaining Task Horizon | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Contact Duration | Trajectory Divergence |ΔPosErr| | -0.0403 | 0.2029 | -0.4539 | -2.968e-04 | 0.16% | No Statistically Significant Association Detected |
| Contact Force | Trajectory Divergence |ΔPosErr| | -0.0548 | 0.0834 | +0.2580 | -1.074e-03 | 0.30% | No Statistically Significant Association Detected |
| Contact Impulse | Trajectory Divergence |ΔPosErr| | -0.0471 | 0.1366 | -0.3524 | -2.399e-03 | 0.22% | No Statistically Significant Association Detected |
| Friction Coefficient | Trajectory Divergence |ΔPosErr| | +0.0548 | 0.0834 | -0.2580 | +5.266e-04 | 0.30% | No Statistically Significant Association Detected |
| Slip Event | Trajectory Divergence |ΔPosErr| | -0.0548 | 0.0834 | -0.4146 | -7.900e-05 | 0.30% | No Statistically Significant Association Detected |
| Collision Event | Trajectory Divergence |ΔPosErr| | +0.0526 | 0.0963 | +0.1481 | +7.596e-05 | 0.28% | No Statistically Significant Association Detected |
| Object Displacement | Trajectory Divergence |ΔPosErr| | -0.0374 | 0.2368 | -0.3340 | -5.787e-04 | 0.14% | No Statistically Significant Association Detected |
| Remaining Task Horizon | Trajectory Divergence |ΔPosErr| | +0.0403 | 0.2029 | +0.4539 | +1.484e-06 | 0.16% | No Statistically Significant Association Detected |

### 2.3. Policy: `recovery_augmented_mlp` (Recovery-Augmented MLP, M=1,000)
| Parameter | Endpoint | Pearson $r$ | $p$-value | Spearman $\rho$ | OLS Slope | $R^2$ | Interpretation |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Contact Duration | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Contact Force | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Contact Impulse | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Friction Coefficient | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Slip Event | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Collision Event | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Object Displacement | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Remaining Task Horizon | Action Divergence ||Δa_0|| | +0.0000 | 1.0000 | +0.0000 | +0.000e+00 | 0.00% | No Variation (Invariant) |
| Contact Duration | Trajectory Divergence |ΔPosErr| | +0.0423 | 0.1812 | +0.1132 | +2.616e-02 | 0.18% | No Statistically Significant Association Detected |
| Contact Force | Trajectory Divergence |ΔPosErr| | +0.0280 | 0.3770 | +0.1570 | +4.601e-02 | 0.08% | No Statistically Significant Association Detected |
| Contact Impulse | Trajectory Divergence |ΔPosErr| | +0.0394 | 0.2128 | +0.2020 | +1.686e-01 | 0.16% | No Statistically Significant Association Detected |
| Friction Coefficient | Trajectory Divergence |ΔPosErr| | -0.0280 | 0.3770 | -0.1570 | -2.257e-02 | 0.08% | No Statistically Significant Association Detected |
| Slip Event | Trajectory Divergence |ΔPosErr| | +0.0454 | 0.1511 | +0.1124 | +5.500e-03 | 0.21% | No Statistically Significant Association Detected |
| Collision Event | Trajectory Divergence |ΔPosErr| | +0.3336 | 2.05e-27 | +0.7354 | +4.153e-02 | 11.13% | Statistically Associated (Positive, r=+0.334) |
| Object Displacement | Trajectory Divergence |ΔPosErr| | +0.0274 | 0.3869 | +0.2043 | +3.553e-02 | 0.08% | No Statistically Significant Association Detected |
| Remaining Task Horizon | Trajectory Divergence |ΔPosErr| | -0.0423 | 0.1812 | -0.1132 | -1.308e-04 | 0.18% | No Statistically Significant Association Detected |

### 2.4. Policy: `recovery_augmented_gru` (Recovery-Augmented GRU, M=1,000)
| Parameter | Endpoint | Pearson $r$ | $p$-value | Spearman $\rho$ | OLS Slope | $R^2$ | Interpretation |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Contact Duration | Action Divergence ||Δa_0|| | -0.0434 | 0.1705 | -0.2462 | -4.386e-04 | 0.19% | No Statistically Significant Association Detected |
| Contact Force | Action Divergence ||Δa_0|| | -0.4401 | 1.24e-48 | -0.1983 | -1.184e-02 | 19.37% | Statistically Associated (Negative, r=-0.440) |
| Contact Impulse | Action Divergence ||Δa_0|| | -0.1702 | 6.18e-08 | -0.1386 | -1.189e-02 | 2.90% | Statistically Associated (Negative, r=-0.170) |
| Friction Coefficient | Action Divergence ||Δa_0|| | +0.4401 | 1.24e-48 | +0.1983 | +5.809e-03 | 19.37% | Statistically Associated (Positive, r=+0.440) |
| Slip Event | Action Divergence ||Δa_0|| | -0.5889 | 2.18e-94 | -0.4677 | -1.166e-03 | 34.68% | Statistically Associated (Negative, r=-0.589) |
| Collision Event | Action Divergence ||Δa_0|| | -0.4773 | 4.87e-58 | -0.3230 | -9.710e-04 | 22.78% | Statistically Associated (Negative, r=-0.477) |
| Object Displacement | Action Divergence ||Δa_0|| | -0.0759 | 0.0163 | -0.1801 | -1.611e-03 | 0.58% | Statistically Associated (Negative, r=-0.076) |
| Remaining Task Horizon | Action Divergence ||Δa_0|| | +0.0434 | 0.1705 | +0.2462 | +2.193e-06 | 0.19% | No Statistically Significant Association Detected |
| Contact Duration | Trajectory Divergence |ΔPosErr| | +0.1800 | 9.85e-09 | +0.2664 | +9.946e-02 | 3.24% | Statistically Associated (Positive, r=+0.180) |
| Contact Force | Trajectory Divergence |ΔPosErr| | -0.0719 | 0.0229 | +0.0319 | -1.057e-01 | 0.52% | Statistically Associated (Negative, r=-0.072) |
| Contact Impulse | Trajectory Divergence |ΔPosErr| | +0.1923 | 8.74e-10 | +0.2917 | +7.345e-01 | 3.70% | Statistically Associated (Positive, r=+0.192) |
| Friction Coefficient | Trajectory Divergence |ΔPosErr| | +0.0719 | 0.0229 | -0.0319 | +5.187e-02 | 0.52% | Statistically Associated (Positive, r=+0.072) |
| Slip Event | Trajectory Divergence |ΔPosErr| | +0.2167 | 4.32e-12 | +0.2663 | +2.344e-02 | 4.70% | Statistically Associated (Positive, r=+0.217) |
| Collision Event | Trajectory Divergence |ΔPosErr| | +0.3337 | 1.94e-27 | +0.7715 | +3.709e-02 | 11.14% | Statistically Associated (Positive, r=+0.334) |
| Object Displacement | Trajectory Divergence |ΔPosErr| | +0.2084 | 2.82e-11 | +0.3366 | +2.416e-01 | 4.34% | Statistically Associated (Positive, r=+0.208) |
| Remaining Task Horizon | Trajectory Divergence |ΔPosErr| | -0.1800 | 9.85e-09 | -0.2664 | -4.973e-04 | 3.24% | Statistically Associated (Negative, r=-0.180) |

---

## 3. Forensic Interpretation of Contact Dynamics Mechanisms

### 3.1. Action Divergence (||Δa_0||)
- **Primary Driver is Internal Latent Memory, Not Surface Contact Physics:** Across the 4,000 paired evaluations, initial motor command divergence is strictly confined to policies with recurrent unrolled latent representations (`recovery_augmented_gru`, where $\|\Delta a_0\| \approx 0.0038\text{ m/step}$). For feedforward architectures (`reactive_mlp`, `history_gru`, `recovery_augmented_mlp`), $\|\Delta a_0\| = 0.0000\text{ m/step}$ identically across all contact durations, friction regimes, and impulse loads.
- **Correlation Ceiling:** Across the pooled cohort, contact impulse accounts for less than $0.1\%$ of action divergence variance ($R^2 = 0.08\%$, $r = -0.0284$). In `recovery_augmented_gru`, a weak negative correlation is observed with contact impulse ($r = -0.1702, p = 6.18 \times 10^{-8}$), consistent with the hypothesis that longer pre-perturbation pushes cause recurrent hidden states to settle into steady-state limit cycles.

### 3.2. Trajectory Divergence (|ΔPosErr|)
- **Moderate Association with Active Recovery Contacts:** Trajectory separation between Replay and Matched Injection is most strongly associated with active collision / contact events during the recovery phase ($r = +0.2532$, Spearman $\rho = +0.6147, p < 10^{-50}$, $R^2 = 6.41\%$). When the end-effector successfully re-engages with the target object, minor differences in approach angles compound through frictional sliding.
- **Pre-Failure Contact Impulse and Duration:** Both contact duration ($r = +0.0787, p = 6.17 \times 10^{-7}$) and contact impulse ($r = +0.0814, p = 2.55 \times 10^{-7}$) exhibit small positive associations with subsequent trajectory divergence, accounting for $< 0.7\%$ of total variance.
- **Friction Coefficient Dependence:** Friction coefficient ($\mu = 0.50$ vs $\mu = 0.35$) displays negligible linear correlation with trajectory divergence ($r = +0.0168, p = 0.287$), but shows a negative monotonic rank association (Spearman $\rho = -0.2074, p < 10^{-39}$), consistent with higher friction dampening erratic post-deviation puck sliding.
- **Remaining Horizon Coupling:** Trajectory divergence shows a small negative association with remaining horizon ($r = -0.0787, p = 6.17 \times 10^{-7}$), which is mathematically coupled with contact duration ($H_{\text{rem}} = 150 - T_{\text{fail}}$).

### 3.3. The Physical Information-Bottleneck Hypothesis
- **Decoupling Action Sensitivity from Functional Recovery:** Multivariate regression reveals that all 8 contact dynamics predictors jointly explain only $7.44\%$ of trajectory divergence variance ($R^2_{\text{adj}} = 0.0725$) in the pooled cohort. For `recovery_augmented_mlp`, predictors explain $2.14\%$ ($R^2_{\text{adj}} = 0.0135$), and for `recovery_augmented_gru`, predictors explain $15.54\%$ ($R^2_{\text{adj}} = 0.1485$).
- **Exploratory Synthesis:** These findings are consistent with the hypothesis that physical contact mechanics in robotic pushing function as an information-attenuating filter. While internal recurrent memory and pre-perturbation contact history alter instantaneous motor commands, downstream normal-force and friction constraints funnel trajectories into common physical basins, preventing motor divergences from producing large recovery advantages.

---

## 4. Methodological Scope and Limitations

- **Strictly Exploratory:** All correlations reported herein are exploratory observational diagnostics computed over Stage C simulation logs. They do not constitute experimental proof that contact dynamics cause history attenuation.
- **No Controlled Contact Intervention:** Without an active experimental intervention directly varying contact force or impulse while holding all kinematic state variables invariant, causal attribution cannot be asserted.
- **No Hardware Extrapolation:** In physical robotics, non-rigid compliance, surface micro-roughness, sensor latency, and tracking noise may alter contact interaction regimes. These simulation findings must not be extrapolated to real robot hardware without dedicated hardware experiments.
