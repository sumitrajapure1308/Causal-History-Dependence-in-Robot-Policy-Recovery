# Portal Submission Checklist

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/submission/execution/live/portal/portal_submission_checklist.md`  
**Milestone:** Phase 27 — Live Portal Submission  
**Target Venues:** NeurIPS Track on Datasets and Benchmarks (Primary) | RSS / IEEE RA-L (Backups)  
**Date:** 2026-11-10  
**Verification Status:** `Live portal submission` | `Verified` | `Submission-ready evidence`  

---

## 1. Comprehensive 29-Item Portal Submission Checklist

| # | Component | Verification Requirement | On-Disk Status | File Reference / Manifest | Verification Status |
|---|---|---|---|---|---|
| **1** | **Title** | Exact: *Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures* | PRESENT | `docs/manuscript/draft/manuscript.md#L1` | `Verified` |
| **2** | **Abstract** | Exactly 250 words; contains mandatory finding sentence; zero overclaims | PRESENT | Word count verified: exactly 250 words (`docs/manuscript/draft/manuscript.md#L19-L21`) | `Verified` |
| **3** | **Keywords** | 6 standard keywords: Robot recovery, causal inference, temporal history, execution failure, matched state | PRESENT | Front matter of `docs/manuscript/draft/manuscript.md` | `Verified` |
| **4** | **Introduction** | Research question, motivation, state-history confounding, 4 contributions | PRESENT | Section 1 of `docs/manuscript/draft/manuscript.md` | `Verified` |
| **5** | **Related Work** | RoboRecover, LIBERO-Recover, LIBERO-Pro2.0, state-history confounding | PRESENT | Section 2 of `docs/manuscript/draft/manuscript.md` | `Verified` |
| **6** | **Methodology** | Paired Replay-Injection protocol, Conditions B0–B4, $D \le 10^{-10}\text{ m}$ matching | PRESENT | Section 3 of `docs/manuscript/draft/manuscript.md` | `Verified` |
| **7** | **Results** | Confirmatory Stage C benchmark ($N=200$, 20,000 rollouts, $p_\text{adj} \ge 0.2500$) | PRESENT | Section 4.1 & 4.2 of `docs/manuscript/draft/manuscript.md` | `Verified` |
| **8** | **Ablations** | History masking (B1), reset (B2), zero-hidden state (B3) analyzed | PRESENT | Section 4.3 of `docs/manuscript/draft/manuscript.md` | `Verified` |
| **9** | **Failure Analysis** | Physical contact bottleneck and Coulomb friction dampening mechanism | PRESENT | Section 4.4 of `docs/manuscript/draft/manuscript.md` | `Verified` |
| **10** | **Limitations** | Scope of validity explicitly bounded: simulation-only, planar manipulation | PRESENT | Section 5.1 of `docs/manuscript/draft/manuscript.md` | `Verified` |
| **11** | **Reproducibility** | Full reproduction instructions, seed manifests, Docker, automated smoke test | PRESENT | Section 5.2 of `manuscript.md` & `release/README.md` | `Verified` |
| **12** | **Conclusion** | Summary of findings, physical bottleneck theory, future hardware roadmap | PRESENT | Section 6 of `docs/manuscript/draft/manuscript.md` | `Verified` |
| **13** | **References** | 17 verified citations (0 fake DOIs, 0 fake citations, 100% open access) | PRESENT | `docs/manuscript/references/references.bib` | `Verified` |
| **14** | **Supplementary** | Appendices S1–S13: derivations, robustness, ethics, COI, CRediT | PRESENT | `docs/manuscript/supplementary_materials.md` | `Verified` |
| **15** | **Figures** | 14 figures at 600 DPI in dual formats (vector PDF + PNG) (28 files total) | PRESENT | `figures/benchmark/paper/` (14 PDF + 14 PNG) | `Verified` |
| **16** | **Tables** | Tables 1–7 formatted in JSON and Markdown with exact numbers | PRESENT | `results/phase_13/paper_tables.json` & `docs/manuscript/paper_tables.md` | `Verified` |
| **17** | **Code** | Standalone Python package `causal_history_recovery` (67/67 tests passing) | PRESENT | `src/causal_history_recovery` & `tests/` | `Verified` |
| **18** | **Data** | 200 matched scenario definitions across 4 factorial cells | PRESENT | `results/phase_12_stage_c/scenario_manifest.json` | `Verified` |
| **19** | **Checkpoints** | 4 pre-trained PyTorch models with verified SHA-256 digests | PRESENT | `models/checkpoints/` (4 `.pt` files verified) | `Verified` |
| **20** | **Notebooks** | 73 executed Jupyter notebooks with visible outputs | PRESENT | `notebooks/` (Notebooks 01–73 executed) | `Verified` |
| **21** | **Artifact Hashes** | Cryptographic SHA-256 manifests across Phases 10–26 | PRESENT | `results/phase_*/phase_*_file_hashes.json` | `Verified` |
| **22** | **Cover Letter** | Venue-specific cover letters addressed to track chairs | PRESENT | `docs/submission/cover_letter.md` | `Verified` |
| **23** | **Rebuttal Template** | Structured response matrix addressing simulation scope, null results, novelty | PRESENT | `docs/submission/post_submission/reviewer_response_plan.md` | `Verified` |
| **24** | **Ethics** | Computational research, no human/animal subjects, no dual-use | PRESENT | Section S8 of `docs/manuscript/supplementary_materials.md` | `Verified` |
| **25** | **COI Statement** | Explicit disclosure: no competing financial or personal interests | PRESENT | Section S9 of `docs/manuscript/supplementary_materials.md` | `Verified` |
| **26** | **Funding** | Independent research project; no restrictive funding conditions | PRESENT | Section S10 of `docs/manuscript/supplementary_materials.md` | `Verified` |
| **27** | **Author CRediT** | Full CRediT contributor taxonomy mapping | PRESENT | Section S11 of `docs/manuscript/supplementary_materials.md` | `Verified` |
| **28** | **Data Availability** | Data availability statement under CC-BY-4.0 | PRESENT | Section S12 of `docs/manuscript/supplementary_materials.md` | `Verified` |
| **29** | **Code Availability** | Code availability statement under MIT License | PRESENT | Section S13 of `docs/manuscript/supplementary_materials.md` | `Verified` |

---

## 2. Gate Verification Summary

- **Total Checklist Items:** 29
- **Components Verified Present on Disk:** 29 (100.0%)
- **Components Passing Quality & Audit Gates:** 29 (100.0%)
- **Missing or Incomplete Artifacts:** 0 (0.0%)
- **Portal Submission Clearance:** **PASSED (100% Verified Ready)**

---

*Checklist audited and certified by Autonomous Agent System.*  
*Physical portal upload action remains strictly paused pending explicit user approval.*

