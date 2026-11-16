# Policy Checkpoints Specification

Pre-trained model checkpoints are stored in `models/checkpoints/`:

| Checkpoint Name | Policy Architecture | Hidden Dims | Input Dim | Output Dim | Parameters | Training Dataset | Primary Role |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `reactive_mlp_best.pt` | 2-layer MLP | 64 | 10 | 2 | ~5,000 | Nominal demonstrations | Negative Control |
| `history_gru_best.pt` | 1-layer GRU | 64 | 10 | 2 | ~17,000 | Nominal demonstrations | Nominal Recurrent Baseline |
| `recovery_augmented_mlp_best.pt` | 2-layer MLP | 64 | 10 | 2 | ~5,000 | Augmented recovery dataset | Recovery-Trained Memoryless |
| `recovery_augmented_gru_best.pt` | 1-layer GRU | 64 | 10 | 2 | ~17,000 | Augmented recovery dataset | Recovery-Trained Recurrent |

All checkpoints load seamlessly via `load_policy(path)` and run on standard CPU architecture.
