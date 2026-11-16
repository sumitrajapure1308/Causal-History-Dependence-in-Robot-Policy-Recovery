# Reviewer Response Template: RSS

**Venue:** Robotics: Science and Systems (RSS)  
**Status:** `Submission-ready evidence`  
**Date:** 2026-11-10  

---

## Standard Rebuttal Matrix for Anticipated Critiques

### Critique 1: "The findings are based entirely on simulation without real robot hardware experiments."
- **Author Response:** We agree that hardware validation is an essential future milestone. However, our primary scientific objective is to perform a rigorous counterfactual isolation of execution history by holding the physical state invariant. On physical hardware, exact physical state injection to sub-millimeter precision without reset hysteresis or sensor tracking noise is physically intractable. Simulation in MuJoCo permits sub-atomic state matching ($D \le 1.0 \times 10^-10$ m) and bitwise determinism ($D = 0.0$), mathematically isolating the temporal history confound. We have explicitly bounded our claims in Section 5.1 and Section 6 as simulation-based counterfactual evaluations.
- **Manuscript Change:** Clarified the necessity of sub-atomic simulation matching in Section 1 and Section 5.1.
- **Evidence Source:** Table 1, Table 7, and `docs/audit/real_robot_readiness_audit.md`.
- **Status:** `Verified`.

### Critique 2: "A null result (no binary recovery difference) is uninteresting or shows that the policies simply failed."
- **Author Response:** We respectfully emphasize that our evaluation does not represent a simple policy failure:
  1. The policies evaluated include **Recovery-Augmented policies** achieving up to 24.5% recovery with 45% active re-alignment maneuvers (Table 5).
  2. The recurrent policy exhibits **massive, statistically significant motor action divergence** ($\|\Delta a_0\| = 0.0038$ m/step, Cohen's $d = 3.99$, $p < 10^-15$) and intermediate trajectory separation ($2.48$ cm, $d = 0.754$), proving that the recurrent network's internal memory is active and divergent.
  3. Our contribution is the **mechanistic discovery** that physical Coulomb friction and normal force constraints act as an information bottleneck that dampens this divergence before terminal goal dwell.
- **Manuscript Change:** Expanded Section 4.4 and Section 7 detailing the physical decoupling mechanism.
- **Evidence Source:** Figure 5, Figure 6, Figure 7, Table 4.
- **Status:** `Verified`.

### Critique 3: "How does this differ from RoboRecover or LIBERO-Recover?"
- **Author Response:** As detailed in our related work audit, RoboRecover and LIBERO-Recover evaluate end-to-end recovery from perturbed initial states or action prefix replays, but **never match the instantaneous physical state** visited under different history conditions. Consequently, observed recovery differences in those benchmarks confound physical state divergence with history dependence. Our work introduces Paired Replay-Injection to hold physical state invariant, providing the missing counterfactual control.
- **Manuscript Change:** Added a comparative taxonomy table in Section 2 explicitly citing RoboRecover and LIBERO-Recover.
- **Evidence Source:** `docs/audit/novelty_overlap_audit.md`.
- **Status:** `Verified`.

---
*Template certified by Autonomous Agent System.*
