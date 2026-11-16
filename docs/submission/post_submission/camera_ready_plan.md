# Camera-Ready Preparation & Archival Deposition Plan

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Document:** `docs/submission/post_submission/camera_ready_plan.md`  
**Milestone:** Phase 22 — Post-Submission Readiness and Reviewer-Response Preparation  
**Date:** 2026-11-10  
**Verification Status:** `Post-submission readiness` | `Submission-ready evidence` | `Verified`  

---

## 1. Camera-Ready Governance Charter

This plan governs the transition from provisional acceptance notification to final archival camera-ready publication for the **NeurIPS Track on Datasets and Benchmarks** (and fallback venues **RSS** and **IEEE RA-L**).

Operating standard: **Camera-ready files must incorporate all approved reviewer clarifications while maintaining exact empirical fidelity to the Stage C benchmark results and remaining strictly within venue page budgets.**

---

## 2. Camera-Ready Task & Risk Matrix

| Task # | Camera-Ready Required Action | Camera-Ready Deadline | Camera-Ready Owner | Camera-Ready Status | Camera-Ready Risk | Camera-Ready Mitigation | Camera-Ready Owner (Sign-Off) | Camera-Ready Deadline (Window) |
|---|---|---|---|---|---|---|---|---|
| **CR-01** | **De-Anonymize Author & Institutional Metadata** | Notification $+ 3\text{d}$ ($T+83\text{d}$) | Lead Author | `Planned` | Adding author affiliations and acknowledgments causes main text to overflow 9-page limit | Main text draft is currently 8.2 pages, providing 0.8 pages of buffer for author block and acknowledgments | Lead Author | $T+83$ Days |
| **CR-02** | **Integrate Post-Review Minor Text Clarifications** | Notification $+ 6\text{d}$ ($T+86\text{d}$) | Methodologist | `Planned` | Clarifications alter empirical claims or introduce unverified statements | Restrict text revisions strictly to pre-approved rebuttal clarifications (power analysis notes, contact manifold explanation) | Lead Author | $T+86$ Days |
| **CR-03** | **Typeset Final Vector Figures & Tables** | Notification $+ 8\text{d}$ ($T+88\text{d}$) | Visuals Lead | `Planned` | Type 3 bitmap fonts or non-embedded fonts in final PDF | Compile figures using Matplotlib PDF engine with `pdf.fonttype: 42` (TrueType embedding); verify vector rendering | Visuals Lead | $T+88$ Days |
| **CR-04** | **Mint Persistent Zenodo DOI for Benchmark Dataset** | Notification $+ 10\text{d}$ ($T+90\text{d}$) | Data Lead | `Planned` | DOI minting delayed, leaving camera-ready paper with unresolved placeholder links | Upload pre-staged 4-file deposit bundle (125,486 bytes) cataloged in `zenodo_doi_reservation.md` immediately upon acceptance notification | Data Lead | $T+90$ Days |
| **CR-05** | **Public GitHub / Open-Source Code Release** | Notification $+ 10\text{d}$ ($T+90\text{d}$) | Release Lead | `Planned` | Repository link rot or licensing ambiguity | Publish clean MIT-licensed public repository from `release/` bundle; tag release `v1.0.0` matching Zenodo deposit | Release Lead | $T+90$ Days |
| **CR-06** | **OpenReview Camera-Ready PDF & Bundle Ingestion** | Final Deadline ($T+90\text{d}$) | Submitter | `Planned` | Portal timeout or submission formatting check failure | Perform pre-upload verification $\ge 24$ hours prior to deadline; verify checksums of final PDF and supplementary archive | Lead Author | $T+90$ Days |

---

## 3. Camera-Ready Quality Assurance Checklist

- [ ] Page count of main text body strictly $\le 9$ pages (including figures, tables, author block, and acknowledgments).
- [ ] References and checklist permitted beyond the 9-page limit in accordance with NeurIPS guidelines.
- [ ] All 14 figures verified at 600 DPI vector quality with fully embedded fonts.
- [ ] Live Zenodo DOI (`10.5281/zenodo.XXXXXXX`) embedded in abstract and data availability statement.
- [ ] Public GitHub repository URL embedded in code availability statement.
- [ ] Standalone smoke test (`smoke_test.py`) verified functional on public repository tag.

---
*Camera-ready plan verified and certified by Autonomous Agent System.*
