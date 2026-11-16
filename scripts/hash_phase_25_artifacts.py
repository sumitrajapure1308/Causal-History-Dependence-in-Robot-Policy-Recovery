#!/usr/bin/env python3
"""
Compute SHA-256 cryptographic hashes for all Phase 25 artifacts and related files.
Outputs to results/phase_25/phase_25_file_hashes.json.
"""

import os
import hashlib
import json
from datetime import datetime, timezone

def hash_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Target directories and explicit files
    target_dirs = [
        os.path.join(repo_root, 'docs', 'submission', 'execution', 'final'),
        os.path.join(repo_root, 'docs', 'submission', 'action'),
        os.path.join(repo_root, 'docs', 'submission', 'final_decision'),
        os.path.join(repo_root, 'docs', 'audit'),
        os.path.join(repo_root, 'release'),
        os.path.join(repo_root, 'results', 'phase_25')
    ]
    
    explicit_files = [
        os.path.join(repo_root, 'PROJECT_STATUS.md'),
        os.path.join(repo_root, 'docs', 'decision_log.md'),
        os.path.join(repo_root, 'docs', 'reports', 'phase_25_submission_execution_report.md'),
        os.path.join(repo_root, 'docs', 'reports', 'phase_24_submission_action_report.md'),
        os.path.join(repo_root, 'docs', 'manuscript', 'draft', 'manuscript.md'),
        os.path.join(repo_root, 'docs', 'manuscript', 'supplementary_materials.md'),
        os.path.join(repo_root, 'docs', 'manuscript', 'references', 'references.bib'),
        os.path.join(repo_root, 'results', 'phase_12_stage_c', 'scenario_manifest.json'),
        os.path.join(repo_root, 'results', 'phase_12_stage_c', 'evaluation_summary.json'),
        os.path.join(repo_root, 'results', 'phase_12_stage_c', 'paired_comparisons.json'),
        os.path.join(repo_root, 'results', 'phase_13', 'paper_tables.json'),
        os.path.join(repo_root, 'results', 'phase_21', 'anonymous_release_staging.zip'),
        os.path.join(repo_root, 'notebooks', '72_final_submission_execution_audit.ipynb'),
        os.path.join(repo_root, 'notebooks', '71_final_submission_action_plan_audit.ipynb'),
        os.path.join(repo_root, 'scripts', 'build_phase_25_notebook.py'),
        os.path.join(repo_root, 'scripts', 'build_phase_24_notebook.py')
    ]
    
    files_to_hash = set()
    for d in target_dirs:
        if os.path.exists(d):
            for root, _, files in os.walk(d):
                for f in files:
                    if f.endswith(('.md', '.json', '.py', '.yml', '.yaml', '.txt', 'Dockerfile', '.ipynb', '.zip')):
                        if f != 'phase_25_file_hashes.json':
                            files_to_hash.add(os.path.join(root, f))
                            
    for ef in explicit_files:
        if os.path.exists(ef):
            files_to_hash.add(ef)
            
    records = []
    for fp in sorted(files_to_hash):
        rel = os.path.relpath(fp, repo_root).replace('\\', '/')
        sz = os.path.getsize(fp)
        sha = hash_file(fp)
        records.append({
            'file': rel,
            'size_bytes': sz,
            'sha256': sha
        })
        
    out_dir = os.path.join(repo_root, 'results', 'phase_25')
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'phase_25_file_hashes.json')
    
    payload = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'phase': 'Phase 25 — Final Submission Execution',
        'file_count': len(records),
        'manifest': records
    }
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
        
    print(f"Hashed {len(records)} artifacts to {out_file}")

if __name__ == '__main__':
    main()

