# Matched-State Causal-History Evaluation of Robot Policy Recovery under Execution-Induced Failures

**Status:** `Release Candidate`, `Submission-Ready Evidence`, `Pre-Registered`, `Confirmatory`  
**License:** MIT License  
**Repository Root:** `causal-history-recovery/`  

---

## Abstract & Research Core

Autonomous robot manipulation policies frequently experience execution failures caused by kinematic slips and contact disruptions during contact-rich tasks. Standard recovery benchmarks evaluate failure behaviors by restarting executions or replaying trajectories, thereby confounding the instantaneous physical state with the preceding execution history. We formulate a matched-state causal-history evaluation protocol that decouples physical state from execution history using bitwise simulator snapshots with residual matching error below 1e-10. Across two planar pushing manipulation tasks and two distinct execution failure modes (rotational slip and contact loss), 200 recoverable scenarios were mined and verified under privileged oracle reachability. Four policy architectures—reactive MLP, nominal GRU, recovery-augmented MLP, and recovery-augmented GRU—were systematically evaluated across five counterfactual intervention history conditions (B0 to B4) spanning 20,000 confirmatory rollouts. Under the tested policies, tasks, and matched-state protocol, binary recovery success and final goal error were history-invariant, although preserved recurrent history changed immediate control behavior and object trajectories. Paired scenario-level McNemar exact tests confirmed no statistically significant binary advantage for preserved history over direct matched injection across all policy architectures (adjusted p >= 0.2500). Continuous final goal distance errors exhibited negligible differences (adjusted p = 1.0000, Cohen's d <= 0.137). Mechanism diagnostics revealed that recurrent unrolling reconstructed internal representations and induced immediate action divergence (0.0038 m/step) and trajectory divergence (2.48 cm); however, downstream Coulomb friction and normal contact constraints attenuated this kinematic variance before the terminal goal basin. The results are simulation-based and strictly limited to the tested settings. Complete open-source code, checkpoints, seeds, and cryptographic manifests ensure complete scientific reproducibility.

---

## Core Research Question
“When physically equivalent failure states are reached through different execution histories, do robot policies exhibit different detection, diagnosis, recovery, and final task-completion performance?”

## Main Contribution
“A matched-state causal-history evaluation protocol that compares preserved execution history, prefix replay, and physically matched state injection under controlled conditions.”

---

## Quickstart & Verification

```bash
# 1. Install dependencies
pip install -r release/requirements.txt
pip install -e .

# 2. Run automated smoke test
python scripts/run_smoke_test.py

# 3. Run complete test suite (67 tests)
pytest tests -v
```

---

## Limitations
“The results are simulation-based and limited to the tested tasks, policies, failure modes, and matched-state protocol; they do not establish real-robot validity or generalization beyond these conditions.”

---

## Disclosures & Statements
- **Ethical Considerations:** Simulation-only robotics research without human or animal subjects.
- **Conflict of Interest:** The authors declare no competing financial or personal interests.
- **Funding:** Conducted as an independent robotics research project.
- **Data Availability:** Complete 20,000 rollout records are available in `results/phase_12_stage_c/rollouts/`.
- **Code Availability:** All source code, configs, notebooks, and models are open-source under the MIT License.
