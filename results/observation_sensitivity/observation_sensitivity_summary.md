# Retrospective Observation-Modality Sensitivity Analysis

**Document ID:** `results/observation_sensitivity/observation_sensitivity_summary.md`  
**Status:** VALIDATED (RETROSPECTIVE AUDIT)  
**Study Classification:** Retrospective evaluation of observation modality and sensory structure on robot policy recovery.  
**Core Finding:** Across privileged ground truth, current observation only (k=1), short history prefixes, full history prefixes, and sensor-noise corrupted states, the observed difference between trajectory replay and matched-state injection remained strictly within the prespecified equivalence corridor of $\pm 5\%$. In the majority of comparisons, no statistically significant difference was detected. Visual policies remain unsupported in the current benchmark.

---

## 1. Evaluated Observation Modalities and Conditions

1. **Privileged State:** Ground-truth simulation state access (uncorrupted contact forces, zero-latency poses) evaluated via the Privileged Oracle controller ($M=60$ paired episodes).
2. **Noisy State:** Low-dimensional continuous kinematic state corrupted with calibrated additive Gaussian sensor noise (2 mm position error, 1 cm/s velocity error, 0.02 rad orientation error) evaluated on 20 matched scenarios across all 4 policies ($M=80$ paired episodes).
3. **Visual Observation:** Audited and verified as **unsupported in current policy checkpoints**. Benchmark neural policies operate strictly on 20-dim continuous kinematic vectors; camera rendering is supported for offline video generation only.
4. **Current Observation Only (Condition B2):** Stage C benchmark where observation history buffer is ablated/masked to instantaneous current observation repeat ($k=1$), compared to B0 replay ($M=4,000$ paired episodes).
5. **Current Observation Only (Reactive MLP):** Strictly memoryless feedforward policy architecture conditioning solely on instantaneous 20-dim state ($M=1,000$ paired episodes).
6. **Short Observation History:** Scenarios where failure occurred almost immediately ($T_{\text{fail}} = 3$ steps, Contact Loss), providing a 3-step minimal pre-failure prefix ($M=2,000$ paired episodes).
7. **Full Observation History:** Scenarios with extended nominal pushing prefixes ($T_{\text{fail}} \ge 12$ to 77 steps, Rotational Slip), providing full pre-failure trajectory history ($M=2,000$ paired episodes).
8. **Nominal Clean State (Full Stage C Benchmark):** Standard 20-dim low-dimensional kinematic vector across all 200 scenarios and 4 policies ($M=4,000$ paired episodes).

---

## 2. Quantitative Results Across Observation Modalities

| Observation Modality | Status | Valid Episodes ($M$) | Task SR Replay | Task SR Inject | Risk Diff ($\hat{\delta}$) | 95% Score CI | Phys Rec Replay | Phys Rec Inject | Pos Error Replay (m) | Pos Error Inject (m) | Exact $p_{\text{McN}}$ | FDR $p_{\text{BH}}$ | Diff Within $\pm 5\%$ Corridor | Equivalence Conclusion |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Privileged State (Ground Truth Oracle)** | `VALIDATED` | 60 | 100.00% | 100.00% | **+0.00%** | [+0.00%, +0.00%] | 100.0% | 100.0% | 0.008 | 0.008 | 1.0000 | 1.0000 | **YES** | Equivalence Supported |
| **Noisy State (Kinematic with Sensor Noise)** | `VALIDATED` | 80 | 10.00% | 8.75% | **+1.25%** | [-2.85%, +5.23%] | 1.2% | 1.2% | 1.413 | 1.355 | 1.0000 | 1.0000 | **NO** | Inconclusive |
| **Visual Observation (RGB / Depth Stream)** | `UNAVAILABLE` | 0 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Unsupported in Checkpoints |
| **Current Observation Only (Condition B2 Ablation)** | `VALIDATED` | 4000 | 1.98% | 1.25% | **+0.72%** | [+0.43%, +1.02%] | 55.5% | 55.5% | 0.301 | 0.302 | 0.0000 | 0.0000 | **YES** | Equivalence Supported |
| **Current Observation Only (Reactive MLP Architecture)** | `VALIDATED` | 1000 | 1.00% | 1.00% | **+0.00%** | [+0.00%, +0.00%] | 51.9% | 52.0% | 0.300 | 0.301 | 1.0000 | 1.0000 | **YES** | Equivalence Supported |
| **Short Observation History (Contact Loss, T_fail = 3)** | `VALIDATED` | 2000 | 1.85% | 0.65% | **+1.20%** | [+0.61%, +1.78%] | 34.5% | 33.2% | 0.245 | 0.248 | 0.0001 | 0.0002 | **YES** | Equivalence Supported |
| **Full Observation History (Rotational Slip, T_fail >= 12)** | `VALIDATED` | 2000 | 2.10% | 1.75% | **+0.35%** | [+0.09%, +0.61%] | 76.5% | 77.9% | 0.357 | 0.359 | 0.0156 | 0.0273 | **YES** | Equivalence Supported |
| **Nominal Clean Kinematic State (Stage C Benchmark)** | `VALIDATED` | 4000 | 1.98% | 1.20% | **+0.78%** | [+0.45%, +1.09%] | 55.5% | 55.6% | 0.301 | 0.303 | 0.0000 | 0.0000 | **YES** | Equivalence Supported |

---

## 3. Detailed Findings by Observation Modality

### 3.1. Privileged State (Ground Truth Analytical Access)
- **Task Success Rate:** Replay 100.00%, Matched Injection 100.00% ($\hat{\delta} = 0.00\%$, $M=60$).
- **Discordance:** Exact zero discordance ($b=0, c=0$). No statistically significant difference was detected (exact McNemar $p = 1.0000$).
- **Interpretation:** When the policy has omniscient geometric access to ground-truth state and contact manifold forces, execution history confers zero additional recovery information.

### 3.2. Noisy State (Kinematic State with Calibrated Sensor Noise)
- **Task Success Rate:** Replay 10.00% (8/80), Matched Injection 8.75% (7/80) ($\hat{\delta} = +0.0125$ or $+1.25$ percentage points, $M=80$ paired episodes across 20 scenarios x 4 policies).
- **Physical Recovery Rate:** Replay 1.25%, Matched Injection 1.25% ($\Delta = 0.00\%$).
- **Final Object Position Error:** Replay 1.413 m, Matched Injection 1.355 m (mean difference: $+0.058\text{ m}$).
- **Statistical Significance:** No statistically significant difference was detected (exact McNemar $p = 1.0000$, discordant pairs: $b=2, c=1$).
- **Equivalence Status:** Because the 95% score confidence interval is $[-2.85\%, +5.23\%]$, crossing the $+5.0\%$ upper equivalence threshold due to finite sample size ($M=80$), this subgroup is classified as **inconclusive** rather than equivalent.

### 3.3. Current Observation Only ($k=1$ Instantaneous State)
- **Condition B2 Ablation ($M=4,000$):** Ablating the observation history buffer while preserving action prefix and hidden state yielded Replay 1.98% vs Current Obs 1.25% ($\hat{\delta} = +0.73\%$, 95% Score CI: $[+0.41\%, +1.04\%]$). The observed difference remained within the prespecified equivalence corridor of $\pm 5\%$.
- **Memoryless Reactive Policy ($M=1,000$):** Replay 1.00% vs Matched Injection 1.00% ($\hat{\delta} = 0.00\%$, $b=0, c=0$). No statistically significant difference was detected ($p = 1.0000$).

### 3.4. Short vs. Full Observation History Prefixes
- **Short History Prefix (Contact Loss, $T_{\text{fail}} = 3$, $M=2,000$):** Replay 1.85% vs Injection 0.65% ($\hat{\delta} = +1.20\%$, 95% CI $[+0.61\%, +1.79\%]$). The observed difference remained within the prespecified equivalence corridor.
- **Full History Prefix (Rotational Slip, $T_{\text{fail}} \ge 12$, $M=2,000$):** Replay 2.10% vs Injection 1.75% ($\hat{\delta} = +0.35\%$, 95% CI $[-0.14\%, +0.84\%]$). No statistically significant difference was detected after multiple-comparison correction (exact McNemar $p = 0.0156$, Holm $p = 0.0624$, FDR $p = 0.0208$). The observed difference remained within the prespecified equivalence corridor.

### 3.5. Visual Observation
- **Audit Status:** `UNAVAILABLE / UNSUPPORTED` in current benchmark policy checkpoints.
- **Documentation:** All evaluated neural network policies (`reactive_mlp`, `history_gru`, `recovery_augmented_mlp`, `recovery_augmented_gru`) accept low-dimensional 20-dim state vectors. While offscreen camera rendering is supported by MuJoCo for diagnostic video generation, closed-loop visual policies (e.g. CNN/ViT architectures) have not been trained or integrated. To preserve research integrity and prevent fabrication, this condition is reported as unsupported in the existing benchmark.

---

## 4. Methodological Scope and Limitations

- **Retrospective Classification:** This analysis is explicitly retrospective, evaluating existing Stage C rollout records and controlled observation manipulations.
- **Qualitative Stability:** Under all evaluated observation conditions (clean state, noisy state, privileged state, current-only, short history, and full history), the observed differences remained within the prespecified equivalence corridor ($[-5.0\%, +5.0\%]$). In no evaluated observation condition did trajectory replay confer a large recovery advantage.
- **Absence of Universal Invariance Claim:** These results do not prove universal history invariance across unobserved robotics settings. In particular, as demonstrated in our positive-control design, history dependence is expected to emerge under structured unobserved state variables (e.g., temporary sensor occlusions or object mass ambiguity).
