# IEEE RA-L Page Budget & Typesetting Allocation (Manuscript Package)

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/submission/venues/ra_l/manuscript/ra_l_page_budget.md`  
**Milestone:** Phase 31 — RA-L Manuscript Adaptation  
**Target Venue:** IEEE Robotics and Automation Letters (RA-L)  
**Date:** 2026-11-10  
**Verification Status:** `Verified` | `Submission-ready evidence`  

---

## 1. Verified Page Ceiling & Financial Constraints

- **Standard Base Limit:** **6 pages** (standard publication fee).
- **Maximum Permitted Overlength:** **2 additional pages** (total **8 pages**, incurring mandatory $175/page charge).
- **Enforced Page Count Target:** Exactly **8.0 pages** (maximally utilizing the allowable space to rigorously detail the matched-state protocol, empirical results, and physical contact attenuation mechanism).

---

## 2. Page-by-Page Architectural Layout

```
PAGE 1 (Columns 1 & 2):
├── Document Header & RA-L Publication Banner
├── Title Block: Single-Blind Authors, Affiliations, Emails, Footnotes
├── Abstract: Condensed 182-word text (<= 200 words)
├── Index Terms: 6 standardized IEEE keywords
└── Section I: Introduction (Motivation, State-History Confounding)

PAGE 2 (Columns 1 & 2):
├── Section I (cont.): Formal Research Questions & 4 Contributions
├── Section II: Related Work (RoboRecover, LIBERO-Recover, Policy Recovery)
└── Section III: Problem Formulation (POMDP Recovery Objective)

PAGE 3 (Columns 1 & 2):
├── Section III (cont.): Paired Replay-Injection Matching Protocol (D <= 1e-10 m)
├── Conditions B0 (Replay), B1 (Masked), B2 (Reset), B3 (Zero), B4 (Injection)
├── Fig. 1 (2-column width, 2.2 in height): Paired Replay-Injection Method Pipeline
└── Action Divergence Metric Formulation (||Delta a_0||)

PAGE 4 (Columns 1 & 2):
├── Section IV: Experimental Benchmark Suite & Environments
│   ├── PushTargetEnv & SecondPushTaskEnv (Kinematics, Friction, Dynamics)
│   ├── Failure Generation: Off-Center Slip & Premature Contact Loss
│   └── 4 Policy Architectures: Reactive MLP, History GRU, Rec-Aug MLP, Rec-Aug GRU
├── Privileged Oracle Controller & Recoverability Filter (R_oracle = 1)
└── Fig. 2 (1-column width, 2.0 in height): Failure Deviation & State Matching

PAGE 5 (Columns 1 & 2):
├── Section V: Confirmatory Benchmark Results
│   ├── Benchmark Scope: 20,000 Rollouts, 200 Scenarios across 4 Factorial Cells
│   ├── Table I (2-column width): Primary Recovery Success Rates & McNemar Tests
│   └── Primary Binary Outcome: Null Recovery Parity (p_adj >= 0.2500)
├── Negative Control Validation: Reactive MLP 0/200 Discordant (CI [0.00%, 1.83%])
└── Fig. 3 (1-column width, 2.0 in height): Binary Recovery Success by Architecture

PAGE 6 (Columns 1 & 2):
├── Section V (cont.): Continuous Divergence & Motor Action Dynamics
├── Table II (1-column width): Continuous Goal Error & Action Separation Metrics
├── Initial Recurrent Motor Divergence (||Delta a_0|| = 0.0038 m/step, d = 3.99, p < 1e-15)
├── Intermediate Object Separation (2.48 cm max divergence)
├── Terminal Goal Distance Attenuation (p_adj = 1.0000, Wilcoxon rank-sum)
└── Fig. 4 (1-column width, 2.0 in height): Continuous Action Divergence Dynamics

PAGE 7 (Columns 1 & 2):
├── Section VI: Discussion & Physical Attenuation Mechanism
│   ├── 5-Tier Causal Chain: Divergence -> Contact -> Slip -> Damping -> Dwell
│   ├── Normal Contact Forces & Coulomb Friction Information Bottleneck
│   ├── Capability Boundaries: Nominal vs Recovery-Augmented Architecture Collapse
│   └── Fig. 5 (1-column width, 2.2 in height): Contact Force Decoupling & Attenuation
└── Robustness across 14 Experimental Dimensions & Covariate Invariance

PAGE 8 (Columns 1 & 2):
├── Section VII: Limitations, Scope, and Hardware Roadmap
│   ├── Explicit Simulation Bounding: MuJoCo Planar Manipulation Scope
│   ├── Counterfactual Matching Constraint: D <= 1e-10 m Achievable only in Simulation
│   └── Physical Robot Roadmap: Franka Panda Cross-Embodiment Blueprint
├── End Matter: Code & Data Availability (Zenodo DOI), Ethical Compliance, CRediT
└── Section VIII: References (17 Verified IEEE Bibliographic Citations)
```

---

## 3. Quantitative Space Accounting

| Section / Element | Allocated Columns | Target Height / Space | Estimated Words / Equivalent |
|---|---|---|---|
| Title Block & Affiliations | 2 columns (Span) | 2.2 in | ~250 words equiv. |
| Abstract & Index Terms | 2 columns (Span) | 1.8 in | 182 words + 30 words |
| Section I (Introduction) | 1.8 columns | 8.5 in | ~750 words |
| Section II (Related Work) | 1.2 columns | 5.5 in | ~500 words |
| Section III (Problem & Protocol) | 2.5 columns | 11.5 in | ~1,050 words |
| Section IV (Experimental Setup) | 2.0 columns | 9.0 in | ~850 words |
| Section V (Benchmark Results) | 2.2 columns | 10.0 in | ~900 words |
| Section VI (Physical Mechanism) | 1.8 columns | 8.0 in | ~750 words |
| Section VII (Limitations & Scope) | 1.0 column | 4.5 in | ~400 words |
| Display Figures (5 figures) | Mixed (1 span, 4 single) | 10.6 in total | ~900 words equiv. |
| Display Tables (2 tables) | Mixed (1 span, 1 single) | 3.5 in total | ~350 words equiv. |
| References (17 entries) | 1.0 column | 4.5 in | 17 citations (~250 words) |
| **Total Manuscript Package** | **16 Column-Pages** | **70.6 in** | **8.0 Pages Exactly** |

