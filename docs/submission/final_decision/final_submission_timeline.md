# Final Submission Operations Timeline

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Document:** `docs/submission/final_decision/final_submission_timeline.md`  
**Milestone:** Phase 23 — Final Submission Decision and Journal-Readiness Gate  
**Date:** 2026-11-10  
**Verification Status:** `Final submission decision` | `Journal-readiness gate` | `Submission-ready evidence` | `Verified`  

---

## 1. Operational Scheduling Architecture

The final submission timeline coordinates all packaging, ingestion, verification, peer-review rebuttal, and camera-ready deposition activities for the target venue: **NeurIPS Track on Datasets and Benchmarks** (with backup venues **RSS** and **IEEE RA-L**).

Operating constraint: **All live external submission operations remain strictly paused until explicit user authorization is provided.**

---

## 2. Detailed Operational Task Schedule

| Task ID | Task Description | Owner | Start Date | End Date | Duration | Dependencies | Required Artifacts | Required Approvals | Required Checks | Required Submissions | Required Follow-Ups | Primary Risk | Mitigation Strategy |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **F-01** | **Decision Freeze & Gate Certification** | Lead Author | 2026-11-10 | 2026-11-10 | 1 Day | Phase 22 package | `final_submission_decision.md`, `journal_readiness_gate.md` | User approval gate | Check all 31 dimensions pass or bounded | None | Archive local git-free hash ledger | Unapproved external transmission | Enforce strict pause; zero automatic network requests |
| **F-02** | **Double-Blind Scrub Final Sign-Off** | Lead Author | 2026-11-11 | 2026-11-11 | 1 Day | F-01 freeze | Anonymized `manuscript.md`, stripped `references.bib` | Author sign-off | Regex search for author names, emails, grants | None | Verify zero self-identifying phrasing | Desk rejection via de-anonymization | Double-blind inspection protocol (18 dimensions verified) |
| **F-03** | **Release Package Staging Verification** | Release Lead | 2026-11-12 | 2026-11-12 | 1 Day | F-02 scrub | `anonymous_release_staging.zip` (16,393 bytes) | Data Lead approval | Verify `release/smoke_test.py` passes in Docker | Supplementary ZIP bundle | Generate SHA-256 checksum file | Code link failure during review | Bundle self-contained code ZIP directly to OpenReview |
| **F-04** | **LaTeX Typesetting & Font Embedding** | Visuals Lead | 2026-11-13 | 2026-11-13 | 1 Day | F-02 scrub | Compiled `manuscript.pdf`, 14 vector figures | Visuals Lead sign-off | Page count $\le 9$ pages main body; 600 DPI vector rendering | Formatted submission PDF | Visual inspection of typography and fonts | Formatting rejection / overflow | Strict page budget: 8.2 pages main text + references + checklist |
| **F-05** | **Pre-Flight Ingestion & OpenReview Submission** | Submitter | 2026-11-14 | 2026-11-14 | 1 Day | F-03, F-04 | Final PDF, Supplementary PDF, Code ZIP | Lead Author approval | Verify metadata matches manuscript (250-word abstract) | Upload to OpenReview system | Save official confirmation receipt | Server overload at final deadline | Submit $\ge 24$ hours prior to deadline cutoff |
| **F-06** | **Post-Upload Checksum Match & Archival** | Lead Author | 2026-11-15 | 2026-11-15 | 1 Day | F-05 submission | OpenReview submission receipt PDF | Lead Author sign-off | Re-download uploaded files; match SHA-256 against manifest | Official submission receipt archive | Log receipt in `docs/submission/final_decision/` | Corrupted upload on server | Automated checksum match against local files |
| **F-07** | **Interactive Rebuttal Dispatch & Closure** | All Authors | Review Release Date | Rebuttal Close Date | 14 Days | Official review release | `reviewer_response_plan.md`, `rebuttal_plan.md` | All Authors consensus | Verify all empirical answers match Stage C benchmark data | OpenReview rebuttal responses | Track reviewer rating changes | Reviewer pushback on null effect / simulation | Pre-structured rebuttal matrices citing normal contact damping |
| **F-08** | **Camera-Ready De-Anonymization & DOI Deposition** | Visuals Lead / Data Lead | Camera-Ready Notification | Camera-Ready Deadline | 15 Days | Notification of Acceptance | Final LaTeX source, 4-file Zenodo bundle | All Authors sign-off | Verify full author names, affiliations, grant numbers | Camera-ready PDF, Zenodo open dataset | Link persistent DOI into camera-ready paper | Delay in DOI resolution | Deploy pre-staged deposit payload cataloged in `zenodo_doi_reservation.md` |

---
*Operations timeline approved and certified by Autonomous Agent System.*

