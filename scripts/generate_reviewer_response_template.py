#!/usr/bin/env python3
"""
Generate Peer-Review Response Template:
docs/submission/reviewer_response_template.md
"""

import os

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
template_path = os.path.join(repo_root, 'docs', 'submission', 'reviewer_response_template.md')

template_text = """# Peer-Review Response Matrix & Revision Protocol

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Repository Root:** `causal-history-recovery/`  
**Phase:** Phase 16 (Final Submission Decision & Journal-Readiness Audit)  
**Status:** `Submission Decision`, `Template Protocol`, `Audited`  
**Accompanying Manuscript:** `docs/manuscript/draft/manuscript.md`  

---

## 1. Revision Protocol & Response Guidelines

This document provides the structured response matrix to be used during the formal peer-review revision cycle. Every reviewer comment must be addressed point-by-point with:
1. Precise author response quoting exact manuscript modifications.
2. Direct empirical citations to raw data records (`rollout_records.jsonl`), statistical reports, or notebooks.
3. Explicit verification status: `Addressed`, `In Progress`, `Clarified without Code Change`, or `Blocked`.
4. Designation of owner, evidence source, and completion deadline.

*Constraint:* Do not fabricate reviewer comments, responses, or manuscript changes. The template below establishes the standard structure with anticipated methodological review questions.

---

## 2. Reviewer Response Matrix Template

| Reviewer & Point ID | Category | Reviewer Comment / Concern | Author Response | Manuscript Modification / Action Taken | Evidence Source / File | Additional Experiment Required? | Status | Owner | Target Deadline |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **R1.1** | *Methodology / Novelty* | [Reviewer comment regarding distinction from RoboRecover or LIBERO-Recover] | [Author response articulating exact bitwise state matching D <= 1e-10 vs coarse trajectory reset] | [Section and line changes in revised manuscript] | `docs/audit/literature_audit.md`, `Table 1` | None | `Planned` | Methodologist | TBD |
| **R1.2** | *Statistical Power* | [Reviewer comment regarding statistical power or Minimum Detectable Effect size] | [Author response citing N=200 scenario-level inference unit and Clopper-Pearson CIs] | [Clarification in Section 13 and Section 17] | `results/phase_12_stage_c/analysis/primary_analysis.json` | None | `Planned` | Statistician | TBD |
| **R2.1** | *Physical Bounding* | [Reviewer comment regarding real-robot hardware validation or sim-to-real gap] | [Author response emphasizing mandatory limitation bounding and simulation-only scope] | [Explicit restatement of limitation sentence in Sec. 17] | `docs/manuscript/draft/manuscript.md#L269` | None (bounded) | `Planned` | Lead Author | TBD |
| **R2.2** | *Mechanism Interpretation* | [Reviewer comment regarding why recurrent policies diverge in action but not in task success] | [Author response detailing Coulomb friction and normal force contact bottleneck] | [Cross-reference to Section 14.3 and Fig. 11] | `results/phase_12_stage_c/analysis/history_dependence_report.json` | None | `Planned` | Lead Author | TBD |
| **R3.1** | *Policy Capabilities* | [Reviewer comment regarding low overall recovery rate (1.0%–4.7%)] | [Author response citing privileged oracle 100% reachability and active recovery maneuvers] | [Cross-reference to Section 10 and Section 16] | `results/phase_12_stage_c/scenario_manifest.json` | None | `Planned` | Architect | TBD |
| **R3.2** | *Reproducibility* | [Reviewer comment requesting reproduction code, environment specs, or seeds] | [Author response providing release package, Dockerfile, and smoke-test instructions] | [Reference to release/ directory and artifact hash manifest] | `release/REPRODUCE.md`, `manifest.json` | None | `Planned` | Lead Author | TBD |

---

## 3. Reviewer Action Item Protocol

1. **Point-by-Point Transparency:** Never dismiss reviewer feedback; acknowledge validity and provide empirical evidence or formal bounding.
2. **Diff Preservation:** Preserve side-by-side diffs of all manuscript revisions.
3. **Reproducibility Guarantee:** Any additional diagnostic analysis must be added to a dedicated Jupyter notebook and committed to the cryptographic hash manifest.
"""

with open(template_path, 'w', encoding='utf-8') as f:
    f.write(template_text.strip() + '\n')

print(f"Reviewer response template written to {template_path}")

