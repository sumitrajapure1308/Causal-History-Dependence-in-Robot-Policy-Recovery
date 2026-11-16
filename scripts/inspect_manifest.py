import hashlib
import os
import json

files = [
    'docs/manuscript/draft/manuscript.md',
    'docs/manuscript/supplementary_materials.md',
    'docs/manuscript/references/references.bib',
    'results/phase_12_stage_c/scenario_manifest.json',
    'results/phase_12_stage_c/evaluation_summary.json',
    'results/phase_12_stage_c/paired_comparisons.json',
    'results/phase_13/paper_tables.json',
    'figures/benchmark/paper/fig_paper_01_method_pipeline.pdf',
    'figures/benchmark/paper/fig_paper_03_state_matching.pdf',
    'figures/benchmark/paper/fig_paper_05_recovery_success_by_policy.pdf',
    'figures/benchmark/paper/fig_paper_07_recovery_success_by_failure_type.pdf',
    'models/checkpoints/reactive_mlp_best.pt',
    'models/checkpoints/history_gru_best.pt',
    'models/checkpoints/recovery_augmented_mlp_best.pt',
    'models/checkpoints/recovery_augmented_gru_best.pt',
    'release/smoke_test.py',
    'release/Dockerfile',
    'release/environment.yml',
    'release/run_all.py',
    'results/phase_21/anonymous_release_staging.zip',
    'docs/submission/final_decision/final_submission_decision.md',
    'docs/submission/final_decision/journal_readiness_gate.md'
]

root = r'D:\PROJECT\CASUAL HISTORY IN ROBOT POLICY RECOVERY\causal-history-recovery'
out = []
for rel in files:
    full = os.path.join(root, rel)
    if os.path.exists(full):
        sz = os.path.getsize(full)
        h = hashlib.sha256(open(full, 'rb').read()).hexdigest()
        out.append({'path': rel, 'size': sz, 'sha256': h})
    else:
        print('MISSING:', rel)

with open(os.path.join(root, 'results', 'phase_24', 'inspected_manifest_hashes.json'), 'w') as f:
    json.dump(out, f, indent=2)

print(f"Successfully inspected {len(out)} files.")

