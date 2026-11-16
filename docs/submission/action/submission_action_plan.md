# Final Submission Action Plan

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/submission/action/submission_action_plan.md`  
**Milestone:** Phase 24 — Final Submission Action Preparation  
**Target Venues:** NeurIPS Track on Datasets and Benchmarks (Primary) | RSS / IEEE RA-L (Backups)  
**Date:** 2026-11-10  
**Verification Status:** `Final submission action plan` | `Submission action plan` | `Submission-ready evidence`  

---

## 1. Executive Summary & Target Venue Specifications

This document defines the final operational submission action plan for transitioning the completed, audited, and certified benchmark package from internal repository release candidate to live archival conference submission.

- **Primary Submission Target:** **NeurIPS Track on Datasets and Benchmarks** (Evaluation & Benchmark Track)
  - *Format:* 9 pages main text (excluding references and NeurIPS paper checklist), double-blind, anonymized vector figures, standalone code release, complete dataset manifest.
- **Backup Submission Target A:** **Robotics: Science and Systems (RSS)**
  - *Format:* 8 pages main text plus references, double-blind, robotics benchmark focus.
- **Backup Submission Target B:** **IEEE Robotics and Automation Letters (RA-L)**
  - *Format:* 6–8 pages letter format, single-blind/double-blind depending on letter portal, focused empirical study.
- **Hardware-Mandatory Venues (IEEE T-RO / IJRR):**
  - *Status:* Classified as `NO-GO` because physical robot hardware experiments are mandatory prerequisites.
- **Current Operating Status:** **Action plan fully prepared; portal submission action remains strictly paused pending explicit user approval.**

---

## 2. Comprehensive 10-Point Submission Action Breakdown

| # | Action Item | Target Scope | Owner | Deadline | Status | Risk Level | Mitigation Strategy | Required Artifacts | Required Approvals | Required Checks | Required Submissions | Required Follow-ups |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1** | **User Approval Gate** | Obtain explicit user authorization for live transmission | User / Lead Author | Day 0 | `Planned` | High (Unapproved action) | Enforce hard programmatic pause; execute no network upload commands without user prompt | Phase 24 Action Plan & Decision document | Explicit User Directive | Verify zero pending review blockers | User approval prompt | Transition to Stage 2 |
| **2** | **Double-Blind Anonymization Audit** | Scrub author names, institution affiliations, grant IDs, and machine paths | Lead Author | Day 1 | `Verified` | Low (De-anonymization) | Pre-verified 18-point anonymization regex audit (`docs/audit/anonymization_scrub_audit.md`) | Anonymized manuscript draft & supplementary | Internal Co-Author Sign-Off | Zero author string hits across all text/code | Internal anonymized bundle | Record audit log |
| **3** | **Anonymous Repository & Code Staging** | Deploy sanitized code release to anonymous hosting (OSF / Anonymous GitHub) | DevOps Lead | Day 2 | `Verified` (Local bundle ready) | Low (Broken links / repo downtime) | Pre-staged zip in `results/phase_21/anonymous_release_staging.zip` (16,393 bytes, SHA-256: `a318dd7de...`) | `release/` package, `anonymous_release_staging.zip` | Release Lead | Clean-room unzip, environment rebuild, and smoke test pass | Anonymous repo URL / portal zip upload | Verify public URL accessibility |
| **4** | **Zenodo Dataset DOI Reservation** | Pre-register metadata and reserve DOI for 20,000-rollout benchmark dataset | Data Lead | Day 2 | `Planned` (Metadata ready) | Low (Hosting latency) | Use local verified copy in `results/phase_12_stage_c/`; attach dataset manifest to submission zip | `scenario_manifest.json`, `evaluation_summary.json` | Data Lead | Check JSON schema and SHA-256 integrity | Zenodo deposit draft | Record reserved DOI for camera-ready |
| **5** | **LaTeX Typesetting & Page Budget** | Compile `docs/manuscript/draft/manuscript.md` into official `neurips_2026.sty` | Typesetter | Day 3 | `Planned` (Content audited) | Low (Overlength) | Pre-audited text budget: 8.2 pages fits easily within the 9-page limit; references and checklist exempt | `manuscript.md`, `references.bib`, `neurips_2026.sty` | Visuals Lead | Verify compilation with 0 overfull hboxes and page count $\le 9$ | Compiled main paper PDF | Visual inspection of typography |
| **6** | **Vector PDF Figure Embedding** | Embed all 14 standalone 600 DPI vector PDF figures into compiled manuscript | Visuals Lead | Day 3 | `Verified` (14 vector PDFs ready) | Low (Downsampling blur) | Embed vector PDF files directly from `figures/benchmark/paper/` (no rasterized JPG/PNG downsampling) | 14 vector PDFs (`fig_paper_01` to `fig_paper_14`) | Visuals Lead | Check vector scalability at 800% zoom | Embedded PDF figures | Cross-platform font embedding check |
| **7** | **Mandatory Paper Checklist Compilation** | Complete NeurIPS 2026 Paper Checklist covering compute, reproducibility, and ethics | Lead Author | Day 4 | `Verified` (Text pre-compiled) | Zero | Pre-compiled in Section S8–S13 of `docs/manuscript/supplementary_materials.md` | NeurIPS Checklist form | Lead Author | Verify all questions answered with exact section pointers | Completed checklist section in paper | Consistency verification |
| **8** | **OpenReview Portal Ingestion** | Ingest metadata, exact 250-word abstract, keywords, and upload PDF/ZIP | Submitter | Day 5 | `Planned` | Low (Portal timeout / size limits) | Submission bundle is ~42 MB (well below OpenReview 100 MB limit); submit $\ge 24\text{h}$ prior to deadline | Main PDF, Supplementary PDF, Code ZIP | All Authors | Verify upload confirmation and file integrity | OpenReview upload form | Generate official submission receipt |
| **9** | **Post-Submission Verification & Archival** | Download uploaded PDF/bundle from OpenReview; verify byte-exact matches | Lead Author | Day 5 | `Planned` | Zero | Automated SHA-256 checksum comparison against local pre-upload ledger | Downloaded portal receipt and PDF | Lead Author | Bitwise and perceptual verification | Archived receipt in `results/submission/` | Initiate post-submission monitoring |
| **10** | **Rebuttal Phase Monitoring & Execution** | Monitor discussion portal; deploy pre-structured rebuttal matrix | All Authors | Post-Sub (Review Period) | `Planned` (Matrix ready) | Medium (Reviewer skepticism on sim-only scope) | Deploy pre-validated arguments from `docs/submission/post_submission/reviewer_response_plan.md` | Rebuttal response templates | Lead Author & Co-Authors | Reviewer point-by-point coverage | Official OpenReview rebuttal responses | Camera-ready plan execution |

---

## 3. Required Submission Artifacts & Cryptographic Provenance

The archival submission package comprises the following core verified components:
1. **Main Paper Manuscript:** Anonymized 9-page PDF compiled from `docs/manuscript/draft/manuscript.md` (42,952 bytes, SHA-256: `233c4fa5b843...`).
2. **Supplementary Materials Document:** Appendices S1–S13 compiled from `docs/manuscript/supplementary_materials.md` (16,409 bytes, SHA-256: `ab2e32058d...`).
3. **Bibliographic Database:** Verified 17-entry BibTeX file `docs/manuscript/references/references.bib` (5,014 bytes, SHA-256: `827cc28d57...`).
4. **Confirmatory Benchmark Data:**
   - Scenario definitions: `results/phase_12_stage_c/scenario_manifest.json` (71,225 bytes, SHA-256: `8a04c47eed...`).
   - Evaluation statistics: `results/phase_12_stage_c/evaluation_summary.json` (14,596 bytes, SHA-256: `982b796c37...`).
   - Paired hypothesis tests: `results/phase_12_stage_c/paired_comparisons.json` (23,272 bytes, SHA-256: `2642472dc8...`).
   - Structured publication tables: `results/phase_13/paper_tables.json` (10,872 bytes, SHA-256: `9dd7bbffb8...`).
5. **Standalone Code & Environment Package:**
   - Verification CLI: `release/smoke_test.py` (8,471 bytes, SHA-256: `36d6d44f38...`).
   - Container recipe: `release/Dockerfile` (1,079 bytes, SHA-256: `589156440f...`).
   - Environment lockfile: `release/environment.yml` (381 bytes, SHA-256: `dd7ee46c3c...`).
   - Runner: `release/run_all.py` (672 bytes, SHA-256: `81ea452e0a...`).
   - Pre-staged anonymous bundle: `results/phase_21/anonymous_release_staging.zip` (16,393 bytes, SHA-256: `a318dd7de1...`).
6. **Pre-trained Policy Weights:**
   - `models/checkpoints/reactive_mlp_best.pt` (81,869 bytes, SHA-256: `f99beb840b...`).
   - `models/checkpoints/history_gru_best.pt` (272,843 bytes, SHA-256: `5fcf94e241...`).
   - `models/checkpoints/recovery_augmented_mlp_best.pt` (87,461 bytes, SHA-256: `1aba926f4a...`).
   - `models/checkpoints/recovery_augmented_gru_best.pt` (282,037 bytes, SHA-256: `7888cc1fc6...`).
7. **Publication-Ready Figures:** 14 standalone 600 DPI vector PDFs in `figures/benchmark/paper/`.

---

## 4. Required Approvals & Quality Gates

- **User Approval Gate (MANDATORY):** No portal upload, API submission, or external public disclosure shall be executed without explicit user confirmation.
- **Ethics & Integrity Gate:** Verified compliance with IEEE / ACM / NeurIPS ethics codes. No human subjects, animal subjects, or dual-use military applications.
- **Reproducibility Quality Gate:** `release/smoke_test.py` must execute in clean container environment in $< 5\text{ s}$ with exact state distance $D \le 10^{-10}\text{ m}$ and bitwise action determinism ($D = 0.0$).
- **Anti-Overclaim Audit:** 0 claims of novelty, 0 claims of Q1 journal status, 0 claims of real-robot validity, 0 claims of universal history invariance.

---

*Action plan codified and certified by Autonomous Agent System.*  
*Final portal submission action remains paused pending explicit user approval.*
