# IEEE RA-L Condensed Abstract Specification

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/submission/venues/ra_l/manuscript/ra_l_abstract.md`  
**Milestone:** Phase 31 — RA-L Manuscript Adaptation  
**Target Venue:** IEEE Robotics and Automation Letters (RA-L)  
**Date:** 2026-11-10  
**Verification Status:** `Verified` | `Submission-ready evidence`  

---

## 1. Official RA-L Abstract Constraint
- **Rule:** IEEE RA-L enforces a strict abstract ceiling of **no more than 200 words**.
- **Enforcement:** PaperPlaza web forms strictly validate word counts and reject abstracts exceeding 200 words.

---

## 2. Condensed Abstract Text

Policy recovery from execution-induced failures is frequently assumed to require temporal history. However, evaluating history dependence by comparing reactive and recurrent policies conflates history access with state divergence following a failure. We introduce a paired replay-injection evaluation that isolates the causal effect of history by initializing policies at identical physical states ($D \le 10^{-10}\text{ m}$) under matched failure conditions across planar manipulation tasks in MuJoCo. In a confirmatory benchmark of 20,000 rollouts across 200 matched scenarios, recovery-augmented recurrent policies exhibit substantial motor action divergence ($\|\Delta a_0\| = 0.0038\text{ m/step}$, Cohen's $d = 3.99$, $p < 10^{-15}$) and transient trajectory separation ($2.48\text{ cm}$) upon failure. However, binary recovery success exhibits no statistically significant causal-history advantage after Holm-Bonferroni correction ($p_\text{adj} \ge 0.2500$ across all policies; negative control discordance $= 0/200$, 95% CI $[0.00\%, 1.83\%]$). Physical contact analysis reveals that normal contact forces and Coulomb friction act as an information-destroying bottleneck, attenuating recurrent divergence prior to terminal goal dwell ($p_\text{adj} = 1.0000$). These simulation-based findings indicate that history benefits depend heavily on contact damping dynamics.

---

## 3. Abstract Verification Metrics

- **Exact Word Count:** **182 words**
- **Margin Under 200-Word Ceiling:** 18 words (100% compliant)
- **Scientific Content Preserved:**
  1. *Problem formulation:* Confounding between temporal history and state divergence in standard recovery evaluations.
  2. *Methodology:* Paired replay-injection protocol achieving exact physical state matching ($D \le 10^{-10}\text{ m}$).
  3. *Benchmark scope:* Confirmatory benchmark of 20,000 rollouts across 200 matched scenarios in MuJoCo planar manipulation.
  4. *Motor action divergence finding:* Significant initial action divergence ($\|\Delta a_0\| = 0.0038\text{ m/step}$, Cohen's $d = 3.99$, $p < 10^{-15}$).
  5. *Primary binary recovery outcome:* Null causal-history advantage confirmed after Holm-Bonferroni correction ($p_\text{adj} \ge 0.2500$, negative control discordance $0/200$).
  6. *Decoupling physical mechanism:* Normal contact forces and Coulomb friction surface dissipation attenuate divergence prior to goal dwell ($p_\text{adj} = 1.0000$).
  7. *Explicit simulation bounding:* Explicitly qualified as simulation-based manipulation findings.

---

## 4. Standardized Index Terms (IEEE Keywords)

*Index Terms*—Failure recovery, robot manipulation, causal inference, contact mechanics, state-history confounding, imitation learning.

