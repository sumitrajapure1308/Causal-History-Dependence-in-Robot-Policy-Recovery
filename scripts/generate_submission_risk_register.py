#!/usr/bin/env python3
"""
Generate Submission Risk Register:
docs/submission/submission_risk_register.md
"""

import os

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
risk_path = os.path.join(repo_root, 'docs', 'submission', 'submission_risk_register.md')

risk_text = """# Submission Risk Register & Reviewer Vulnerability Audit

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Repository Root:** `causal-history-recovery/`  
**Phase:** Phase 16 (Final Submission Decision & Journal-Readiness Audit)  
**Status:** `Audited`, `Verified`, `Submission Decision`, `Release Candidate`  
**Target Manuscript:** `docs/manuscript/draft/manuscript.md`  

---

## 1. Executive Summary & Risk Management Strategy

This risk register identifies, categorizes, and provides concrete mitigations for 17 potential scientific and peer-review vulnerabilities across novelty, benchmark overlap, simulation bounding, statistical power, policy capabilities, and generalization.

Every identified risk is assigned a severity (Critical, High, Medium, Low), likelihood (High, Medium, Low), empirical evidence baseline, and actionable mitigation already embedded in the manuscript and release package.

---

## 2. Comprehensive 17-Risk Vulnerability Register

| Risk ID | Risk Domain & Description | Severity | Likelihood | Empirical Evidence | Built-in Mitigation in Manuscript | Required Action for Submission | Owner | Status |
| :---: | :--- | :---: | :---: | :--- | :--- | :--- | :---: | :---: |
| **RSK-01** | **Novelty Claims:** Reviewers perceive contribution as "just another benchmark" or challenge novelty. | Medium | Medium | Literature audit of RoboRecover and LIBERO. | Sec. 6 disclaims "first benchmark"; frames contribution precisely as a matched-state evaluation protocol. | Highlight state-matching precision ($D \le 10^{-10}$) vs unconstrained replay. | Lead Author | `Mitigated` |
| **RSK-02** | **RoboRecover Overlap:** Reviewers argue RoboRecover already evaluated recovery from manipulation failure modes. | High | High | RoboRecover evaluates prompting and restarts without isolating physical state. | Sec. 4.1 explicitly audits RoboRecover across 4 criteria; Table 1 details exact methodological divergence. | Direct reviewer to Table 1 and unconfounded negative control. | Methodologist | `Mitigated` |
| **RSK-03** | **LIBERO-Recover Overlap:** Reviewers cite LIBERO-Recover as prior work evaluating perturbation recovery. | High | Medium | LIBERO-Recover uses coarse task switching without matched-state controls. | Sec. 4.1 contrasts LIBERO-Recover; demonstrates that LIBERO conflates memory unrolling with spatial drift. | Emphasize bitwise state matching ($D \le 10^{-10}$). | Methodologist | `Mitigated` |
| **RSK-04** | **LIBERO-Pro2.0 Overlap:** Reviewers cite LIBERO-Pro2.0 sequential task chaining under object dislodgement. | Medium | Medium | LIBERO-Pro2.0 lacks paired counterfactual interventions ($B_0–B_4$). | Sec. 4.1 and Table 1 establish that our protocol introduces scenario-level paired inference ($N=200$). | Cite paired McNemar formulation and Clopper-Pearson CIs. | Statistician | `Mitigated` |
| **RSK-05** | **Simulation-Only Evidence:** Reviewers reject manuscript due to lack of real-world robotic trials. | **Critical** | **High** | Experiments conducted in MuJoCo simulation. | Abstract and Sec. 17 contain mandatory limitation sentence bounding findings to simulation. | Avoid hardware-mandatory journals (T-RO/IJRR); submit to benchmark tracks (NeurIPS/RSS/RA-L). | Lead Author | `Bounded` |
| **RSK-06** | **Limited Task Diversity:** Benchmark evaluates planar pushing (cube and puck); lacks 6-DoF manipulation. | Medium | High | Tasks restricted to `push_target_cube` and `second_push_puck`. | Sec. 17 explicitly bounds findings to planar pushing; explains contact mechanics in planar regime. | Frame planar pushing as foundational canonical contact benchmark. | Lead Author | `Bounded` |
| **RSK-07** | **Limited Policy Diversity:** Policies limited to MLPs and GRUs; no large VLA models or diffusion policies. | Medium | High | 4 baseline architectures evaluated. | Sec. 11 & 17 explain that memoryless vs recurrent contrast directly isolates internal temporal memory unrolling. | Note that VLA evaluation is natural extension once foundation is established. | Architect | `Bounded` |
| **RSK-08** | **Low Binary Success Rate:** Overall recovery rates among autonomous policies are low ($1.0\%–4.7\%$). | High | High | Floor effects in unconstrained planar pushing without privileged state. | Continuous goal distance error evaluated as co-primary metric; mechanism diagnostics explain physical contact bottleneck. | Emphasize that privileged oracle achieves 100% recovery, proving reachability. | Statistician | `Mitigated` |
| **RSK-09** | **Statistical Power Boundary:** With $N=200$, MDE is $\approx 0.08$; sub-MDE trends ($\Delta R = +0.032$) remain unresolved. | Medium | Medium | Statistical power re-analysis in Phase 11 & 13. | Sec. 17 transparently reports MDE boundary and avoids claiming definitive absence of micro-effects. | Transparently acknowledge MDE in discussion and reviewer responses. | Statistician | `Mitigated` |
| **RSK-10** | **Limited Failure Types:** Deviations restricted to rotational slip and contact loss. | Low | Medium | 2 failure modes evaluated. | Sec. 8 & 15 demonstrate null result holds across both slip and contact loss failure modes. | Frame slip and contact loss as dominant planar failure modes. | Methodologist | `Mitigated` |
| **RSK-11** | **Low-Dimensional Observations:** Policies operate on 10D state vectors rather than raw RGB pixels. | Medium | Medium | Low-dimensional kinematics and object poses. | Decouples representation learning from causal history; eliminates visual occlusion confounds. | Justify state observation as isolating temporal dynamics from visual perception. | Architect | `Mitigated` |
| **RSK-12** | **Simulator-Specific Dynamics:** MuJoCo contact dynamics may exhibit contact solver artifacts. | Medium | Low | MuJoCo convex optimization contact solver. | Exact state matching ($D \le 10^{-10}$) guarantees identical simulator state across compared conditions. | Emphasize within-simulator counterfactual control. | Methodologist | `Mitigated` |
| **RSK-13** | **Absence of Real-Robot Validation:** Reality gap prevents claiming real-robot validity. | **Critical** | **High** | No hardware trials conducted. | Abstract, Sec. 3, Sec. 17 explicitly state findings do NOT establish real-robot validity. | Reject hardware claims; strictly enforce simulation-only bounding in all communications. | Lead Author | `Bounded` |
| **RSK-14** | **Absence of Cross-Simulator Trials:** Benchmark not evaluated on Isaac Gym or PyBullet. | Low | Medium | MuJoCo-only implementation. | Documented as limitation in Sec. 17. | Recommend cross-simulator replication as valuable community contribution. | Lead Author | `Bounded` |
| **RSK-15** | **Absence of Human-Subject Validation:** No user studies on human-in-the-loop recovery. | Low | Low | Fully autonomous policy execution. | Scope restricted to autonomous algorithmic policy recovery. | State that human-in-the-loop recovery is out of scope. | Lead Author | `Not Applicable` |
| **RSK-16** | **Causal Generalization Beyond Intervention:** Overclaiming causality beyond $B_0–B_4$ conditions. | High | Low | Interventions strictly test preserved history vs matched injection. | Sec. 7 defines Pearlian counterfactual interventions; claims strictly restricted to $B_0–B_4$ contrast. | Adhere to exact causal definitions in all discussions. | Statistician | `Mitigated` |
| **RSK-17** | **Generalization Beyond Tested Conditions:** Overclaiming that "history does not matter in robotics". | **Critical** | Medium | Planar manipulation with known physical state. | Sec. 3, 17, 19 repeatedly state history matters in unobserved latent POMDPs (hidden mass/friction changes). | Proactively clarify that POMDPs with changing latent variables require history. | Lead Author | `Mitigated` |

---

## 3. Summary Risk Profile & Pre-Submission Action Items

1. **Target Venue Selection:** Do NOT submit to IEEE T-RO or IJRR without physical robot experiments (RSK-05, RSK-13). Submit to **NeurIPS Datasets & Benchmarks Track**, **Robotics: Science and Systems (RSS)**, or **IEEE Robotics and Automation Letters (RA-L)**.
2. **Reviewer Strategy:** Prepare defensive responses for RSK-02 (RoboRecover) and RSK-08 (low binary success rate), emphasizing paired state matching ($D \le 10^{-10}$) and privileged oracle reachability ($R_\text{oracle} = 1.0$).
3. **Bounding Discipline:** Maintain strict adherence to mandatory limitation sentences and avoid any generalized claims regarding real-world robots.

**Audit Status:** `Submission Decision`, `Journal-Ready Evidence` (`Audited`, `Verified`).
"""

with open(risk_path, 'w', encoding='utf-8') as f:
    f.write(risk_text.strip() + '\n')

print(f"Submission risk register written to {risk_path}")

