# IEEE RA-L Page Budget & Content Allocation

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/submission/venues/ra_l/ra_l_page_budget.md`  
**Milestone:** Phase 30 — RA-L Format Adaptation Planning  
**Target Venue:** IEEE Robotics and Automation Letters (RA-L)  
**Date:** 2026-11-10  
**Status:** `Planned` | `Draft`  

---

## 1. Executive Page Budget Overview

IEEE Robotics and Automation Letters (RA-L) enforces a strict length policy:
- **Base Page Limit:** **6 pages** (standard publication fee).
- **Maximum Permitted Overlength:** **2 additional pages** (total **8 pages**, incurring $175/page mandatory overlength fee).
- **Target Manuscript Length:** **8.0 pages** (maximally utilizing the 8-page allowable envelope to thoroughly present the matched-state protocol, empirical results, and physical contact attenuation mechanism without truncating scientific content).

---

## 2. Condensed Abstract Draft ($\le 200$ Words)

The original 250-word abstract is condensed to **182 words** to comply strictly with the RA-L 200-word limit while preserving all essential empirical elements:

> **Abstract**—Policy recovery from execution-induced failures is frequently assumed to require temporal history. However, evaluating history dependence by comparing reactive and recurrent policies conflates history access with state divergence following a failure. We introduce a paired replay-injection evaluation that isolates the causal effect of history by initializing policies at identical physical states ($D \le 10^{-10}\text{ m}$) under matched failure conditions across planar manipulation tasks in MuJoCo. In a confirmatory benchmark of 20,000 rollouts across 200 matched scenarios, recovery-augmented recurrent policies exhibit substantial motor action divergence ($\|\Delta a_0\| = 0.0038\text{ m/step}$, Cohen's $d = 3.99$, $p < 10^{-15}$) and transient trajectory separation ($2.48\text{ cm}$) upon failure. However, binary recovery success exhibits no statistically significant causal-history advantage after Holm-Bonferroni correction ($p_\text{adj} \ge 0.2500$ across all policies; negative control discordance $= 0/200$, 95% CI $[0.00\%, 1.83\%]$). Physical contact analysis reveals that normal contact forces and Coulomb friction act as an information-destroying bottleneck, attenuating recurrent divergence prior to terminal goal dwell ($p_\text{adj} = 1.0000$). These simulation-based findings indicate that history benefits depend heavily on contact damping dynamics.

*Word count: 182 words (Complies with RA-L $\le 200$ word rule).*

---

## 3. Page-by-Page Allocation Matrix (8 Pages Total)

| Page | Columns | Target Sections | Visual Elements | Estimated Word Count | Target Content |
|---|---|---|---|---|---|
| **Page 1** | Two-column | Title Block, Abstract, Index Terms, Sec I (Introduction) | None | ~650 words | Paper title, single-blind author block, 182-word abstract, 5 IEEE index terms, research motivation, state-history confounding problem. |
| **Page 2** | Two-column | Sec I (Contributions), Sec II (Related Work), Sec III (Problem Formulation) | None | ~850 words | 4 formal contributions, literature analysis (RoboRecover, LIBERO-Recover), POMDP recovery formulation, counterfactual objectives. |
| **Page 3** | Two-column | Sec III (Matched-State Evaluation Protocol) | **Fig. 1** (Full-width 2-column or 1-column Method Pipeline) | ~600 words | Paired Replay-Injection protocol, Conditions B0–B4, state snapshot restoration exactness ($D \le 10^{-10}\text{ m}$), action divergence metric $\|\Delta a_0\|$. |
| **Page 4** | Two-column | Sec IV (Experimental Setup & Benchmark Suite) | **Fig. 2** (1-column Failure Deviation & State Matching) | ~700 words | Environments (`PushTargetEnv`, `SecondPushTaskEnv`), failure mechanisms (off-center slip, contact loss), 4 policy architectures, privileged oracle admissibility. |
| **Page 5** | Two-column | Sec V (Confirmatory Benchmark Results: Binary Analysis) | **Table I** (2-column Confirmatory Recovery Success), **Fig. 3** (1-column Recovery by Policy) | ~550 words | Primary binary recovery analysis ($N=200$, 20,000 rollouts), Holm-Bonferroni corrected McNemar tests ($p_\text{adj} \ge 0.2500$), negative control validation (0/200 discordance). |
| **Page 6** | Two-column | Sec V (Confirmatory Results: Continuous Divergence) | **Table II** (1-column Continuous Goal Error), **Fig. 4** (1-column Trajectory Divergence vs Physical Damping) | ~600 words | Initial action divergence ($d=3.99$), intermediate path separation ($2.48\text{ cm}$), terminal goal error equivalence ($p_\text{adj} = 1.0000$), Wilcoxon rank-sum tests. |
| **Page 7** | Two-column | Sec VI (Physical Mechanism & Discussion) | **Fig. 5** (1-column Contact Force Decoupling & Friction Dynamics) | ~800 words | 5-tier causal chain, normal contact force damping, Coulomb friction surface dissipation, information-destroying bottleneck, capability bounds of nominal vs recovery policies. |
| **Page 8** | Two-column | Sec VII (Limitations & Future Roadmap), Sec VIII (References) | None | ~450 words + 17 references | Explicit simulation bounds (MuJoCo planar manipulation), Franka Panda hardware blueprint roadmap, 17 verified references in standard IEEE style. |

---

## 4. Total Budget Aggregation

- **Total Estimated Words:** ~5,250 words of body prose.
- **Total Display Figures:** 5 carefully selected, high-impact composite figures (1 method pipeline, 1 state-matching geometry, 2 benchmark outcome figures, 1 physical contact mechanism figure).
- **Total Display Tables:** 2 compact IEEE-style tables (Table I: Primary Recovery Success Rates; Table II: Continuous Divergence & Attenuation Metrics).
- **Total References:** 17 verified citations typeset in standard IEEE two-column bibliography style.
- **Net Page Count:** **8.0 pages** (inclusive of figures, tables, and bibliography).

