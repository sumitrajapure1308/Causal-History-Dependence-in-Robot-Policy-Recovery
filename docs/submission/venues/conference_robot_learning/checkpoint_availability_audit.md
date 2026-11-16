# Checkpoint Availability Audit: CoRL

**Venue:** Conference on Robot Learning (CoRL)  
**Status:** `Verified` | `Submission-ready evidence`  
**Date:** 2026-11-10  

---

- **Model Checkpoints:** Pre-trained PyTorch weights stored in `models/checkpoints/`:
  - `reactive_mlp_best.pt` (81,869 bytes, SHA-256 verified)
  - `history_gru_best.pt` (272,843 bytes, SHA-256 verified)
  - `recovery_augmented_mlp_best.pt` (87,461 bytes, SHA-256 verified)
  - `recovery_augmented_gru_best.pt` (282,037 bytes, SHA-256 verified)
- **Seeds:** Checkpoints across training seeds 42, 123, 456 preserved in `results/recovery_training/checkpoints/`
- **Compliance:** Verified loadable via standard PyTorch CPU tensors.

---
*Audit certified by Autonomous Agent System.*
