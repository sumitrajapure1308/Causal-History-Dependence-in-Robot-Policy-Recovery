# Submission Cover Letter

**Date:** November 10, 2026  
**To:** The Editorial Board / Program Committee  
**Submission Venue:** Robotics: Science and Systems (RSS) / NeurIPS Datasets and Benchmarks Track / IEEE Robotics and Automation Letters (RA-L)  
**Submission Type:** Original Research / Benchmark and Evaluation Methodology Track  

---

**Manuscript Title:**  
*Matched-State Causal-History Evaluation of Robot Policy Recovery under Execution-Induced Failures*

**Corresponding Author:**  
Causal-History Policy Recovery Research Contributors  
Repository: `causal-history-recovery/`  

---

Dear Editors and Program Chairs,

We submit for your consideration our manuscript entitled *“Matched-State Causal-History Evaluation of Robot Policy Recovery under Execution-Induced Failures”* as an original contribution to the benchmark, evaluation, and robot learning literature.

### 1. Research Question & Methodological Core
In autonomous continuous manipulation, unexpected execution deviations (such as kinematic slip or contact stall) inevitably occur. When policies fail to recover, standard evaluation protocols restart executions or replay trajectories, introducing an acute methodological confound: the coupling of the instantaneous physical state with the preceding execution history. This paper investigates the fundamental research question:
*“When physically equivalent failure states are reached through different execution histories, do robot policies exhibit different detection, diagnosis, recovery, and final task-completion performance?”*

### 2. Main Contribution & Novelty Distinction
To address this gap without overclaiming universal properties, our contribution is:
*“A matched-state causal-history evaluation protocol that compares preserved execution history, prefix replay, and physically matched state injection under controlled conditions.”*

We explicitly do NOT claim a "first benchmark" or "first recovery benchmark"; rather, we frame our work relative to recent benchmarks (RoboRecover, LIBERO-Recover, and LIBERO-Pro2.0), providing the exact bitwise physical state matching ($D \le 1.0 	imes 10^{-10}	ext{ m}$) necessary to decouple history prefix effects from physical state configurations.

### 3. Empirical Results & Findings
In an extensive pre-registered confirmatory benchmark comprising 20,000 rollouts across 200 independently mined scenarios, 2 manipulation tasks, 2 failure modes, and 4 policy architectures:
*“Under the tested policies, tasks, and matched-state protocol, binary recovery success and final goal error were history-invariant, although preserved recurrent history changed immediate control behavior and object trajectories.”*

Paired scenario-level McNemar exact tests with Holm-Bonferroni correction confirmed no statistically detectable binary advantage for preserved history ($p_	ext{adj} \ge 0.2500$ across all 4 policies). Our unconfounded memoryless negative control (`reactive_mlp`) achieved exactly 0/200 discordant pairs ($0.00\%$, Clopper-Pearson 95% CI $[0.00\%, 1.83\%]$), verifying zero leakage in the evaluation harness. While recurrent memory unrolling reconstructed internal hidden states ($\|h\| pprox 0.8805$) and induced initial action divergence ($\|\Delta a_0\| = 0.0038	ext{ m/step}$, Cohen's $d = 3.99$) and $2.48	ext{ cm}$ path divergence, downstream Coulomb friction and normal force constraints attenuated this kinematic variance before the terminal goal basin.

### 4. Key Limitations & Bounding
We maintain strict scientific bounding throughout the manuscript:
*“The results are simulation-based and limited to the tested tasks, policies, failure modes, and matched-state protocol; they do not establish real-robot validity or generalization beyond these conditions.”*
We do not claim real-world robotic validity or universal applicability to unobserved non-Markovian dynamics where physical parameters (e.g. mass, friction) vary dynamically within an episode.

### 5. Reproducibility & Open Artifacts
Complete reproducibility is guaranteed through an open, verified release package (`release/`):
- Complete raw rollout logs ($20,000$ JSONL records, $15.5	ext{ MB}$).
- 4 trained policy checkpoints in `models/checkpoints/`.
- 14 publication paper figures at 600 DPI (PDF vector + PNG).
- 7 structured publication tables (Markdown + JSON).
- 63 fully executed Jupyter notebooks with visible outputs.
- Standalone Docker container specification (`Dockerfile` and `docker-compose.yml`).
- Automated smoke test (`scripts/run_smoke_test.py`) executing in $pprox 2.5	ext{s}$ with bitwise determinism ($D=0.0$).

### 6. Disclosures & Statements
- **Author Contributions:** Detailed in Section 18 and submission checklist.
- **Conflict of Interest:** The authors declare no competing financial or personal interests.
- **Funding Statement:** This research was conducted independently without external commercial sponsorship.
- **Ethical Considerations:** Simulation-only robotics study; no human or animal subjects involved.
- **Data & Code Availability:** Complete data and source code are open-source under the MIT License.

We look forward to the constructive feedback of the reviewers.

Sincerely,  
*The Causal-History Policy Recovery Research Contributors*
