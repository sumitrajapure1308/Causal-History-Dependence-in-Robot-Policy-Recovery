#!/usr/bin/env python3
"""
Compute SHA-256 cryptographic hashes for Phase 21 final submission execution deliverables,
pre-upload gate, anonymization scrub, staging bundle, Zenodo reservation, OpenReview upload plan,
monitoring plan, notebook, report, and status ledgers.
Outputs to: results/phase_21/phase_21_file_hashes.json
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
    out_dir = os.path.join(repo_root, 'results', 'phase_21')
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'phase_21_file_hashes.json')

    patterns = [
        os.path.join(repo_root, 'docs', 'submission', 'execution', 'final', '*.md'),
        os.path.join(repo_root, 'docs', 'submission', 'execution', '*.md'),
        os.path.join(repo_root, 'docs', 'submission', 'action', '*.md'),
        os.path.join(repo_root, 'docs', 'submission', 'venues', '*', '*.md'),
        os.path.join(repo_root, 'docs', 'submission', '*.md'),
        os.path.join(repo_root, 'docs', 'audit', 'final_pre_upload_gate.md'),
        os.path.join(repo_root, 'docs', 'audit', 'anonymization_scrub_audit.md'),
        os.path.join(repo_root, 'results', 'phase_21', 'anonymous_release_staging.zip'),
        os.path.join(repo_root, 'docs', 'reports', 'phase_21_submission_execution_report.md'),
        os.path.join(repo_root, 'notebooks', '68_final_submission_execution.ipynb'),
        os.path.join(repo_root, 'PROJECT_STATUS.md'),
        os.path.join(repo_root, 'docs', 'decision_log.md'),
    ]

    hashes = {}
    for pattern in patterns:
        for fpath in glob.glob(pattern):
            if os.path.isfile(fpath):
                relpath = os.path.relpath(fpath, repo_root).replace('\\', '/')
                hashes[relpath] = hash_file(fpath)

    manifest = {
        "phase": "phase_21_final_submission_execution",
        "description": "Cryptographic SHA-256 provenance manifest for Phase 21 final submission execution",
        "git_status": "No git repository found; cryptographic file hash manifest used as source-file provenance ledger",
        "total_files_hashed": len(hashes),
        "file_hashes": hashes
    }

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f"Hashed {len(hashes)} artifacts -> {out_file}")

if __name__ == '__main__':
    main()

