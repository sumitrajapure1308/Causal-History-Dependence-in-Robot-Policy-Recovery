# History-Dependent Positive Control Design: Temporary Sensor Occlusion under Planar Contact Failure

**Document ID:** `docs/design/positive_control_design.md`  
**Status:** PROPOSED DESIGN SPECIFICATION (UNEXECUTED)  
**Project:** Causal-History Dependence in Robot Policy Recovery  
**Directory:** `causal-history-recovery/`  
**Purpose:** Design a rigorous, implementable positive control to validate that the matched-state counterfactual evaluation protocol can reliably detect history dependence when execution history provides decision-relevant information absent from the instantaneous observation.

---

## 1. Task Definition

The positive control extends the established tabletop planar manipulation environment ([`PushTargetEnv`](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/src/causal_history_recovery/environments/push_target_env.py)) without altering underlying MuJoCo physics models, friction coefficients, actuator dynamics, or task-success criteria.

- **Base Environment:** A 3-DOF Cartesian pusher interacts with a tabletop object (cube of mass $m = 0.10\text{ kg}$, edge $0.05\text{ m}$) under Coulomb surface friction ($\mu = 0.40$), with the objective of maneuvering the object to a designated planar goal circle ($r_{\text{goal}} = 0.05\text{ m}$) and stabilizing it for a minimum dwell duration ($N_{\text{dwell}} \ge 5$ consecutive timesteps).
- **Failure Induction:** At timestep $t_{\text{perturb}}$ (e.g., $t = 25$), an off-center contact slip or retraction perturbation is physically induced via the verified perturbation schedule, displacing the pusher relative to the object center and initiating contact instability.
- **Informational Disruption (Temporary Sensor Occlusion):** Concurrent with the failure onset at $t_{\text{perturb}}$, a temporary sensor blackout / occlusion window of duration $K_{\text{occ}} = 15$ steps is applied to the observation pipeline (timesteps $[t_{\text{perturb}}, t_{\text{perturb}} + K_{\text{occ}}]$). During this window, object spatial coordinates, orientations, and velocities are masked from the agent's observation vector ($o_t^{\text{obj}} = \mathbf{0}$), while the underlying MuJoCo simulation continues evolving with unperturbed physical fidelity.
- **Evaluation Point ($t_{\text{fail}}$):** The evaluation point is selected within the occlusion window (specifically $t_{\text{fail}} = t_{\text{perturb}} + 5$), at which point the contact slip has physically evolved, the pusher and object have partially separated, and the object's instantaneous position is completely unobservable from the single-frame observation $o_{t_{\text{fail}}}$.
- **Recovery Horizon:** From $t_{\text{fail}}$, the policy must act over the remaining task horizon ($H_{\text{rem}} = H_{\text{max}} - t_{\text{fail}}$) to re-establish stable contact, correct the lateral drift, and complete the target dwell. Sensor visibility is restored at $t_{\text{perturb}} + K_{\text{occ}}$ (10 steps after intervention), forcing the policy to execute initial recovery maneuvers during the blind interval.

---

## 2. Why History Should Help

In the standard benchmark, the observation vector $o_t \in \mathbb{R}^{20}$ provides complete Markovian physical state information (full object coordinates, orientations, and velocities). Under complete Markovian observability, an optimal reactive policy theoretically requires zero past history because the current observation $o_t$ is a sufficient statistic for decision-making.

By contrast, under temporary sensor occlusion:
1. **Instantaneous Ambiguity:** At $t_{\text{fail}}$, the current observation $o_{t_{\text{fail}}}$ conveys zero information regarding where the object is located, which direction it is slipping, or what its residual momentum is. A purely memoryless or reset policy has no mathematical basis to select a directed recovery displacement; any corrective action under $o_{t_{\text{fail}}}$ represents blind random search.
2. **Latent Belief Preservation in History:** The preceding execution prefix $H_{0:t_{\text{fail}}} = \{(o_0, a_0), \dots, (o_{t_{\text{fail}}-1}, a_{t_{\text{fail}}-1})\}$ contains the pre-occlusion trajectory, the approach speed, the contact onset timestep, and the exact sequence of Cartesian pusher displacements leading into the slip.
3. **Dead-Reckoning Capability:** A recurrent policy whose memory ($h(t_{\text{fail}})$) is preserved from prefix unrolling maintains an internal representation of the object's likely displacement vector relative to the pusher. This enables the policy to extrapolate the object's spatial coordinates and execute an informed re-centering maneuver before visual feedback is restored.

Therefore, preserved history provides critical spatial information that is strictly missing from the instantaneous observation at $t_{\text{fail}}$.

---

## 3. What the Current Observation Contains

The instantaneous observation at intervention $t_{\text{fail}}$ is a 20-dimensional vector $o_{t_{\text{fail}}} \in \mathbb{R}^{20}$:

$$\begin{aligned}
o_{t_{\text{fail}}} = [& \underbrace{p_{\text{ee}}}_{\mathbb{R}^3}, \underbrace{v_{\text{ee}}}_{\mathbb{R}^3}, \underbrace{p_{\text{obj}}^{\text{mask}}}_{\mathbb{R}^3}, \underbrace{\phi_{\text{yaw}}^{\text{mask}}}_{\mathbb{R}^2}, \underbrace{v_{\text{obj}}^{\text{mask}}}_{\mathbb{R}^3}, \underbrace{\omega_{\text{obj}}^{\text{mask}}}_{\mathbb{R}^3}, \underbrace{g}_{\mathbb{R}^3} ]
\end{aligned}$$

Where:
- **Observable Pusher State (Indices 0–5):**
  - $p_{\text{ee}} = (x_{\text{ee}}, y_{\text{ee}}, z_{\text{ee}})$: True Cartesian position of the end-effector pusher probe.
  - $v_{\text{ee}} = (\dot{x}_{\text{ee}}, \dot{y}_{\text{ee}}, \dot{z}_{\text{ee}})$: True Cartesian velocity of the end-effector.
- **Masked Object State (Indices 6–16):**
  - $p_{\text{obj}}^{\text{mask}} = (0.0, 0.0, 0.0)$: Object position completely masked.
  - $\phi_{\text{yaw}}^{\text{mask}} = (0.0, 0.0)$: Planar orientation unit vector $[\cos(\psi), \sin(\psi)]$ zeroed.
  - $v_{\text{obj}}^{\text{mask}} = (0.0, 0.0, 0.0)$: Object linear velocity zeroed.
  - $\omega_{\text{obj}}^{\text{mask}} = (0.0, 0.0, 0.0)$: Object angular velocity zeroed.
- **Observable Goal State (Indices 17–19):**
  - $g = (x_g, y_g, z_g)$: Target circle coordinates (static task goal).

The instantaneous observation informs the agent of its own arm configuration and the target goal location, but provides **zero information** regarding the physical whereabouts of the manipulated workpiece.

---

## 4. What the History Contains

The historical trajectory sequence prior to failure intervention comprises:

$$H_{0:t_{\text{fail}}} = \left\{ (o_0, a_0), (o_1, a_1), \dots, (o_{t_{\text{fail}}-1}, a_{t_{\text{fail}}-1}) \right\}$$

This trajectory contains explicit signals that allow latent reconstruction of the object state:
1. **Pre-Occlusion Object Kinematics:** For all $t < t_{\text{perturb}}$, the observations contain unmasked, ground-truth object coordinates $p_{\text{obj}}(t)$, velocities $v_{\text{obj}}(t)$, and heading angles $\psi(t)$.
2. **Applied Action Trajectory:** The exact history of commanded Cartesian pusher displacements $\{a_t\}_{t=0}^{t_{\text{fail}}-1}$. Because pusher dynamics follow stiff position-delta control ($\Delta p = a_t$), the agent's action history encodes the exact volume of work performed on the object.
3. **Contact Slip Onset Time:** The observation transitions immediately preceding $t_{\text{perturb}}$ reveal the onset of pusher deceleration or lateral drift, establishing the initial slip angle.
4. **Recurrent Belief State ($h(t_{\text{fail}})$):** When unrolled through an architecture with recurrent hidden units (e.g., GRU), the hidden vector $h(t_{\text{fail}}) \in \mathbb{R}^{d_{\text{hidden}}}$ encodes an integrated internal belief of the relative pusher-object displacement $(\hat{p}_{\text{obj}} - p_{\text{ee}})$.

---

## 5. Matched Replay and Injection Protocol

To isolate history dependence under this positive control, the environment must satisfy the identical counterfactual matching guarantees established in the primary benchmark:

```
                          t = 0                  t = t_fail               t = H_max
                            |                        |                        |
[A] Replay Preserved:       o=== Replay Prefix =====>[S_fail, h_fail]==== Recovery Rollout ===>
                            (seed S, prefix actions) (D <= 1e-10 m)

[B] Inject Preserved:       [  No Prefix Replay    ]>[S_fail, h_fail]==== Recovery Rollout ===>
                            (direct state injection) (D <= 1e-10 m)

[C] Inject Reset:           [  No Prefix Replay    ]>[S_fail, h = 0 ]==== Recovery Rollout ===>
                            (direct state injection) (D <= 1e-10 m)
```

1. **Replay Condition (`M_REPLAY_PRESERVED`):**
   - The environment is reset with initial seed $S$.
   - The verified action prefix $A_{0:t_{\text{fail}}}$ is stepped sequentially through the simulator.
   - The sensor occlusion filter activates at $t_{\text{perturb}}$, zeroing object observations for $t \in [t_{\text{perturb}}, t_{\text{fail}}]$.
   - At $t_{\text{fail}}$, the simulator reaches physical snapshot $S_{\text{fail}}$, while the policy's recurrent memory is dynamically unrolled to $h(t_{\text{fail}})$.
2. **Matched Injection with Preserved Memory (`M_INJECT_PRESERVED`):**
   - The simulator is directly initialized by injecting physical snapshot $S_{\text{fail}}$ via `PushTargetEnv.restore_state_snapshot(S_fail)`.
   - The physical matching distance is verified to satisfy bitwise tolerance ($D \le 10^{-10}\text{ m}$).
   - The policy's recurrent memory is initialized to $h(t_{\text{fail}})$ via `policy.set_memory_state(mem_unrolled)`.
3. **Matched Injection with Reset Memory (`M_INJECT_RESET`):**
   - The simulator is directly initialized with the identical physical snapshot $S_{\text{fail}}$ ($D \le 10^{-10}\text{ m}$).
   - The policy's recurrent memory is strictly reset to cold start via `policy.reset_memory(o_{t_{\text{fail}}})`, ensuring $h = \mathbf{0}$ and clearing historical action deques.

Because physical states $S_{\text{fail}}$ are bitwise identical between Condition B and Condition C, any divergence in recovery performance between B and C isolates the causal effect of policy memory in overcoming the sensor occlusion.

---

## 6. Policy Memory Preservation and Reset Mechanisms

Memory control relies on the validated interfaces in [`ConditionGenerator`](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/src/causal_history_recovery/counterfactuals/condition_generator.py) and [`BasePolicy`](file:///d:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/src/causal_history_recovery/policies/base_policy.py):

- **Extraction:** Policy memory is extracted using `ConditionGenerator.unroll_policy_memory_on_prefix(policy, seed, action_prefix)`. This unrolls the policy over the prefix with occlusion active and captures a deep copy of the memory dictionary:
  ```python
  mem_state = {
      "hidden_state": policy.get_hidden_state().clone(),
      "obs_buffer": copy.deepcopy(policy.obs_buffer),
      "action_buffer": copy.deepcopy(policy.action_buffer),
  }
  ```
- **Preserved Injection (`M_INJECT_PRESERVED`):** Prior to the first rollout step from $S_{\text{fail}}$, `policy.set_memory_state(mem_state)` is invoked, restoring the unrolled tensor bitwise.
- **Reset Injection (`M_INJECT_RESET`):** `policy.reset_memory(o_{t_{\text{fail}}})` is invoked, setting $h = \mathbf{0}$, populating the observation buffer exclusively with duplicates of $o_{t_{\text{fail}}}$, and zeroing the action history buffer.
- **Memory Leakage Prevention:** Verified by asserting $\|h\| == 0.0$ under Condition C and ensuring successive rollouts are isolated.

---

## 7. Primary Outcome Metric

The primary outcome is the **Paired Counterfactual Recovery Advantage** ($\Delta \text{SR}_{\text{memory}}$):

$$\Delta \text{SR}_{\text{memory}} = \text{SR}(\text{M\_INJECT\_PRESERVED}) - \text{SR}(\text{M\_INJECT\_RESET})$$

Where $\text{SR}(C)$ is the binary task recovery success rate under condition $C$ across the identical matched scenario cohort:

$$\text{SR}(C) = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}\left( \text{Task Success in Scenario } i \text{ under condition } C \right)$$

Secondary quantitative outcomes:
- **Mean Recovery Time ($T_{\text{rec}}$):** Timesteps from $t_{\text{fail}}$ to successful target dwell entry.
- **Terminal Distance to Goal ($d_{\text{goal}}$):** Final Euclidean distance $\|p_{\text{obj}}(H_{\text{max}}) - g\|$ at episode termination.
- **Initial Action Divergence ($\Delta a_0$):** Euclidean difference $\|a_0^{\text{preserved}} - a_0^{\text{reset}}\|$ on the very first action executed at $t_{\text{fail}}$.

---

## 8. Sample-Size and Statistical Power Plan

- **Statistical Test:** Two-sided paired McNemar test for paired binary outcomes across matched scenarios.
- **Design Parameters:**
  - Significance level: $\alpha = 0.01$ (family-wise error controlled).
  - Statistical power: $1 - \beta = 0.95$.
  - Anticipated null success rate (Reset Memory): $\text{SR}_{\text{reset}} \le 0.05$ (5% chance of blind recovery).
  - Minimum detectable effect size: $\Delta \text{SR} \ge 0.25$ (Preserved Memory $\text{SR} \ge 0.30$).
  - Proportion of discordant pairs anticipated: $p_{\text{disc}} \ge 0.30$.
- **Sample Allocation:**
  - $N = 100$ distinct matched failure scenarios (50 under off-center contact slip, 50 under transient contact loss).
  - Each scenario evaluated under paired conditions (Condition B vs. Condition C) using identical random seed streams for post-failure execution.
  - Total evaluation runs: $N \times 2 = 200$ rollouts per policy architecture.

---

## 9. Success Criterion for the Positive Control

The positive control experiment shall be declared valid and conclusive if and only if all four of the following criteria are satisfied:

1. **State Matching Verification:** Maximum physical matching error between replay and injection conditions is bitwise bounded:
   $$\max_{i} D(S_{\text{replay}}^{(i)}, S_{\text{inject}}^{(i)}) \le 10^{-10}\text{ m}$$
2. **Memory Control Verification:**
   - Memory restoration error: $\|h_{\text{restored}} - h_{\text{unrolled}}\| \le 10^{-6}$.
   - Memory reset norm: $\|h_{\text{reset}}\| = 0.0$.
3. **Statistically Significant History Separation:** The paired success advantage is positive and statistically significant:
   $$\Delta \text{SR}_{\text{memory}} \ge 0.20 \quad \text{with} \quad p_{\text{McNemar}} < 0.001$$
4. **Negative Control Invariance:** Under the companion negative-control condition (unoccluded observations), $\Delta \text{SR}_{\text{negative}}$ is not statistically different from zero ($p > 0.05$).

---

## 10. Negative-Control Condition

To ensure that any observed performance advantage in the positive control is caused specifically by the resolution of the partial observability deficit rather than an artifact of hidden state initialization, a companion **Negative-Control Condition** is established:

- **Fully Observable Companion Task:** The identical 100 scenarios are executed with the sensor occlusion filter completely disabled ($K_{\text{occ}} = 0$, observation mask opacity $= 0\%$).
- **Observation Space:** The policy receives the full, unmasked 20-D observation $o_t$ at all timesteps, including $t_{\text{fail}}$.
- **Expected Outcome:** Because the unmasked observation contains the exact object coordinates and velocities, the instantaneous state is fully Markovian. Consequently:
  $$\Delta \text{SR}_{\text{neg}} = \text{SR}_{\text{neg}}(\text{M\_INJECT\_PRESERVED}) - \text{SR}_{\text{neg}}(\text{M\_INJECT\_RESET}) \approx 0$$
- **Purpose:** Demonstrates that when partial observability is absent, the evaluation pipeline yields null history dependence, confirming that the pipeline does not generate false positives.

---

## 11. Risks of Overinterpretation

A rigorous positive control carries explicit interpretation bounds to avoid scientific overclaiming:

1. **Synthetic vs. Intrinsic History Dependence:** Demonstrating that an agent leverages history under an artificial sensor blackout proves that the *evaluation benchmark is sensitive to history dependence when information is missing*. It does **not** prove that the physical dynamics of robot pushing are intrinsically non-Markovian in fully visible settings.
2. **State Estimation vs. Dynamic Memory:** A positive outcome reflects the policy's capacity to function as a latent state estimator (dead-reckoning object position), not that contact friction requires execution-history conditioning.
3. **Architecture-Specific Generalization:** Success on this positive control using a specific GRU model cannot be generalized to claim that all recurrent policies possess robust temporal memory; it only benchmarks the specific checkpoint evaluated.

---

## 12. Required Implementation Changes

Implementation requires zero changes to MuJoCo physics, assets, compilers, or core environments. The modifications are strictly confined to an observation filter wrapper:

1. **`OcclusionEnvWrapper` (`src/causal_history_recovery/environments/occlusion_wrapper.py`):**
   ```python
   class OcclusionEnvWrapper(gym.Wrapper):
       def __init__(self, env: BaseRoboticEnv, occlusion_window: Tuple[int, int]):
           super().__init__(env)
           self.start_step, self.end_step = occlusion_window
           self.mask_indices = slice(6, 17)  # object pos, rot, vel

       def step(self, action):
           obs, reward, term, trunc, info = self.env.step(action)
           if self.start_step <= self.env.step_count <= self.end_step:
               obs = obs.copy()
               obs[self.mask_indices] = 0.0
           return obs, reward, term, trunc, info
   ```
2. **Condition Generator Extension:** Pass the occlusion configuration to `ConditionGenerator` to ensure replay unrolling applies the identical observation masking schedule.
3. **Execution Script (`scripts/run_positive_control_benchmark.py`):** Dedicated evaluation script executing the 100 paired scenarios across Conditions B and C, plus the negative control.

---

## 13. Required Validation Tests

Prior to executing any benchmark rollouts, four unit and integration smoke tests must pass:

1. **`test_occlusion_masking_boundaries`:**
   - Verify that observations for $t < t_{\text{perturb}}$ and $t > t_{\text{perturb}} + K_{\text{occ}}$ are unmasked.
   - Verify that for $t \in [t_{\text{perturb}}, t_{\text{perturb}} + K_{\text{occ}}]$, indices 6–16 are strictly zeroed.
   - Verify that end-effector (0–5) and goal (17–19) indices remain untouched.
2. **`test_physics_invariance_under_masking`:**
   - Execute two parallel simulator runs from the same seed with identical actions: one with occlusion active and one without.
   - Verify that MuJoCo physical coordinates ($q_{\text{pos}}, q_{\text{vel}}$) are bitwise identical at all steps ($D \equiv 0.0\text{ m}$).
3. **`test_occluded_snapshot_restoration`:**
   - Capture a snapshot during the occlusion window.
   - Restore snapshot into a fresh environment.
   - Verify physical state error $D \le 10^{-10}\text{ m}$ and that subsequent step observations maintain correct masking state.
4. **`test_recurrent_memory_determinism_under_occlusion`:**
   - Unroll `RecoveryAugmentedGRUPolicy` twice across the masked prefix.
   - Verify that resulting hidden state tensors match bitwise ($\Delta h \le 10^{-12}$).

---

## 14. Expected Interpretation if the Control Succeeds

If $\Delta \text{SR}_{\text{memory}} \ge 0.20$ ($p < 0.001$) while $\Delta \text{SR}_{\text{neg}} \approx 0$:
- **Harness Sensitivity Validated:** Establishes definitive proof that the matched-state counterfactual evaluation harness possesses sufficient statistical power and measurement precision to detect causal history dependence when such dependence exists.
- **Clarification of Baseline Results:** Re-affirms that the near-zero history dependence observed in the Stage C benchmark was **not** a false negative of an insensitive protocol, but an accurate reflection of the fully Markovian nature of the original state observation space.
- **Methodological Contribution:** Demonstrates a sound paradigm for benchmarking robot policy memory under controlled partial observability.

---

## 15. Expected Interpretation if the Control Fails

If $\Delta \text{SR}_{\text{memory}} \approx 0$ ($p > 0.05$) under complete sensor occlusion:
- **Policy Capacity Diagnostic:** Demonstrates that the trained GRU policy does not possess functional dead-reckoning capabilities. Despite possessing recurrent weights, the network failed to learn an internal state estimator capable of bridging 10 timesteps of missing observations.
- **Scientific Implication:** Proves that merely adding recurrent layers (such as GRU or LSTM) to a policy architecture does not automatically confer usable temporal memory in robotics manipulation tasks unless explicitly trained with state-estimation objectives, auxiliary predictive losses, or domain-randomized sensor dropouts.
- **Preservation of Protocol Validity:** Demonstrates that failure in the positive control is an architectural limitation of the policy rather than a failure of the counterfactual matching framework, motivating architectural improvements rather than modifications to the evaluation methodology.

---

## 16. Protocol Integrity Notice

- **No Benchmark Rerun:** This design document defines a future prospective protocol. No benchmark rollouts have been executed.
- **No Data Alteration:** Stage C benchmark results, scenario manifests, and statistical reports in `results/phase_12_stage_c/` remain strictly immutable.
- **Zero Fabrication:** No empirical numbers, success rates, or p-values are claimed as observed.

