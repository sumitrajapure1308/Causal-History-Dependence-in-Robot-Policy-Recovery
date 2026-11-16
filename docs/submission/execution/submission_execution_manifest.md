# Cryptographic Submission Execution Manifest

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Document:** `docs/submission/execution/submission_execution_manifest.md`  
**Milestone:** Phase 20 — Final Submission Execution Preparation  
**Date:** 2026-11-10  
**Verification Status:** `Submission execution package` | `Submission-ready evidence` | `Verified`  

---

## 1. Execution Manifest Overview

- **Primary Target Venue:** **NeurIPS Track on Datasets and Benchmarks**  
- **Secondary Target Venues:** **Robotics: Science and Systems (RSS)** (Alternative A) / **IEEE Robotics and Automation Letters (RA-L)** (Alternative B)  
- **Submission Type:** Archival Benchmark and Evaluation Track Research Paper  
- **Provenance Standard:** Cryptographic SHA-256 Digest Verification (Git status: No git repository initialized; hash manifest serves as authoritative ledger)  

---

## 2. Exhaustive Submission Artifact Register

| Venue | Submission Type | Required Files | File Path | File Size (Bytes) | Cryptographic Hash (SHA-256) | Verification Status | Required Action | Owner | Deadline |
|---|---|---|---|---|---|---|---|---|---|
| **NeurIPS D&B** | Main Manuscript | Full Manuscript Draft | `docs/manuscript/draft/manuscript.md` | 42,952 | `233c4fa5b843863ba3146c2c4daaaca1456174c5cf94b1eb09887436ec93583e` | `Verified` | Compile to PDF via `neurips_2026.sty` | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Supplementary | Appendices S1–S13 | `docs/manuscript/supplementary_materials.md` | 16,409 | `ab2e32058dbb300fcd5511873f5c5f0a454ac354f565af74288506f7893f4fd3` | `Verified` | Compile standalone supplementary PDF | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Bibliography | Audited BibTeX Database | `docs/manuscript/references/references.bib` | 5,014 | `827cc28d57a27cd1829f058c6bf2f8c73c7621626fce61c7d9dab077c7fa1488` | `Verified` | Link during LaTeX compilation | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Dataset / Protocol | Matched Scenarios Manifest | `results/phase_12_stage_c/scenario_manifest.json` | 71,225 | `8a04c47eed1b818f9c823dbb1454bae183c4bf78be8caaab8eea3eff8bd5b259` | `Verified` | Upload to Zenodo / OpenReview | Data Lead | Day 2 |
| **NeurIPS D&B** | Dataset / Results | Stage C Evaluation Summary | `results/phase_12_stage_c/evaluation_summary.json` | 14,596 | `982b796c3735c9d12bb698851b080e5252960e5197703da9c760d9ad57bfc343` | `Verified` | Include in data bundle | Data Lead | Day 2 |
| **NeurIPS D&B** | Statistical Results | Paired Comparisons Matrix | `results/phase_12_stage_c/paired_comparisons.json` | 23,272 | `2642472dc83248249f300ab37ff53a7cc9fce16e6074b1cba53248f0c734a25d` | `Verified` | Deposition in supplementary data | Data Lead | Day 2 |
| **NeurIPS D&B** | Manuscript Tables | Primary Paper Tables (7) | `results/phase_13/paper_tables.json` | 10,872 | `9dd7bbffb81bc7106a7fb2391c971316f94f27988a3265971cd1f4a2f1b604a6` | `Verified` | Render as LaTeX booktabs | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 1 | Method Pipeline Vector PDF | `figures/benchmark/paper/fig_paper_01_method_pipeline.pdf` | 18,182 | `e6816f4079f54c698fc7b3b03202bfb506c985311d6ea4a67f3f30f8a0f680e4` | `Verified` | Embed in Section 3 | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 2 | Scenario Generation PDF | `figures/benchmark/paper/fig_paper_02_scenario_generation.pdf` | 20,359 | `dc4cbb6eef6399878f2f26d9ec577d7f8765293f0d2bf2a37c925551e961d495` | `Verified` | Embed in Section 3 | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 3 | State Matching Precision PDF| `figures/benchmark/paper/fig_paper_03_state_matching.pdf` | 25,359 | `fe2c169eae67c41102e2e0880932561a6ede1fec5e419e79c9ce64de84930150` | `Verified` | Embed in Section 3 | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 4 | Recovery Success Condition | `figures/benchmark/paper/fig_paper_04_recovery_success_by_condition.pdf` | 19,223 | `e5378b288bce1a5783d75e8ff8e49a5052007febb358c70ddb475d74f5c72c83` | `Verified` | Embed in Section 4 | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 5 | Recovery Success Policy | `figures/benchmark/paper/fig_paper_05_recovery_success_by_policy.pdf` | 19,143 | `0a2606e4372827302744633c170106cb64655ade3087c16020d2f81ebb804252` | `Verified` | Embed in Section 4 | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 6 | Recovery Success Task | `figures/benchmark/paper/fig_paper_06_recovery_success_by_task.pdf` | 19,504 | `4501baec7efba3c0ea5e87df2237955d97262ab5b7ce88e45d9802999c7c4696` | `Verified` | Embed in Section 4 | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 7 | Failure Type Breakdown | `figures/benchmark/paper/fig_paper_07_recovery_success_by_failure_type.pdf` | 18,637 | `121dcab6f44fc07aba4d9b3190328d83aa83c021b109e1ced37c83cfeecd4d2c` | `Verified` | Embed in Section 4 | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 8 | History Dependence Score | `figures/benchmark/paper/fig_paper_08_history_dependence_score.pdf` | 20,355 | `8019e159fb49bb2d56ba776496dbedf74d8835a231b5f519999b5b48d54f6273` | `Verified` | Embed in Section 4 | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 9 | Paired Difference Distrib | `figures/benchmark/paper/fig_paper_09_paired_difference_distribution.pdf` | 21,845 | `690a709d780f54ac114234d0b57fd3692a713f6bc7546a8a5023ce778efd633f` | `Verified` | Embed in Section 4 | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 10 | CI Forest Plot | `figures/benchmark/paper/fig_paper_10_confidence_interval_forest.pdf` | 19,324 | `218dba2f9adae06aefd68b1e1494e2a54c5668e78b7926a39fd87c91b84df1b2` | `Verified` | Embed in Section 4 | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 11 | Mechanism Divergence | `figures/benchmark/paper/fig_paper_11_mechanism_divergence.pdf` | 16,681 | `94e685ba8da102f76a1f7c4067428af309b249edf5dee66effc5876d8ec3d4fe` | `Verified` | Embed in Section 4 | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 12 | Recovery Decomposition | `figures/benchmark/paper/fig_paper_12_recovery_decomposition.pdf` | 21,907 | `d38a766aad2a64cdd1bc5e79405f4e096b864b27ed2a497bcae38086d40ed492` | `Verified` | Embed in Section 4 | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 13 | Policy Ranking Summary | `figures/benchmark/paper/fig_paper_13_policy_ranking.pdf` | 17,050 | `f6c04b73be903911eb1fbc443eb50b196521ede53dc8bcf583d7ca1a604bf56c` | `Verified` | Embed in Section 4 | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Figure 14 | Sensitivity Analysis | `figures/benchmark/paper/fig_paper_14_sensitivity_analysis.pdf` | 20,238 | `5146a853f9d2c638eb2dbb9d38bfb83c92b652e98354fee969fab0d051f18b62` | `Verified` | Embed in Appendix | Visuals Lead | Day 3 |
| **NeurIPS D&B** | Model Weight | Baseline Reactive MLP | `models/checkpoints/reactive_mlp_best.pt` | 81,869 | `f99beb840b878d347772a9423037c47f366fa659d482b5765bc7566b9cdba542` | `Verified` | Include in release code zip | Release Lead | Day 2 |
| **NeurIPS D&B** | Model Weight | History-Conditioned GRU | `models/checkpoints/history_gru_best.pt` | 272,843 | `5fcf94e2410efca8a8c70f47ea6bec7c8f2efd6bf10b665aa1c7d531a15fd6a0` | `Verified` | Include in release code zip | Release Lead | Day 2 |
| **NeurIPS D&B** | Model Weight | Recovery-Augmented MLP | `models/checkpoints/recovery_augmented_mlp_best.pt` | 87,461 | `1aba926f4ad7bbd1d147034419afb74956501f0b1fa44dfd9bafe3089c60cd8b` | `Verified` | Include in release code zip | Release Lead | Day 2 |
| **NeurIPS D&B** | Model Weight | Recovery-Augmented GRU | `models/checkpoints/recovery_augmented_gru_best.pt` | 282,037 | `7888cc1fc63b7d2d47b51d68989636b2108b51d7919ccd83f12511f4a7fd48ee` | `Verified` | Include in release code zip | Release Lead | Day 2 |
| **NeurIPS D&B** | Standalone Code | Release Smoke Test CLI | `release/smoke_test.py` | 8,471 | `36d6d44f3896e7d8fc3a141ce79c61048cd69b519f92324b24ce9e28191e9ccb` | `Verified` | Automated reproduction gate | Release Lead | Day 1 |
| **NeurIPS D&B** | Container Config| Docker Containerfile | `release/Dockerfile` | 1,079 | `589156440ff649cb33c1cac4348c67d96f39f03df1c9557e6cbfe19b47f8ed6f` | `Verified` | Docker build validation | Release Lead | Day 2 |
| **NeurIPS D&B** | Env Config | Conda Environment YAML | `release/environment.yml` | 381 | `dd7ee46c3ca368df043409e1b1077db2cef908946135afb2ad0f4f2cb1be0b48` | `Verified` | Conda env validation | Release Lead | Day 2 |
| **NeurIPS D&B** | Documentation | Standalone Release Guide | `release/README.md` | 3,879 | `2e97cfbb998e831c7875d578cf5934b60c558f4de3c38fd2e236a57a4a57200a` | `Verified` | Include in root of zip | Release Lead | Day 2 |
| **NeurIPS D&B** | Administrative | Senior Chairs Cover Letter | `docs/submission/cover_letter.md` | 5,332 | `1df5a6903bbe9553109e708d507459652359bf587dd513508730023c1b05b6b4` | `Verified` | OpenReview confidential field | Lead Author | Day 4 |
| **NeurIPS D&B** | Rebuttal Staging| Reviewer Rebuttal Protocol | `docs/submission/reviewer_response_template.md` | 4,146 | `69bded07ae9305024bf20c4a29375056ef6d48b089ad1ba4eb3753b36e50ae83` | `Verified` | Hold for discussion period | All Authors | Rebuttal |
| **NeurIPS D&B** | Execution Core | Submission Package Spec | `docs/submission/execution/submission_execution_package.md` | 7,516 | `131448d24fdd62e489f8ccf8ffb3051591016744543612bbef04727daf7e8200` | `Verified` | Submission governance | Lead Author | Day 0 |
| **NeurIPS D&B** | Execution Core | 29-Item Execution Checklist| `docs/submission/execution/submission_execution_checklist.md` | 7,867 | `680f43761cbb2a5b3193c5368e50b976e22d17c1cce989f851f2646714746732` | `Verified` | Final pre-flight sign-off | Lead Author | Day 0 |

---
*Manifest registered and cryptographically verified by Autonomous Agent System.*

