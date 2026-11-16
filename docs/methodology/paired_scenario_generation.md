# Paired Replay-Injection Matching Strategy

> **Document Type:** Research Methodology Specification  
> **Project:** Causal-History Dependence in Robot Policy Recovery  
> **Phase:** 5 (Paired Scenario Generation & Matching-Yield Optimization)  
> **Status:** `Verified & Operational`  
> **Core Innovation:** Guaranteed Physical State Matching by Construction via Deterministic Replay and Lossless State Injection.

---

## 1. Scientific Rationale: The Failure of Accidental Matching

In Phase 4, the audit of passive cross-episode matching confirmed that searching for matching failure states across independent stochastic rollouts yields an effective yield of **0.0%**. In continuous 19-dimensional multi-body state space with discrete contact chattering, the likelihood of two independent rollouts intersecting within a tolerance ball of $\epsilon \le 0.05$ is effectively zero.

Attempting to relax the tolerance threshold to $\epsilon > 0.10$ would introduce massive physical state discrepancies, completely confounding any comparison of recovery performance.

To overcome this fundamental barrier, Phase 5 transitions from passive observational matching to **Paired Replay-Injection Matching**.

---

## 2. The 13-Step Paired Generation Protocol

The paired replay-injection strategy guarantees physical state equivalence by construction:

```
[Source Rollout]
t=0 ---------- t_pert ---------- t_d (Deviation Detected)
                                  |
                                  +--> Evaluate Oracle Recoverability (R_oracle == 1)
                                  |
                                  +--> Extract Snapshot s(t_d), Obs Hist, Act Hist,
                                       Contact Hist, Hidden State h(t_d), Horizon T - t_d, Goal g
                                  |
    +-----------------------------+-----------------------------+
    |                             |                             |
[Condition B0]              [Condition B1]                [Condition B4]
Deterministic Prefix        Action History                Direct State Injection s(t_d)
Replay -> Full History      Ablated (Zeroed)              All History Erased (h=0)
Physical State: s(t_d)      Physical State: s(t_d)        Physical State: s(t_d)
State Error: D = 0.0        State Error: D = 0.0          State Error: D = 0.0
```

For each candidate failure episode:
1. **Run Policy Execution:** Execute policy $\pi$ in the environment from seed $s$.
2. **Detect Recoverable Deviation:** Monitor object kinematics for off-center contact slip ($\theta \ge \theta_{\text{thresh}}$, $\Delta y \ge \Delta y_{\text{thresh}}$) at step $t_d$.
3. **Capture Physical State Snapshot:** Save full MuJoCo simulation coordinates $s(t_d) = (\mathbf{q}_{\text{pos}}, \mathbf{q}_{\text{vel}}, \mathbf{a}_{\text{act}}, \mathbf{w}_{\text{warmstart}})$.
4. **Save Observation History:** Archive observation buffer sequence $\mathbf{o}_{t_d-k:t_d}$.
5. **Save Action History:** Archive action prefix sequence $\mathbf{a}_{0:t_d-1}$.
6. **Save Contact History:** Record active contact manifolds and normal forces leading up to $t_d$.
7. **Save Policy Hidden State:** Extract recurrent memory tensor $\mathbf{h}(t_d)$.
8. **Save Remaining Horizon:** Record exact remaining steps $H_{\text{rem}} = T_{\max} - t_d$.
9. **Save Task Goal:** Record target goal vector $\mathbf{g}$.
10. **Oracle Recoverability Gate:** Run Privileged Oracle Controller from $s(t_d)$. Only proceed if $R_{\text{oracle}} = 1$.
11. **Replay Action Prefix (Conditions B0–B3):** Reset environment to seed $s$, step actions $\mathbf{a}_{0:t_d-1}$ open-loop to reproduce exact physical dynamics.
12. **Direct State Injection (Condition B4):** Reset fresh environment, inject $s(t_d)$ bitwise losslessly, and re-synchronize kinematics (`mj_forward`).
13. **Apply Controlled History Interventions:**
    - **B0:** Intact history $(\mathbf{o}, \mathbf{a}, \mathbf{h})$.
    - **B1:** Action history masked ($\mathbf{a}_{\text{hist}} \gets \mathbf{0}$).
    - **B2:** Observation history masked ($\mathbf{o}_{\text{hist}} \gets \mathbf{o}_{t_d}$).
    - **B3:** Policy recurrent hidden state reset ($\mathbf{h} \gets \mathbf{0}$).
    - **B4:** Complete history erased $(\mathbf{o}_{\text{reset}}, \mathbf{a}_{\mathbf{0}}, \mathbf{h}_{\mathbf{0}})$.

---

## 3. Mathematical Equivalence Guarantee

Under this protocol, the physical initial-state distance between any two conditions $C_a, C_b \in \{\text{B0}, \text{B1}, \text{B2}, \text{B3}, \text{B4}\}$ is:
$$D_{\text{phys}}(s_{C_a}(t_d), s_{C_b}(t_d)) = 0.0000000000$$

Because physical initial conditions are identical, any divergence in subsequent policy recovery metrics ($R_{C_a} \neq R_{C_b}$) is **strictly attributable to the causal history intervention**.

---

## 4. Scenario Data Architecture & Storage Schema

Each paired scenario is assigned a globally unique Scenario ID (`scen_<policy>_s<seed>_t<td_step>_<uuid>`) and serialized into `results/paired_scenarios/scenarios/<scenario_id>/`:
- `snapshot.npz`: Complete generalized coordinates and velocities.
- `metadata.json`: Scenario parameters, failure severity tier, deviation metrics, oracle verification report.
- `conditions/`: Subdirectory storing rollout logs and metrics for B0, B1, B2, B3, B4.

The collective dataset is indexed by `results/paired_scenarios/scenario_manifest.json` and validated by `results/paired_scenarios/validation_report.json`.

