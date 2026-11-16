# Gemini Instructions: Causal-History Dependence in Robot Policy Recovery

This repository hosts an independent, rigorous robotics research project:
**Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures**

All autonomous agents, coding assistants, and human contributors operating in this repository MUST strictly follow these rules:

1. **Independent Project Boundary:** This is an independent new project. Do not merge it with, rename it as, or treat it as an extension of MIND-Contact or MIND-Contact++. Never import previous MIND-Contact results or claim that previous MIND-Contact experiments validate this project.
2. **Read Methodology Before Implementation:** Always read and consult `docs/audit/methodology_summary.md` and `docs/methodology/` specifications before writing code or making design choices.
3. **No Fabrication of Results:** Never fabricate experimental numbers, success rates, recovery metrics, ablation tables, or performance gains.
4. **No Fabrication of Citations:** Never invent papers, authors, venues, or arXiv IDs. Every citation must be verified.
5. **No Fabrication of Visual Artifacts:** Never fabricate plots, figures, tables, videos, or metrics. All figures must be generated from verifiable data pipelines.
6. **No Premature Novelty Claims:** Never claim novelty before a rigorous literature audit. Frame contributions precisely relative to existing benchmarks (e.g., RoboRecover, LIBERO-Recover, LIBERO-Pro2.0).
7. **Simulation vs Hardware Bounding:** Never claim hardware validity from simulation-only experiments. Simulation results are explicitly bounded as simulation-based counterfactual evaluations.
8. **Strict Data Lineage:** Keep raw data (`data/raw/`, `results/raw/`) strictly separate and immutable from processed data (`data/processed/`, `results/processed/`).
9. **Provenance & Reproducibility:** Every run must record and save full configurations, environment parameters, random seeds, execution logs, and output manifests.
10. **Path Discipline:** Use project-relative paths everywhere. Do not hardcode machine-specific absolute paths in source code or scripts.
11. **No Silent Overwrites:** Do not silently overwrite existing code, configurations, or data files without explicit justification.
12. **No Unapproved Deletions:** Never delete existing project files or directories without explicit user approval.
13. **Explicit Verification Status:** Label all metrics and results with explicit status tags: `planned`, `executed`, `validated`, `failed`, or `unavailable`.
14. **Pre-Experiment Testing:** Always implement and run unit and integration tests (smoke tests) before launching official benchmark runs or data collection.
15. **Phase Gate Protocol:** Stop at the end of each designated implementation phase and request user approval before proceeding to the next phase.
16. **Code Provenance Tracking:** Document reused code separately from newly written code in `docs/decision_log.md` with source path, new path, justification, modifications, and validation status.
17. **Separation from Past Work:** Maintain total conceptual, architectural, and data separation from MIND-Contact and MIND-Contact++.

