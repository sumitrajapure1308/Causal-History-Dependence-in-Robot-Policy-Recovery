# Archival Submission Execution Package

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Document:** `docs/submission/execution/submission_execution_package.md`  
**Milestone:** Phase 20 — Final Submission Execution Preparation  
**Date:** 2026-11-10  
**Verification Status:** `Submission execution package` | `Submission-ready evidence` | `Verified`  

---

## 1. Submission Overview & Target Venues

- **Primary Venue:** **NeurIPS Track on Datasets and Benchmarks**
  - Track Profile: Rigorous benchmark methodology, open evaluation protocol, unconfounded control validation, and reproducible codebase.
  - Evaluation Focus: Scientific validity of matched-state recovery protocol, physical decoupling findings, and statistical rigor across 20,000 standardized rollouts.
- **Backup Venues:** 
  - **Alternative A:** **Robotics: Science and Systems (RSS)** — Manipulation systems and algorithmic evaluation focus.
  - **Alternative B:** **IEEE Robotics and Automation Letters (RA-L)** — Rapid letter track with concise 6-to-8 page presentation.
- **Submission Type:** Archival Benchmark and Evaluation Track Research Paper.
- **Submission Deadline:** Official Track Deadline (Annual Conference Cycle: June Round 1 / September Round 2).
- **Execution Operating Status:** **Submission execution package assembled and frozen; physical transmission to submission portals remains strictly paused pending explicit user approval.**

> [!NOTE]
> Bounded Scope Declaration: No claims are made that any target venue accepts or will accept the submission. No claims of "top-tier" or "Q1" status are made. All evaluations are simulation-based counterfactual evaluations in MuJoCo 3.10.0; physical robot hardware deployment and cross-simulator replication are bounded as documented future work.

---

## 2. Submission Execution Breakdown

| # | Action Item | Detailed Scope | Owner | Deadline | Status | Risk Level | Mitigation Strategy |
|---|---|---|---|---|---|---|---|
| **1** | **User Approval Gate** | Obtain explicit user command to proceed from execution packaging to live upload | User / Lead Author | Day 0 | `Planned` | High (Unapproved external action) | Hard execution stop until explicit user instruction is issued |
| **2** | **Double-Blind Identity Scrub** | Remove author names, affiliations, institutions, and repository URLs from manuscript PDF and release metadata | Lead Author | Day 1 | `Verified` in draft | Low (De-anonymization) | Double-blind inspection protocol against all manuscript sections |
| **3** | **Anonymous Repository Sync** | Verify release package zip checksums for upload to anonymous hosting portal (e.g., Anonymous GitHub) | Release Lead | Day 2 | `Verified` local | Low (Portal sync glitch) | Provide self-contained standalone ZIP archive with all weights |
| **4** | **Zenodo Dataset Pre-Staging** | Stage the 20,000-rollout benchmark dataset, scenario manifests, and paired records for permanent deposition | Data Lead | Day 2 | `Planned` | Low (Staging delay) | Retain immutable local validated copies in `results/phase_12_stage_c/` |
| **5** | **LaTeX Engine Compilation** | Compile `docs/manuscript/draft/manuscript.md` into official `neurips_2026.sty` format with 9-page budget | Visuals Lead | Day 3 | `Planned` | Low (Page overflow) | Pre-budgeted page count: 8.2 pages main text + references + checklist |
| **6** | **Vector PDF Embedding** | Embed all 14 standalone 600 DPI vector PDF figures into the compiled document | Visuals Lead | Day 3 | `Verified` files | Low (Font rendering issues) | Pre-compiled vector PDFs in `figures/benchmark/paper/` |
| **7** | **Paper Checklist Certification** | Complete official NeurIPS Dataset and Benchmark Paper Checklist (ethics, compute, reproducibility) | Lead Author | Day 4 | `Verified` | Zero | Checklist pre-verified in `docs/manuscript/supplementary_materials.md` |
| **8** | **OpenReview Portal Ingestion** | Input paper metadata (exact 250-word abstract, subject areas, keywords), upload main PDF and zip | Submitter | Day 5 | `Planned` | Low (Portal congestion) | Submit >= 24 hours prior to final submission window closure |
| **9** | **Post-Upload Hash Verification** | Download uploaded files from OpenReview; compute SHA-256 digests and compare against on-disk manifest | Lead Author | Day 5 | `Planned` | Zero | Automated cryptographic verification script |
| **10** | **Rebuttal Phase Monitoring** | Monitor review release; deploy pre-structured rebuttal responses from `reviewer_response_template.md` | All Authors | Post-Review | `Planned` | Medium (Reviewer skepticism on null results) | Pre-verified evidence: physical contact normal forces attenuate action divergence |

---

## 3. Required Submission Artifacts

1. **Main Manuscript Document:** Anonymized PDF adhering to `neurips_2026.sty` (9 pages main text + references + checklist).
2. **Supplementary Materials Document:** Appendices S1–S13 spanning experimental protocols, hyperparameter tables, proofs, and extended failure audits (`docs/manuscript/supplementary_materials.md`).
3. **Reproducible Release Code Package:** Standalone `release/` bundle containing Dockerfile, environment configs, policy weights, evaluation drivers, and smoke tests (23 files, 35 MB).
4. **Benchmark Scenario & Evaluation Manifests:** `results/phase_12_stage_c/scenario_manifest.json` (200 matched scenarios) and `evaluation_summary.json` (20,000 rollouts).
5. **Cryptographic Provenance Manifests:** `results/phase_19/phase_19_file_hashes.json` (78 hashes) and `results/phase_20/phase_20_file_hashes.json`.

---

## 4. Required Approvals

- **User Approval Gate:** Explicit authorization from the user is required before any external network connection, portal upload, or DOI registration occurs.
- **Author Sign-Off:** Lead author and contributor consensus on double-blind anonymization compliance.
- **Methodological Verification:** Frozen methodology sign-off confirming zero deviation from pre-registered Stage C protocols.

---

## 5. Required Checks & Verification Milestones

- **Unit & Integration Tests:** 67/67 tests passing (`pytest tests -v` passing in under 12 seconds).
- **Release Smoke Test:** `release/smoke_test.py` passing in under 3.0 seconds.
- **Sub-Atomic State Matching:** State matcher residual distance $D \le 10^{-10}$ m across all matched scenario pairs.
- **Bitwise Determinism:** Bitwise reproducible duplicate trajectory execution ($D = 0.0$).
- **Anti-Overclaim Verification:** Strict enforcement of zero unsupported novelty claims, zero hardware claims, and zero unverified generalization claims.

---

## 6. Required Submissions

- **OpenReview Upload Receipt:** Official system receipt confirming successful receipt of:
  - Main manuscript PDF.
  - Supplementary material PDF.
  - Source code and checkpoint ZIP archive.
  - Metadata form inputs (subject areas: Robot Learning, Datasets & Benchmarks, Evaluation Methodologies).

---

## 7. Required Follow-Ups

- **Submission Receipt Archival:** Save PDF receipt and submission ID in `docs/submission/execution/receipt.pdf`.
- **Reviewer Response Staging:** Keep `docs/submission/reviewer_response_template.md` staged for immediate rebuttal drafting upon review release.
- **Camera-Ready Pipeline:** Maintain compilation scripts for immediate de-anonymization and final camera-ready generation upon acceptance notification.

---
*Execution package prepared and certified by Autonomous Agent System.*

