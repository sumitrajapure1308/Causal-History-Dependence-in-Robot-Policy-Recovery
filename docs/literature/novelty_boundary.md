# Novelty Boundaries & Publication Strategy Freeze

> **Publication Target:** Q1 Robotics Journal (e.g. IEEE Transactions on Robotics [T-RO], Autonomous Robots [AURO], Robotics and Autonomous Systems [RAS])  
> **Scientific Stance:** Cautious, Defensible, and Strictly Bounded  
> **Status:** BOUNDARY FROZEN FOR PHASE 1

---

## 1. What Already Exists in Prior Work (Do NOT Claim as Novel)

| Technique / Concept in Prior Work | Prior Literature Anchor | Explicit Citation & Boundary Directive |
|---|---|---|
| **Reconstructing execution deviations via action-prefix replay** | RoboRecover (arXiv:2409.28952) | Do **not** claim execution-prefix recovery as novel. RoboRecover explicitly pioneered this. Use RoboRecover as our Condition B baseline. |
| **Hierarchical multi-tier recovery categorization (retry, adaptation, etc.)** | LIBERO-Recover | Do **not** claim recovery taxonomy as the core novelty. |
| **Static & runtime perturbation suites** | LIBERO-Pro / LIBERO-Pro2.0 | Do **not** claim runtime disturbance injection as novel. |
| **Counterfactual memory auditing via trajectory crossing** | CMA (arXiv:2609.27247) | Do **not** claim counterfactual history auditing in the abstract is novel; CMA applied it to nominal task instruction memory. |
| **Test-time causal history scaling in WAMs** | FARE (arXiv:2609) | Do **not** claim that intervening on causal history in robot models has never been studied; FARE explored KV-cache pruning as an inference method. |
| **Simulation state serialization and restoration in MuJoCo** | MuJoCo native API / Gymnasium | Standard simulation engineering; not a scientific contribution. |

---

## 2. What is Potentially New (Our Focused Research Niche)

1. **Matched-State Counterfactual Protocol:** A protocol that takes an execution-induced failure state reached via action prefix replay (Condition B) and directly pairs it with a physically matched state reached without that action history (Condition C), holding the instantaneous physical Markov state invariant within $\epsilon$-tolerances.
2. **The Causal-History Dependence Metric ($H_R$):** The quantitative differential $H_R = R_{\text{replay}} - R_{\text{injected}}$, isolating the specific performance delta attributable to the causal prefix versus the instantaneous physical state.
3. **Recovery Validity Audit:** Testing whether existing recovery benchmarks produce distorted policy quality rankings ($\tau < 1.0, \rho < 1.0$) because they evaluate only replayed prefixes or only injected shifts in isolation.
4. **Decomposed Detection-Diagnosis-Recovery Stage Metrics:** Quantifying whether causal history selectively assists failure detection ($D$) or diagnosis ($Z$), while physical recovery ($P$) remains state-governed.

---

## 3. The Provisional Central Contribution Statement

The paper's contribution is strictly defined as:

> **“A physically matched-state evaluation protocol for measuring the effect of controlled causal-history interventions on robot recovery.”**

- **What It Is:** A methodological validity audit and diagnostic benchmark protocol for robot policy recovery.
- **What It Is NOT:**
  - NOT "the first causal-history recovery method".
  - NOT a claim of introducing a new robot policy architecture.
  - NOT "the first recovery benchmark".
  - NOT a proof of real-world universal causality.

---

## 4. Prohibited Claims Until Official Experiments are Completed

Contributors, autonomous agents, and manuscript drafts MUST strictly refrain from making the following claims:
1. **NO CLAIMS OF NOVELTY AS "VERIFIED":** Label novelty as *provisional* until empirical experiments demonstrate that $H_R$ provides statistically significant discriminative power beyond standard benchmarks.
2. **NO HARDWARE / SIM-TO-REAL CLAIMS:** Initial experiments are strictly simulation-based. No claims regarding physical robot transfer or real-world validity are permitted.
3. **NO PREMATURE SUPERIORITY CLAIMS:** Do not claim that any policy family (e.g., recurrent vs. reactive) is universally superior until multi-seed, multi-task experiments are executed and analyzed.
4. **NO AD-HOC SCOPE EXPANSION:** Do not inject unrelated modules (e.g. diffusion policies, large language models, or tactile skins) merely to artificially inflate perceived novelty.

