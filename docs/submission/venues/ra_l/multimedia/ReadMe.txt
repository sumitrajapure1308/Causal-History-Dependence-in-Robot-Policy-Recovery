IEEE ROBOTICS AND AUTOMATION LETTERS (RA-L) MULTIMEDIA PACKAGE
=============================================================
Article Title: Causal-History Dependence in Robot Policy Recovery:
               A Matched-State Evaluation under Execution-Induced Failures
Authors: Lead Researcher, Systems Engineer, Robotics Lead, Principal Investigator
Contact: causal.history.recovery@gmail.com

CONTENTS OF THIS PACKAGE
------------------------
1. video/causal_history_recovery_demo.mp4
   - High-definition (720p, 30 fps, H.264/MP4) visualization of the matched-state
     recovery protocol and physical damping dynamics.
   - Panel 1: End-effector and object trajectories comparing nominal execution,
     unperturbed replay, and matched recovery post-injection.
   - Panel 2: Motor action divergence ||Delta a_t|| over the recovery horizon.
   - Panel 3: Normal contact force F_N and Coulomb friction energy dissipation.

2. code/
   - Lightweight evaluation and verification suite.
   - smoke_test.py: Bitwise determinism and sub-atomic state matching test (D <= 1e-10 m).
   - environment.yml: Conda environment specification.
   - requirements.txt: Pip dependencies.
   - src/: Core model architectures, match engine, and simulation dynamics.
   - checkpoints/: Policy weights for Reactive MLP, History LSTM, Trajectory Transformer, and Diffusion.

3. data/
   - scenario_manifests/: Benchmark configuration manifests for Stage C evaluation (N=200 pairs).
   - summary/: Benchmark summary statistics and Holm-Bonferroni adjusted p-values.

SYSTEM REQUIREMENTS
-------------------
- Operating System: Linux (Ubuntu 20.04/22.04), macOS 12+, or Windows 10/11 (64-bit)
- Python Version: 3.10 or 3.11
- Disk Space: ~50 MB uncompressed
- Media Player: VLC, Windows Media Player, QuickTime, or any modern web browser for MP4.

EXECUTION INSTRUCTIONS
----------------------
To run the automated verification smoke test:
   python code/smoke_test.py

Expected runtime: < 5 seconds.
Verification output confirms bitwise state matching (residual D <= 1.0e-10 m)
and deterministic policy action rollouts.

NOTE ON SUPPLEMENTAL MATERIAL
-----------------------------
In compliance with IEEE RA-L author instructions, this multimedia package
does NOT contain any supplemental text, extended derivations, proofs, or
extra figures. All documentation is strictly instructional for video playback
and code verification. Extended appendices are archived separately in the
permanent Zenodo repository (DOI: 10.5281/zenodo.10892341).
