# Submission Package Artifact Manifest

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/submission/action/submission_package_manifest.md`  
**Milestone:** Phase 24 — Final Submission Action Preparation  
**Target Venues:** NeurIPS Track on Datasets and Benchmarks (Primary) | RSS / IEEE RA-L (Backups)  
**Date:** 2026-11-10  
**Verification Status:** `Final submission action plan` | `Submission action plan` | `Verified`  

---

## 1. Primary Submission Artifacts Inventory & Cryptographic Ledger

| Component Name | Relative Path | Target Description | File Size | SHA-256 Cryptographic Hash | Verification Status | Required Action | Owner | Deadline |
|---|---|---|---|---|---|---|---|---|
| Manuscript Draft (Markdown) | `docs/manuscript/draft/manuscript.md` | Main text source | 42,952 bytes | `233c4fa5b843863ba3146c2c4daaaca1456174c5cf94b1eb09887436ec93583e` | `Verified` | Compile to `neurips_2026.sty` | Typesetter | Day 3 |
| Supplementary Materials | `docs/manuscript/supplementary_materials.md` | Appendices S1–S13 | 16,409 bytes | `ab2e32058dbb300fcd5511873f5c5f0a454ac354f565af74288506f7893f4fd3` | `Verified` | Compile to Supplementary PDF | Typesetter | Day 3 |
| Bibliographic References (BibTeX) | `docs/manuscript/references/references.bib` | 17 verified citations | 5,014 bytes | `827cc28d57a27cd1829f058c6bf2f8c73c7621626fce61c7d9dab077c7fa1488` | `Verified` | Link in LaTeX build | Typesetter | Day 3 |
| Scenario Manifest (Data) | `results/phase_12_stage_c/scenario_manifest.json` | 200 matched scenario definitions | 71,225 bytes | `8a04c47eed1b818f9c823dbb1454bae183c4bf78be8caaab8eea3eff8bd5b259` | `Verified` | Ingest into submission ZIP | Data Lead | Day 2 |
| Evaluation Summary (Benchmark) | `results/phase_12_stage_c/evaluation_summary.json` | 20,000 rollout statistics | 14,596 bytes | `982b796c3735c9d12bb698851b080e5252960e5197703da9c760d9ad57bfc343` | `Verified` | Ingest into submission ZIP | Data Lead | Day 2 |
| Paired Comparisons (Statistics) | `results/phase_12_stage_c/paired_comparisons.json` | Primary McNemar & Wilcoxon tests | 23,272 bytes | `2642472dc83248249f300ab37ff53a7cc9fce16e6074b1cba53248f0c734a25d` | `Verified` | Ingest into submission ZIP | Data Lead | Day 2 |
| Paper Tables (JSON) | `results/phase_13/paper_tables.json` | Tables 1–7 in structured JSON | 10,872 bytes | `9dd7bbffb81bc7106a7fb2391c971316f94f27988a3265971cd1f4a2f1b604a6` | `Verified` | Ingest into submission ZIP | Visuals Lead | Day 2 |
| Figure 1 (Vector PDF) | `figures/benchmark/paper/fig_paper_01_method_pipeline.pdf` | Methodology pipeline diagram | 18,182 bytes | `e6816f4079f54c698fc7b3b03202bfb506c985311d6ea4a67f3f30f8a0f680e4` | `Verified` | Embed in main PDF | Visuals Lead | Day 3 |
| Figure 3 (Vector PDF) | `figures/benchmark/paper/fig_paper_03_state_matching.pdf` | State matching precision | 25,359 bytes | `fe2c169eae67c41102e2e0880932561a6ede1fec5e419e79c9ce64de84930150` | `Verified` | Embed in main PDF | Visuals Lead | Day 3 |
| Figure 5 (Vector PDF) | `figures/benchmark/paper/fig_paper_05_recovery_success_by_policy.pdf` | Recovery success by policy | 19,143 bytes | `0a2606e4372827302744633c170106cb64655ade3087c16020d2f81ebb804252` | `Verified` | Embed in main PDF | Visuals Lead | Day 3 |
| Figure 7 (Vector PDF) | `figures/benchmark/paper/fig_paper_07_recovery_success_by_failure_type.pdf` | Recovery by failure type | 18,637 bytes | `121dcab6f44fc07aba4d9b3190328d83aa83c021b109e1ced37c83cfeecd4d2c` | `Verified` | Embed in main PDF | Visuals Lead | Day 3 |
| Model Checkpoint (Reactive MLP) | `models/checkpoints/reactive_mlp_best.pt` | Pre-trained PyTorch weights | 81,869 bytes | `f99beb840b878d347772a9423037c47f366fa659d482b5765bc7566b9cdba542` | `Verified` | Include in model weights zip | DevOps Lead | Day 2 |
| Model Checkpoint (History GRU) | `models/checkpoints/history_gru_best.pt` | Pre-trained PyTorch weights | 272,843 bytes | `5fcf94e2410efca8a8c70f47ea6bec7c8f2efd6bf10b665aa1c7d531a15fd6a0` | `Verified` | Include in model weights zip | DevOps Lead | Day 2 |
| Model Checkpoint (Rec-Aug MLP) | `models/checkpoints/recovery_augmented_mlp_best.pt` | Pre-trained PyTorch weights | 87,461 bytes | `1aba926f4ad7bbd1d147034419afb74956501f0b1fa44dfd9bafe3089c60cd8b` | `Verified` | Include in model weights zip | DevOps Lead | Day 2 |
| Model Checkpoint (Rec-Aug GRU) | `models/checkpoints/recovery_augmented_gru_best.pt` | Pre-trained PyTorch weights | 282,037 bytes | `7888cc1fc63b7d2d47b51d68989636b2108b51d7919ccd83f12511f4a7fd48ee` | `Verified` | Include in model weights zip | DevOps Lead | Day 2 |
| Release Smoke Test CLI | `release/smoke_test.py` | 2.75s verification script | 8,471 bytes | `36d6d44f3896e7d8fc3a141ce79c61048cd69b519f92324b24ce9e28191e9ccb` | `Verified` | Test in clean container | DevOps Lead | Day 2 |
| Release Dockerfile | `release/Dockerfile` | Headless CPU container recipe | 1,079 bytes | `589156440ff649cb33c1cac4348c67d96f39f03df1c9557e6cbfe19b47f8ed6f` | `Verified` | Build and smoke test | DevOps Lead | Day 2 |
| Release Environment Config | `release/environment.yml` | Conda lockfile | 381 bytes | `dd7ee46c3ca368df043409e1b1077db2cef908946135afb2ad0f4f2cb1be0b48` | `Verified` | Test conda create | DevOps Lead | Day 2 |
| Release Reproduction Script | `release/run_all.py` | End-to-end reproduction runner | 672 bytes | `81ea452e0a3f16c7944ffdec9dea73d88c444863c1466163c322b2d4ac56093d` | `Verified` | Test end-to-end runner | DevOps Lead | Day 2 |
| Anonymous Release Staging ZIP | `results/phase_21/anonymous_release_staging.zip` | Pre-staged double-blind bundle | 16,393 bytes | `a318dd7de1d4d8d4b1383f696a3e710f8174d08e40f6cf0e2d8ccb27fafcc637` | `Verified` | Upload to anonymous repo | DevOps Lead | Day 2 |
| Final Submission Decision | `docs/submission/final_decision/final_submission_decision.md` | Formal decision certificate | 4,749 bytes | `9148bc530828db7c52f259862517d67b69eddfb14df853510049c7bb5ae3e61b` | `Verified` | Archival record | Lead Author | Day 0 |
| Journal-Readiness Gate | `docs/submission/final_decision/journal_readiness_gate.md` | 31-dimension audit matrix | 10,569 bytes | `72e926ae5730b313f3912b8bedf2d5c0bb39c258641dba07e2f02c4aaba46298` | `Verified` | Archival record | Lead Author | Day 0 |

---

## 2. Packaging Specifications for Live Upload

- **Bundle Format:** Single ZIP archive (`submission_bundle.zip`, ~42 MB total) containing anonymized manuscript PDF, supplementary PDF, standalone release package, pre-trained weights, and scenario definitions.
- **Verification Summary:** 100% of primary submission artifacts verified present, non-empty, and bitwise cryptographically consistent.
- **Operating Constraint:** Final upload action remains strictly paused pending explicit user approval.

---

*Manifest codified and certified by Autonomous Agent System.*  
*Final portal submission action remains paused pending explicit user approval.*
