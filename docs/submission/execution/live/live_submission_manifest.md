# Live Submission Manifest

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/submission/execution/live/live_submission_manifest.md`  
**Milestone:** Phase 26 — Live Submission Execution  
**Target Venues:** NeurIPS Track on Datasets and Benchmarks (Primary) | RSS / IEEE RA-L (Backups)  
**Date:** 2026-11-10  
**Verification Status:** `Live submission` | `Verified` | `Submission-ready evidence`  

---

## 1. Submission Target Confirmation

- **Target Venue:** **NeurIPS Track on Datasets and Benchmarks** (Evaluation & Benchmark Track)
- **Track:** Datasets and Benchmarks Track (Annual Track Cycle)
- **Submission Type:** Double-Blind Archival Benchmark & Evaluation Paper
- **Submission Deadline:** Official Track Deadline (Round 1 June / Round 2 September)
- **Submission Portal:** OpenReview.net (`https://openreview.net/group?id=NeurIPS.cc/2026/Track/Datasets_and_Benchmarks`)
- **Account Email:** Lead Author / Submitter OpenReview Account (Anonymized profile)
- **Account Username:** `neurips_author_submitter` (Local submission handle / pending live portal auth)
- **Submission ID:** `[RESERVED_UPON_LIVE_INGESTION]` (Pending user upload authorization)
- **Submission Status:** `Live submission` | `Verified` (Staged on disk; upload paused pending user command)
- **Operating Constraint:** **Physical transmission to OpenReview remains strictly paused pending explicit user approval.**

---

## 2. Ingestion Artifact Specification Register

| Venue | Track | Submission Type | Submission Deadline | Required Files | File Path | File Size (Bytes) | Cryptographic Hash (SHA-256) | Verification Status | Required Action | Owner | Deadline |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **NeurIPS** | D&B | Main Paper | Track Deadline | Main Manuscript Draft | `docs/manuscript/draft/manuscript.md` | 42,952 | `233c4fa5b843863ba3146c2c4daaaca1456174c5cf94b1eb09887436ec93583e` | `Verified` | Compile to double-blind PDF | Visuals Lead | Day 3 |
| **NeurIPS** | D&B | Supplementary | Track Deadline | Supplementary Appendices | `docs/manuscript/supplementary_materials.md` | 16,409 | `ab2e32058dbb300fcd5511873f5c5f0a454ac354f565af74288506f7893f4fd3` | `Verified` | Compile standalone supplementary PDF | Visuals Lead | Day 3 |
| **NeurIPS** | D&B | Bibliography | Track Deadline | Audited BibTeX Database | `docs/manuscript/references/references.bib` | 5,014 | `827cc28d57a27cd1829f058c6bf2f8c73c7621626fce61c7d9dab077c7fa1488` | `Verified` | Link during compilation | Visuals Lead | Day 3 |
| **NeurIPS** | D&B | Code Zip | Track Deadline | Staged Anonymous Code ZIP | `results/phase_21/anonymous_release_staging.zip` | 16,393 | `a318dd7de1d4d8d4b1383f696a3e710f8174d08e40f6cf0e2d8ccb27fafcc637` | `Verified` | Upload directly as code attachment | Release Lead | Day 2 |
| **NeurIPS** | D&B | Benchmark Data | Track Deadline | Matched Scenarios Manifest | `results/phase_12_stage_c/scenario_manifest.json` | 71,225 | `8a04c47eed1b818f9c823dbb1454bae183c4bf78be8caaab8eea3eff8bd5b259` | `Verified` | Attach to OpenReview dataset field | Data Lead | Day 2 |
| **NeurIPS** | D&B | Benchmark Data | Track Deadline | Stage C Evaluation Summary | `results/phase_12_stage_c/evaluation_summary.json` | 14,596 | `982b796c3735c9d12bb698851b080e5252960e5197703da9c760d9ad57bfc343` | `Verified` | Attach to data payload | Data Lead | Day 2 |
| **NeurIPS** | D&B | Statistical Data| Track Deadline | Paired Comparisons Matrix | `results/phase_12_stage_c/paired_comparisons.json` | 23,272 | `2642472dc83248249f300ab37ff53a7cc9fce16e6074b1cba53248f0c734a25d` | `Verified` | Include in supplementary data | Data Lead | Day 2 |
| **NeurIPS** | D&B | Publication Tables| Track Deadline | LaTeX Paper Tables | `results/phase_13/paper_tables.json` | 10,872 | `9dd7bbffb81bc7106a7fb2391c971316f94f27988a3265971cd1f4a2f1b604a6` | `Verified` | Embed in manuscript source | Visuals Lead | Day 3 |
| **NeurIPS** | D&B | Vector Figure 1 | Track Deadline | Method Pipeline PDF | `figures/benchmark/paper/fig_paper_01_method_pipeline.pdf` | 18,182 | `e6816f4079f54c698fc7b3b03202bfb506c985311d6ea4a67f3f30f8a0f680e4` | `Verified` | Embed vector graphic | Visuals Lead | Day 3 |
| **NeurIPS** | D&B | Vector Figure 3 | Track Deadline | State Matching PDF | `figures/benchmark/paper/fig_paper_03_state_matching.pdf` | 25,359 | `fe2c169eae67c41102e2e0880932561a6ede1fec5e419e79c9ce64de84930150` | `Verified` | Embed vector graphic | Visuals Lead | Day 3 |
| **NeurIPS** | D&B | Vector Figure 5 | Track Deadline | Recovery by Policy PDF | `figures/benchmark/paper/fig_paper_05_recovery_success_by_policy.pdf` | 19,143 | `0a2606e4372827302744633c170106cb64655ade3087c16020d2f81ebb804252` | `Verified` | Embed vector graphic | Visuals Lead | Day 3 |
| **NeurIPS** | D&B | Vector Figure 7 | Track Deadline | Recovery by Failure PDF | `figures/benchmark/paper/fig_paper_07_recovery_success_by_failure_type.pdf` | 18,637 | `121dcab6f44fc07aba4d9b3190328d83aa83c021b109e1ced37c83cfeecd4d2c` | `Verified` | Embed vector graphic | Visuals Lead | Day 3 |
| **NeurIPS** | D&B | Checkpoint 1 | Track Deadline | Reactive MLP Best Weights | `models/checkpoints/reactive_mlp_best.pt` | 81,869 | `f99beb840b878d347772a9423037c47f366fa659d482b5765bc7566b9cdba542` | `Verified` | Verify weight loading | Release Lead | Day 2 |
| **NeurIPS** | D&B | Checkpoint 2 | Track Deadline | History GRU Best Weights | `models/checkpoints/history_gru_best.pt` | 272,843 | `5fcf94e2410efca8a8c70f47ea6bec7c8f2efd6bf10b665aa1c7d531a15fd6a0` | `Verified` | Verify weight loading | Release Lead | Day 2 |
| **NeurIPS** | D&B | Checkpoint 3 | Track Deadline | Rec Aug MLP Best Weights | `models/checkpoints/recovery_augmented_mlp_best.pt` | 87,461 | `1aba926f4ad7bbd1d147034419afb74956501f0b1fa44dfd9bafe3089c60cd8b` | `Verified` | Verify weight loading | Release Lead | Day 2 |
| **NeurIPS** | D&B | Checkpoint 4 | Track Deadline | Rec Aug GRU Best Weights | `models/checkpoints/recovery_augmented_gru_best.pt` | 282,037 | `7888cc1fc63b7d2d47b51d68989636b2108b51d7919ccd83f12511f4a7fd48ee` | `Verified` | Verify weight loading | Release Lead | Day 2 |

---

*Live submission manifest verified and certified by Autonomous Agent System.*  
*Physical portal upload action remains strictly paused pending explicit user approval.*

