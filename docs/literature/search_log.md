# Literature Search Log

This document records the exact search queries, dates, sources, and key findings used during the literature and novelty audit of `causal-history-recovery`.

---

## Query 1: RoboRecover Benchmark & Execution Deviations
- **Query:** `"RoboRecover" robot recovery execution deviation`
- **Date:** 2026-11-06
- **Engines:** Google Vertex AI Search / ArXiv / GitHub
- **Key Findings:**
  - Paper: *RoboRecover: Benchmarking Robot Policy Recovery under Execution Deviations* (arXiv:2409.28952, Sept 2024 / 2026 preprints).
  - Authors: Renmin University of China, USTC, et al. (GitHub: `RUCKBReasoning/RoboRecover`).
  - Approach: Evaluates policy recovery from off-nominal intermediate states by replaying action prefixes in LIBERO and RoboTwin.
  - Scale: 2,000 scenarios (1,000 in LIBERO, 1,000 in RoboTwin; 800/200 train/test split per benchmark).
  - Key Observation: Standard initial-state performance does not predict recovery performance from intermediate deviations.
  - Critical Gap for Our Work: RoboRecover evaluates *only* replayed execution deviation start points (equivalent to our Condition B). It **does not** perform counterfactual state-matched injection without history (Condition C), nor does it calculate history-dependence metrics $H_R = R_{\text{replay}} - R_{\text{injected}}$, nor does it decompose recovery into detection vs. diagnosis vs. correction.

---

## Query 2: LIBERO-Recover Benchmark
- **Query:** `"LIBERO-Recover" robot policy failure recovery benchmark`
- **Date:** 2026-11-06
- **Engines:** Google Vertex AI Search / ArXiv / GitHub
- **Key Findings:**
  - Focus: Evaluates failure recovery across four progressive hierarchical levels:
    1. Action Retry (repeating failed action under minimal scene change)
    2. Action Adaptation (adjusting planned action for minor state shift)
    3. Object State Recovery (restoring displaced/dropped object state)
    4. Environmental Recovery (resolving broader environment/workspace disruptions)
  - Scenarios: Over 2,000 failure-recovery scenarios evaluated on VLA and World-Action models.
  - Critical Gap for Our Work: Focuses on hierarchical task-level recovery taxonomies and scene restoration from fixed/preset failure conditions. It does not control for the causal history of the failure or isolate physical state equivalence from preceding action prefixes.

---

## Query 3: LIBERO-Pro & LIBERO-Pro2.0
- **Query:** `"LIBERO-Pro" OR "LIBERO-Pro2.0" robot perturbation benchmark`
- **Date:** 2026-11-06
- **Engines:** Google Vertex AI Search / ArXiv / HuggingFace
- **Key Findings:**
  - Focus: Tests embodied foundation models and VLAs against 22 static distribution shifts and 20 runtime interventions (1,648 validated shifted instances across condition, environment, observation, execution, robot-state, and language dimensions). Includes 39,390 robustness training trajectories.
  - Findings: Reports significant performance drops (~26.5% average degradation) under runtime perturbations.
  - Critical Gap for Our Work: Evaluates robustness under runtime shifts and static perturbations, but does not conduct matched-state counterfactual comparisons between action-prefix-induced failures and state-injected failures.

---

## Query 4: Causal & Counterfactual Evaluation in Robot Manipulation
- **Query:** `"RoboRecover" "matched state" OR "counterfactual" OR "causal history" OR "same state"`
- **Date:** 2026-11-06
- **Engines:** Google Vertex AI Search / Preprints / ArXiv
- **Key Findings:**
  - While counterfactual concepts are discussed in abstract reinforcement learning (offline RL, trajectory relabeling), in robotic manipulation benchmarks, "same state" has meant either identical starting poses or replaying the exact prefix.
  - **No existing benchmark has performed a controlled paired comparison between: (1) an action-prefix replayed failure state, and (2) an identical physical state directly injected without history, while decomposing detection, diagnosis, and correction.**
  - The research niche is confirmed to be wide open, highly defensible, and sharply defined.

