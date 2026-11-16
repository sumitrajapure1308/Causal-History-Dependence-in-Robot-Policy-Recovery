# Post-Submission Cryptographic Artifact Manifest

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Document:** `docs/submission/post_submission/post_submission_manifest.md`  
**Milestone:** Phase 22 — Post-Submission Readiness and Reviewer-Response Preparation  
**Date:** 2026-11-10  
**Verification Status:** `Post-submission readiness` | `Submission-ready evidence` | `Verified`  

---

## 1. Post-Submission Manifest Overview

- **Primary Target Venue:** **NeurIPS Track on Datasets and Benchmarks**  
- **Secondary Target Venues:** **Robotics: Science and Systems (RSS)** (Alternative A) / **IEEE Robotics and Automation Letters (RA-L)** (Alternative B)  
- **Submission Type:** Archival Benchmark and Evaluation Track Research Paper  
- **Provenance Standard:** Cryptographic SHA-256 Digest Verification (Git status: Uninitialized; hash ledger serves as authoritative record)  

---

## 2. Post-Submission Artifact Catalog

| Venue | Submission Type | Required Files | File Path | File Size (Bytes) | Cryptographic Hash (SHA-256) | Verification Status | Required Action | Owner | Deadline |
|---|---|---|---|---|---|---|---|---|---|
| **NeurIPS D&B** | Main Manuscript | Full Manuscript Draft | `docs/manuscript/draft/manuscript.md` | 42,952 | `233c4fa5b843863ba3146c2c4daaaca1456174c5cf94b1eb09887436ec93583e` | `Verified` | Hold frozen for peer-review | Lead Author | Day 0 |
| **NeurIPS D&B** | Supplementary | Appendices S1–S13 | `docs/manuscript/supplementary_materials.md` | 16,409 | `ab2e32058dbb300fcd5511873f5c5f0a454ac354f565af74288506f7893f4fd3` | `Verified` | Hold frozen for peer-review | Visuals Lead | Day 0 |
| **NeurIPS D&B** | Bibliography | Audited BibTeX Database | `docs/manuscript/references/references.bib` | 5,014 | `827cc28d57a27cd1829f058c6bf2f8c73c7621626fce61c7d9dab077c7fa1488` | `Verified` | Maintain audited citations | Visuals Lead | Day 0 |
| **NeurIPS D&B** | Staged Code Bundle| Staged Anonymous ZIP | `results/phase_21/anonymous_release_staging.zip` | 16,393 | `a318dd7de1d4d8d4b1383f696a3e710f8174d08e40f6cf0e2d8ccb27fafcc637` | `Verified` | Ready for portal attachment | Release Lead | Day 0 |
| **NeurIPS D&B** | Dataset / Protocol | Matched Scenarios Manifest | `results/phase_12_stage_c/scenario_manifest.json` | 71,225 | `8a04c47eed1b818f9c823dbb1454bae183c4bf78be8caaab8eea3eff8bd5b259` | `Verified` | Retain immutable dataset | Data Lead | Day 0 |
| **NeurIPS D&B** | Dataset / Results | Stage C Evaluation Summary | `results/phase_12_stage_c/evaluation_summary.json` | 14,596 | `982b796c3735c9d12bb698851b080e5252960e5197703da9c760d9ad57bfc343` | `Verified` | Retain evaluation summary | Data Lead | Day 0 |
| **NeurIPS D&B** | Statistical Data | Paired Comparisons Matrix | `results/phase_12_stage_c/paired_comparisons.json` | 23,272 | `2642472dc83248249f300ab37ff53a7cc9fce16e6074b1cba53248f0c734a25d` | `Verified` | Retain paired data | Data Lead | Day 0 |
| **NeurIPS D&B** | Manuscript Tables | LaTeX Paper Tables (7) | `results/phase_13/paper_tables.json` | 10,872 | `9dd7bbffb81bc7106a7fb2391c971316f94f27988a3265971cd1f4a2f1b604a6` | `Verified` | Retain booktabs structures | Visuals Lead | Day 0 |
| **NeurIPS D&B** | Vector Figure 1 | Method Pipeline PDF | `figures/benchmark/paper/fig_paper_01_method_pipeline.pdf` | 18,182 | `e6816f4079f54c698fc7b3b03202bfb506c985311d6ea4a67f3f30f8a0f680e4` | `Verified` | Maintain vector asset | Visuals Lead | Day 0 |
| **NeurIPS D&B** | Vector Figure 3 | State Matching PDF | `figures/benchmark/paper/fig_paper_03_state_matching.pdf` | 25,359 | `fe2c169eae67c41102e2e0880932561a6ede1fec5e419e79c9ce64de84930150` | `Verified` | Maintain vector asset | Visuals Lead | Day 0 |
| **NeurIPS D&B** | Vector Figure 11 | Mechanism Divergence PDF | `figures/benchmark/paper/fig_paper_11_mechanism_divergence.pdf` | 16,681 | `94e685ba8da102f76a1f7c4067428af309b249edf5dee66effc5876d8ec3d4fe` | `Verified` | Maintain vector asset | Visuals Lead | Day 0 |
| **NeurIPS D&B** | Checkpoint 1 | Reactive MLP Best Weights | `models/checkpoints/reactive_mlp_best.pt` | 81,869 | `f99beb840b878d347772a9423037c47f366fa659d482b5765bc7566b9cdba542` | `Verified` | Maintain checkpoint weight | Release Lead | Day 0 |
| **NeurIPS D&B** | Checkpoint 2 | History GRU Best Weights | `models/checkpoints/history_gru_best.pt` | 272,843 | `5fcf94e2410efca8a8c70f47ea6bec7c8f2efd6bf10b665aa1c7d531a15fd6a0` | `Verified` | Maintain checkpoint weight | Release Lead | Day 0 |
| **NeurIPS D&B** | Checkpoint 3 | Rec Aug MLP Best Weights | `models/checkpoints/recovery_augmented_mlp_best.pt` | 87,461 | `1aba926f4ad7bbd1d147034419afb74956501f0b1fa44dfd9bafe3089c60cd8b` | `Verified` | Maintain checkpoint weight | Release Lead | Day 0 |
| **NeurIPS D&B** | Checkpoint 4 | Rec Aug GRU Best Weights | `models/checkpoints/recovery_augmented_gru_best.pt` | 282,037 | `7888cc1fc63b7d2d47b51d68989636b2108b51d7919ccd83f12511f4a7fd48ee` | `Verified` | Maintain checkpoint weight | Release Lead | Day 0 |
| **NeurIPS D&B** | Standalone Script| Release Smoke Test CLI | `release/smoke_test.py` | 8,471 | `36d6d44f3896e7d8fc3a141ce79c61048cd69b519f92324b24ce9e28191e9ccb` | `Verified` | Automated reproduction test | Release Lead | Day 0 |
| **NeurIPS D&B** | Administrative | Cover Letter to Chairs | `docs/submission/cover_letter.md` | 5,332 | `1df5a6903bbe9553109e708d507459652359bf587dd513508730023c1b05b6b4` | `Verified` | Confidential remarks | Lead Author | Day 0 |
| **NeurIPS D&B** | Post-Submission | Readiness Package Spec | `docs/submission/post_submission/post_submission_readiness_package.md` | 4,753 | `02cb6a5dff01b5f4d31695f199ba4f1eb23d63b4e0850eca0b815d18664119e4` | `Verified` | Lifecycle governance | Lead Author | Day 0 |
| **NeurIPS D&B** | Post-Submission | 29-Item Checklist | `docs/submission/post_submission/post_submission_checklist.md` | 6,562 | `053841a64287e07d07cc4e67cf33ef9cb65cf9a656870b4fb1acaa862caa3a4e` | `Verified` | Quality certification | Lead Author | Day 0 |

---
*Manifest registered and cryptographically verified by Autonomous Agent System.*
