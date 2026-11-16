# Submission Cover Letter

**To:** Track Chairs, NeurIPS Track on Datasets and Benchmarks  
**Venue:** Neural Information Processing Systems (NeurIPS) — Track on Datasets and Benchmarks  
**Date:** 2026-11-10  
**Submission Type:** Benchmark and Evaluation Track Submission  

**Title:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  

Dear Track Chairs, NeurIPS Track on Datasets and Benchmarks,

We submit our manuscript, titled **"Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures"**, for review in **Neural Information Processing Systems (NeurIPS) — Track on Datasets and Benchmarks**.

### Research Question:
Does execution history causally improve or alter policy recovery when physical state is strictly held constant?

### Main Contribution:
This work introduces the **Paired Replay-Injection Matching protocol**, a counterfactual evaluation methodology that holds physical robot and object simulation states strictly invariant to sub-atomic precision ($D \le 1.0 \times 10^-10$ m) while selectively ablating temporal execution history.

### Main Empirical Finding:
Across 20,000 confirmatory rollouts ($N=200$ matched scenarios), execution history confers no statistically significant binary recovery advantage ($p_{adj} \ge 0.2500$) or continuous goal distance improvement ($p_{adj} = 1.0000$), despite significant internal recurrent action divergence (\|\Delta a_0\| = 0.0038 m/step, Cohen's d = 3.99, p < 10^{-15}).

### Novelty and Distinction from Prior Benchmarks:
Resolves physical state-history confounding present in existing benchmarks (RoboRecover, LIBERO-Recover) via sub-atomic state matching ($D \le 10^{-10}$ m) and memoryless negative controls ($0/200$ discordant). We do not claim to introduce recovery as a benchmark task; rather, we provide the first controlled causal audit of whether recurrent history representations are necessary for recovery.

### Key Limitation & Scope of Validity:
Explicitly bounded to simulation-based planar rigid-body manipulation; real-world robot hardware trials and multi-simulator transfers remain future work.

### Reproducibility, Data, and Code Availability:
All 20,000 confirmatory rollouts, pre-trained policy weights, scenario manifests, and standalone reproduction scripts are open-sourced under the MIT License in our release package. A 2.75-second automated smoke test verifies exact state matching and bitwise determinism across platforms.

### Declarations:
- **Conflict of Interest:** The authors declare that they have no competing financial interests or personal relationships that could have appeared to influence this work.
- **Funding:** This research was conducted independently with no restrictive sponsor oversight.
- **Author Contributions:** Mapped using the CRediT taxonomy in the supplementary materials.
- **Ethical Considerations:** Purely computational research on simulated tabletop manipulators; zero human or animal subjects involved.

We thank you and the reviewers for considering this work for NeurIPS Datasets & Benchmarks.

Sincerely,  
*The Authors*
