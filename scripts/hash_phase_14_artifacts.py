#!/usr/bin/env python3
"""
Compute SHA-256 cryptographic hashes for Phase 14 manuscript files,
tables, figures, supplementary materials, reports, checkpoints, and configs.
Outputs to: results/phase_14/phase_14_file_hashes.json
"""

import os
import hashlib
import json
import glob

def hash_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    out_dir = os.path.join(repo_root, 'results', 'phase_14')
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'phase_14_file_hashes.json')

    patterns = [
        os.path.join(repo_root, 'docs', 'manuscript', 'draft', '*'),
        os.path.join(repo_root, 'docs', 'manuscript', 'tables', '*'),
        os.path.join(repo_root, 'docs', 'manuscript', 'references', '*'),
        os.path.join(repo_root, 'docs', 'manuscript', 'submission', '*'),
        os.path.join(repo_root, 'docs', 'manuscript', 'reviews', '*'),
        os.path.join(repo_root, 'docs', 'manuscript', 'figures', '*'),
        os.path.join(repo_root, 'docs', 'manuscript', '*.md'),
        os.path.join(repo_root, 'docs', 'reports', 'phase_14_manuscript_draft_report.md'),
        os.path.join(repo_root, 'configs', 'evaluation', 'stage_c_benchmark.yaml'),
        os.path.join(repo_root, 'results', 'phase_12_stage_c', 'scenario_manifest.json'),
        os.path.join(repo_root, 'results', 'phase_12_stage_c', 'analysis', '*.json'),
        os.path.join(repo_root, 'models', 'checkpoints', '*.pt'),
        os.path.join(repo_root, 'notebooks', '*.ipynb'),
    ]

    hashes = {}
    for pattern in patterns:
        for fpath in glob.glob(pattern):
            if os.path.isfile(fpath):
                relpath = os.path.relpath(fpath, repo_root).replace('\\\\', '/')
                hashes[relpath] = hash_file(fpath)

    manifest = {
        "phase": "phase_14_manuscript_drafting",
        "description": "Cryptographic SHA-256 provenance manifest for Phase 14 manuscript drafting and submission package",
        "git_status": "No git repository found; cryptographic file hash manifest used as source-file provenance ledger",
        "total_files_hashed": len(hashes),
        "file_hashes": hashes
    }

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f"Hashed {len(hashes)} artifacts -> {out_file}")

if __name__ == '__main__':
    main()

