# IEEE RA-L Adaptation Plan

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/submission/venues/ra_l/ra_l_adaptation_plan.md`  
**Milestone:** Phase 30 — RA-L Format Adaptation Planning  
**Target Venue:** IEEE Robotics and Automation Letters (RA-L)  
**Date:** 2026-11-10  
**Status:** `Planned` | `Draft`  

---

## 1. Executive Charter & Scientific Invariance

This plan details the formal adaptation of the existing completed manuscript (`docs/manuscript/draft/manuscript.md`) and release package (`release/`) for submission to **IEEE Robotics and Automation Letters (RA-L)**.

### Strict Scientific Invariance Directives:
- **No Scientific Drift:** The underlying research design, paired replay-injection matching protocol ($D \le 10^{-10}\text{ m}$), simulation environment (`PushTargetEnv`, `SecondPushTaskEnv`), evaluation policies, statistical analysis (McNemar, Holm-Bonferroni, Wilcoxon), empirical numbers, and conclusions remain strictly unchanged.
- **No Claim Escalation:** No claims of novelty, Q1 publication readiness, real-robot hardware validation, or universal generalization beyond the tested simulation conditions.
- **No Premature Readiness Claims:** The manuscript is not claimed to be submission-ready until the RA-L formatted PDF is compiled and all venue-specific checks are verified.
- **No External Upload:** No transmission to PaperPlaza or any external server will occur without explicit user review and approval.

---

## 2. Verified IEEE RA-L Venue Constraints

| Parameter | Verified RA-L Requirement | Existing Manuscript State | Adaptation Strategy |
|---|---|---|---|
| **Submission Model** | Open year-round (continuous submission window) | Staged for periodic conference deadlines | Leverage continuous ingestion; no seasonal deadline pressure |
| **Review Model** | Single-blind review (author identities disclosed on title page) | Double-blind (anonymized, no author names/affiliations) | Re-insert formal author block: names, affiliations, addresses, emails, corresponding author footnote |
| **Manuscript Format** | IEEE RAS conference template (two-column, 10pt font) | Single-column markdown / preprint format | Typeset in LaTeX using `IEEEtran.cls` / RAS conference format |
| **Page Length** | 6 pages base; up to 2 extra pages allowed (max 8 pages total with fee) | ~8.2 pages of single-column text + references + appendices | Condense prose, compact figures/tables to fit strictly within 8 pages |
| **Abstract Limit** | Maximum 200 words | Exactly 250 words | Condense by 50 words while preserving problem, method, findings, and limits |
| **Supplemental Text** | Supplemental text or figures as multimedia are strictly forbidden | 13 standalone appendices (`supplementary_materials.md`) | Offload detailed appendices to public Zenodo repository; retain essential proofs in main text |
| **Multimedia Zip** | Single ZIP archive, maximum 50 MB, containing `ReadMe.txt` and `Summary.txt` | Multiple standalone folders (`release/`, `data/`) | Package release code, benchmark datasets, and demo video into single $\le 50\text{ MB}$ zip |
| **Review Timeline** | Rapid peer review: 6-month rule to final publication or rejection | Standard conference review timeline | Align post-submission monitoring with RA-L 6-month lifecycle |
| **Author Credentials**| PaperPlaza account + ORCID required for all authors | Local staging placeholders | Identify author credentials requirement for user provisioning |

---

## 3. Structural Adaptation Roadmap

```
+-----------------------------------------------------------------------------------+
|                           CURRENT MANUSCRIPT ARCHITECTURE                          |
|  - 21 Markdown Sections (~42.9 KB source text, ~8.2 pages single column)           |
|  - 250-word abstract                                                              |
|  - 14 Standalone Figures (PDF/PNG)                                                |
|  - 7 Full-size Tables                                                             |
|  - 13 Standalone Appendices (S1-S13, 16.4 KB text)                                |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        ADAPTED IEEE RA-L 8-PAGE ARCHITECTURE                      |
|                                                                                   |
|  Page 1: Title, Authors, Affiliations, Abstract (<= 200 words), Sec I (Intro)     |
|  Page 2: Sec II (Related Work & State-History Confounding), Sec III (Methodology) |
|  Page 3: Sec III (Matched-State Formulation, Delta a_0 Divergence Mechanism)      |
|  Page 4: Sec IV (Experimental Setup: 4 Policies, Push Tasks, Failure Models)      |
|  Page 5: Sec V (Confirmatory Benchmark Results: Binary Parity, p_adj >= 0.25)     |
|  Page 6: Sec V (Continuous Attenuation: d=3.99 to p_adj=1.0000, 2-Column Table)   |
|  Page 7: Sec VI (Physical Mechanism & Contact Attenuation Discussion)             |
|  Page 8: Sec VII (Limitations, Simulation Bounds, Future Work) & References (IEEE) |
+-----------------------------------------------------------------------------------+
```

---

## 4. Work Breakdown for Format Adaptation

1. **Phase 30.1: Page Budget Formulation:** Establish precise line, word, figure, and table allocations per page in `ra_l_page_budget.md`.
2. **Phase 30.2: Abstract & Title Block Condensation:** Formulate the $\le 200$-word abstract and the single-blind author/affiliation title block.
3. **Phase 30.3: Figure & Table Rationalization:** Select high-impact composite figures and compact tables suitable for two-column presentation.
4. **Phase 30.4: Supplementary & Multimedia Packaging:** Establish `ra_l_supplementary_plan.md` and `ra_l_multimedia_plan.md` complying with the 50 MB single-zip rule, including `ReadMe.txt` and `Summary.txt`.
5. **Phase 30.5: Account & ORCID Registration Checklist:** Document PaperPlaza registration steps and ORCID requirements in `ra_l_account_and_orcid_requirements.md`.
6. **Phase 30.6: Comprehensive Audit & Reporting:** Audit against all RA-L author guidelines and author `phase_30_ra_l_adaptation_report.md`.

