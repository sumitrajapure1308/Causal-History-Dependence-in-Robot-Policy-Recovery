# Direct Overlap Analysis: Prior Art vs. Causal-History Recovery

> **Status:** PROVISIONALLY PROMISING — DIRECT OVERLAP REQUIRES DETAILED COMPARISON  
> **Audited Literature:**
> 1. *Counterfactual Auditing of History-Conditioned Robot Policies* (arXiv:2609.27247, CMA)
> 2. *Causal-History Test-Time Scaling for Failure Recovery in Autoregressive World-Action Models* (FARE)
> 3. *RoboRecover: Benchmarking Robot Policy Recovery under Execution Deviations* (arXiv:2409.28952)
> 4. *LIBERO-Recover: Benchmarking Failure Recovery in Embodied Manipulation*
> 5. *LIBERO-Pro / LIBERO-Pro2.0: Robustness Evaluation Under Distribution Shifts*

---

## 1. 13-Dimension Systematic Comparison Matrix

| Evaluation Dimension | CMA (arXiv:2609.27247) | FARE (Test-Time Scaling) | RoboRecover (arXiv:2409.28952) | LIBERO-Recover | LIBERO-Pro2.0 | **Proposed Protocol (Causal History Recovery)** |
|---|---|---|---|---|---|---|
| **1. Physical state matching** | Observation reconvergence on nominal tasks | State anchor matching in WAM latent space | Reconstructs single state via replay; no cross-condition match | Preset scenario layouts | Runtime perturbation states | **Rigorous physical state matching: $d(s_1, s_2) \le \epsilon$ across $q, \dot{q}, p, R, v, \omega, c, g$** |
| **2. History construction** | Contrasts two distinct nominal demonstration paths | Unrolls autoregressive rollout until execution drift | Replays single recorded action prefix | None (fixed starting scenes) | Runtime disturbance injected into live trajectory | **Constructs natural rollout history, replayed prefix history, and history-free injection** |
| **3. History alteration** | Swaps past memory banks between reconverging trajectories | Truncates KV history suffix; replaces with historical anchor | None (history is fixed and unmanipulated) | None | Injects disturbances into ongoing execution | **Counterfactual intervention: Preserved prefix vs. erased/reset history at matched physical states** |
| **4. Policy memory reset** | Yes (swaps or clears memory store) | Yes (rewinds KV cache to anchor point) | No (memory state inherits replayed prefix execution) | Initialized at episode start | None (continuous execution) | **Explicitly manipulated: Retained in Condition B, fully reset in Condition C, windowed in Condition D** |
| **5. Observation-history reset**| Crossed between alternative trajectory paths | Corrupted observation tokens pruned | Replayed prefix observations provided | Fresh observation stream from failure scene | Corrupted observations (occlusion, noise) | **Controlled: Current only ($k=1$), short ($k=2,5$), full sequence, or masked** |
| **6. Action-history reset** | Crossed between alternative paths | Action tokens rewound to anchor | Preserved via prefix replay | Fresh start from scene | Continues post-perturbation | **Ablated: Present in replayed prefix; erased/zeroed in matched injection** |
| **7. State injection** | No (evaluates at natural trajectory reconvergence) | No (physical system remains at drifted state; model KV cache is edited) | No (state reached strictly via prefix replay) | Yes (direct reset to preset failure scene) | Yes (forces/impulses injected mid-task) | **Yes: Direct physical state injection matching the exact kinematic/dynamic recovery state** |
| **8. Action-prefix replay** | Yes (replays distinct prefixes to test memory guidance) | No (online test-time search over history hypotheses) | Yes (core mechanism to reconstruct failure states) | No | No | **Yes: Used in Condition B to preserve causal action history before recovery handoff** |
| **9. Recovery evaluation** | No (evaluates memory guidance on nominal tasks) | Yes (evaluates test-time algorithmic recovery of WAMs) | Yes (evaluates task completion from replayed deviation) | Yes (evaluates completion across 4 recovery tiers) | Yes (evaluates completion under runtime shifts) | **Yes: Evaluates recovery success rate (RSR) and recovery cost across causal conditions** |
| **10. Detection evaluation** | No (not focused on failure detection) | Yes (progress-aware recovery trigger monitors drift) | No | Implicit (policy must act appropriately) | Implicit | **Yes: Explicit evaluation of detection accuracy, AUROC, AUPRC, detection delay $D_{\text{delay}}$** |
| **11. Diagnosis evaluation** | No | Limited (identifies unreliable token suffix) | No | Categorical tier placement (retry vs. adaptation) | Limited | **Yes: Explicit multi-class failure diagnosis ($Z$) and contact-mode accuracy** |
| **12. Final task success** | Evaluates warranted choice on nominal tasks | Evaluates final success under test-time scaling | Evaluates task success from deviation state | Evaluates task success per tier | Evaluates task success under perturbation | **Yes: Evaluated through decomposed stages: $P(F) = P(D)P(Z \mid D)P(C \mid Z,D)\dots$** |
| **13. Policy-ranking stability**| Evaluates memory sensitivity metrics across policies | No (benchmarks FARE algorithm on WAMs) | Evaluates policy success rates; no cross-protocol correlation | Evaluates rank within recovery tiers | Evaluates performance drop percentages | **Yes: Formal rank correlation ($\tau, \rho$) testing if benchmark rankings invert under causal control** |

---

## 2. Granular Distinction from Closely Related Prior Art

### A. Distinction from *Counterfactual Auditing of History-Conditioned Robot Policies* (CMA)
- **What CMA Does:** CMA tests whether history-conditioned policies genuinely use memory to guide action on nominal multi-path tasks (e.g., *Put Back* and *Swap*). It crosses past memory banks at observation reconvergence points to check if the policy selects the warranted action.
- **What Our Work Does Differently:**
  1. CMA investigates *nominal task memory guidance* (which drawer to open based on past instructions), whereas our work investigates *physical failure recovery* under execution-induced dynamics (contact slip, jamming, grasp failures).
  2. CMA matches observations at reconvergence points in clean tasks; our work matches the complete physical state (generalized coordinates, velocities, contact forces) of *off-nominal failure configurations*.
  3. CMA does not evaluate failure detection, failure diagnosis, or recovery success metrics ($H_R$).

### B. Distinction from *Causal-History Test-Time Scaling for Failure Recovery* (FARE)
- **What FARE Does:** FARE is an *algorithmic inference method* designed specifically for autoregressive World-Action Models (WAMs). It detects execution drift online and performs test-time search over history KV-cache configurations (complete vs. recovered-prefix vs. full-reset) to recover the model's predictive ability.
- **What Our Work Does Differently:**
  1. FARE is a *policy improvement technique / inference algorithm*; our project is an *evaluation benchmark and scientific audit protocol*.
  2. In FARE, the physical robot remains in its drifted physical state while only the internal autoregressive KV cache is manipulated. In our work, we manipulate the physical execution history leading to a matched physical state to test whether standard policies (reactive, recurrent, recovery-trained) exhibit history dependence.
  3. FARE does not evaluate state-matched counterfactual injection vs. replay, nor does it evaluate policy-ranking stability across benchmark suites.

### C. Distinction from *RoboRecover*
- **What RoboRecover Does:** RoboRecover established the importance of execution deviations by collecting 2,000 scenarios in LIBERO and RoboTwin and reconstructing them by replaying action prefixes.
- **What Our Work Does Differently:**
  1. RoboRecover strictly evaluates *replayed prefixes* (Condition B). It assumes that recovery is a function of that intermediate state.
  2. RoboRecover **never** injects an identical physical state without history (Condition C). It cannot answer whether recovery succeeded because of the physical state or because of the action prefix.
  3. RoboRecover does not decompose recovery into detection and diagnosis, nor does it define history-dependence metrics ($H_R$).

### D. Distinction from *LIBERO-Recover* and *LIBERO-Pro2.0*
- **What They Do:** LIBERO-Recover categorizes recovery into 4 hierarchical levels from static presets. LIBERO-Pro2.0 tests 22 static and 20 runtime perturbations.
- **What Our Work Does Differently:**
  1. Neither framework matches physical states across different execution histories.
  2. Neither framework isolates action prefixes from state configurations.
  3. Our project audits whether benchmarks of this type produce stable or misleading policy evaluations by ignoring causal history.

