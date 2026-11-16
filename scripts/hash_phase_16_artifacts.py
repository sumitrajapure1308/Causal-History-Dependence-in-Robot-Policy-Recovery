#!/usr/bin/env python3
"""
Compute SHA-256 cryptographic hashes for Phase 16 submission decision files,
audits, cover letter, risk register, report, and notebook.
Outputs to: results/phase_16/phase_16_file_hashes.json
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
    out_dir = os.path.join(repo_root, 'results', 'phase_16')
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'phase_16_file_hashes.json')

    patterns = [
        os.path.join(repo_root, 'docs', 'submission', '*'),
        os.path.join(repo_root, 'docs', 'audit', 'final_*'),
        os.path.join(repo_root, 'docs', 'reports', 'phase_16_submission_decision_report.md'),
        os.path.join(repo_root, 'notebooks', '63_final_reproducibility_audit.ipynb'),
    ]

    hashes = {}
    for pattern in patterns:
        for fpath in glob.glob(pattern):
            if os.path.isfile(fpath):
                relpath = os.path.relpath(fpath, repo_root).replace('\\\\', '/')
                hashes[relpath] = hash_file(fpath)

    manifest = {
        "phase": "phase_16_submission_decision",
        "description": "Cryptographic SHA-256 provenance manifest for Phase 16 final submission decision and journal-readiness audit",
        "git_status": "No git repository found; cryptographic file hash manifest used as source-file provenance ledger",
        "total_files_hashed": len(hashes),
        "file_hashes": hashes
    }

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f"Hashed {len(hashes)} artifacts -> {out_file}")

if __name__ == '__main__':
    main()

