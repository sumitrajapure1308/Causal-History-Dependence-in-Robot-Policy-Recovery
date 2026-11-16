# Research Question Formulation

## 1. Context & Motivation
In contemporary robot manipulation learning, benchmark evaluations increasingly recognize that evaluating policies strictly from nominal initial states gives an incomplete picture of real-world robustness. Recent benchmarks such as **RoboRecover** (arXiv:2409.28952) and **LIBERO-Recover** expose policies to execution deviations and measure whether the robot can continue to task completion.

However, existing recovery evaluations share a foundational assumption:
> **The State-Sufficiency Assumption in Recovery:** Recovery difficulty and success are assumed to be a function solely of the instantaneous physical recovery state $s_t$:
> $$\text{Performance} = f(s_t)$$

This assumption implies that if two robots are placed in the exact same physical failure state (same joint configuration, same object pose, same velocities, and same contact manifold), their recovery challenge is identical, regardless of how they arrived at that state.

In physical and cognitive reality, execution failures are fundamentally **causal processes**. An autonomous agent reaching a state through its own erroneous actions may carry internal momentum, unobserved contact friction states, temporal activation patterns in its hidden memory, or miscalibrated confidence. Conversely, an externally injected state change occurs without any preceding action history.

---

## 2. Primary Research Question
We formulate the core scientific question as:

> **When physically equivalent robot failure states are reached through different execution histories, do robot policies show different detection, diagnosis, recovery, and final task-completion performance?**

Formally, we test whether:
$$\text{State } s^{(A)} \approx s^{(B)} \approx s^{(C)} \implies R^{(A)} = R^{(B)} = R^{(C)}$$
or whether there exists a non-zero history effect:
$$H_R = R_{\text{replay}} - R_{\text{injected}} \neq 0$$

---

## 3. Secondary Research Questions

1. **Prediction from Injected Shifts:** Does a policy's recovery rate under externally injected initial or intermediate perturbations ($R_{\text{injected}}$) reliably predict its recovery rate under its own action-induced failures ($R_{\text{natural}}$)?
2. **The Causal Action Prefix Effect:** How does replaying the exact action prefix ($R_{\text{replay}}$) alter recovery performance relative to direct state injection ($R_{\text{injected}}$) when physical state drift is bounded within $\epsilon$?
3. **Role of Temporal Policy Architecture:** Do history-aware policies (e.g., recurrent LSTM/GRU or frame-stacked architectures) exhibit greater or lesser history dependence than memoryless reactive policies? Does temporal context serve as an error-correcting signal or as a vulnerability to out-of-distribution prefix hysteresis?
4. **Decomposition across Cognitive Stages:** Are failure detection ($D$), failure diagnosis ($Z$), corrective action selection ($C$), and physical recovery ($P$) affected equally by causal history, or does history primarily aid diagnosis while physical recovery remains state-governed?
5. **Benchmark Ranking Stability:** Does causal-history evaluation preserve the relative ranking of robot policies, or do policy rankings invert when moving from prefix-replay / static perturbation benchmarks to counterfactually matched causal history evaluation?
6. **Mitigation via Recovery Training:** Can explicit training on recovery demonstrations neutralize history-dependent performance gaps?
7. **Cross-Modality & Cross-Task Invariance:** Does the degree of history dependence persist across contact-rich versus free-space tasks, and across low-dimensional proprioceptive states versus visual observation spaces?

