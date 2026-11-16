#!/usr/bin/env python3
"""
Compute SHA-256 cryptographic hashes for Phase 22 post-submission readiness package,
checklist, manifest, risk plan, timeline, reviewer-response plan, rebuttal plan,
camera-ready plan, notebook, report, and status ledgers.
Outputs to: results/phase_22/phase_22_file_hashes.json
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
    out_dir = os.path.join(repo_root, 'results', 'phase_22')
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'phase_22_file_hashes.json')

    patterns = [
        os.path.join(repo_root, 'docs', 'submission', 'post_submission', '*.md'),
        os.path.join(repo_root, 'docs', 'submission', 'execution', 'final', '*.md'),
        os.path.join(repo_root, 'docs', 'submission', 'execution', '*.md'),
        os.path.join(repo_root, 'docs', 'submission', 'action', '*.md'),
        os.path.join(repo_root, 'docs', 'submission', 'venues', '*', '*.md'),
        os.path.join(repo_root, 'docs', 'submission', '*.md'),
        os.path.join(repo_root, 'docs', 'audit', '*.md'),
        os.path.join(repo_root, 'results', 'phase_21', 'anonymous_release_staging.zip'),
        os.path.join(repo_root, 'docs', 'reports', 'phase_22_post_submission_readiness_report.md'),
        os.path.join(repo_root, 'notebooks', '69_post_submission_readiness_audit.ipynb'),
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
        "phase": "phase_22_post_submission_readiness",
        "description": "Cryptographic SHA-256 provenance manifest for Phase 22 post-submission readiness and reviewer-response preparation",
        "git_status": "No git repository found; cryptographic file hash manifest used as source-file provenance ledger",
        "total_files_hashed": len(hashes),
        "file_hashes": hashes
    }

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f"Hashed {len(hashes)} artifacts -> {out_file}")

if __name__ == '__main__':
    main()
