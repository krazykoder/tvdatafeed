#!/usr/bin/env python3
"""
Compute semantic batches from scan result for parallel analysis.
Produces batches.json compatible with the understand-anything pipeline.
"""

import json
import math
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path("/Users/towshif/code/python/tvdatafeed")
INTERMEDIATE_DIR = PROJECT_ROOT / ".understand-anything" / "intermediate"
SCAN_RESULT_FILE = INTERMEDIATE_DIR / "scan-result.json"
OUTPUT_FILE = INTERMEDIATE_DIR / "batches.json"

# Load scan result
with open(SCAN_RESULT_FILE) as f:
    scan_result = json.load(f)

files = scan_result['files']
import_map = scan_result.get('importMap', {})

print(f"[Phase 1.5/7] Computing semantic batches...")
print(f"  Total files: {len(files)}")

# Group files by language and category for better batching
code_files = [f for f in files if f['fileCategory'] == 'code']
config_files = [f for f in files if f['fileCategory'] == 'config']
doc_files = [f for f in files if f['fileCategory'] == 'docs']
data_files = [f for f in files if f['fileCategory'] in ['data', 'script', 'markup']]

print(f"  Code files: {len(code_files)}, Config: {len(config_files)}, Docs: {len(doc_files)}, Other: {len(data_files)}")

# Create batches - group related files together
# Batch strategy: ~8-12 files per batch, keep related files together
TARGET_BATCH_SIZE = 10
BYTES_PER_LINE_ESTIMATE = 50  # bytes per source line

def create_batches(file_list, batch_name_prefix=""):
    """Create semantic batches from file list."""
    if not file_list:
        return []
    
    batches = []
    current_batch = []
    current_size = 0
    MAX_BATCH_LINES = 5000
    
    for file_info in file_list:
        file_size = file_info.get('sizeLines', 100)
        
        if current_batch and current_size + file_size > MAX_BATCH_LINES and len(current_batch) >= 3:
            batches.append(current_batch)
            current_batch = []
            current_size = 0
        
        current_batch.append(file_info)
        current_size += file_size
    
    if current_batch:
        batches.append(current_batch)
    
    return batches

# Create batches for each category
all_batches = []
batch_idx = 0

# Code files get priority
for batch_files in create_batches(code_files, "code"):
    all_batches.append({
        'index': batch_idx,
        'category': 'code',
        'files': batch_files
    })
    batch_idx += 1

# Config files
for batch_files in create_batches(config_files, "config"):
    all_batches.append({
        'index': batch_idx,
        'category': 'config',
        'files': batch_files
    })
    batch_idx += 1

# Documentation  
for batch_files in create_batches(doc_files, "docs"):
    all_batches.append({
        'index': batch_idx,
        'category': 'docs',
        'files': batch_files
    })
    batch_idx += 1

# Data files
for batch_files in create_batches(data_files, "data"):
    all_batches.append({
        'index': batch_idx,
        'category': 'data',
        'files': batch_files
    })
    batch_idx += 1

# Build neighbor map - track which files import from which other files
neighbor_map = defaultdict(lambda: {'neighbors': {}, 'exports': []})

for file_path, imports in import_map.items():
    for other_file in [f['path'] for f in files]:
        if file_path == other_file:
            continue
        # Check if this file might export to the importing file
        other_name = other_file.replace('/', '_').replace('.py', '')
        if any(imp in other_name or other_name in imp for imp in imports):
            if other_file not in neighbor_map[file_path]['neighbors']:
                neighbor_map[file_path]['neighbors'][other_file] = {
                    'confidence': 0.7,
                    'reason': 'likely cross-batch dependency'
                }

# Create batches output with neighbor data
batches_output = {
    'version': '1.0.0',
    'totalFiles': len(files),
    'batches': []
}

for batch_info in all_batches:
    batch_files = batch_info['files']
    batch_paths = [f['path'] for f in batch_files]
    
    # Find neighbors for this batch (files that import/are imported by files in batch)
    neighbor_data = {}
    for file_info in batch_files:
        path = file_info['path']
        if path in neighbor_map:
            neighbor_data[path] = neighbor_map[path]
    
    batch = {
        'index': batch_info['index'],
        'category': batch_info['category'],
        'batchFiles': batch_files,
        'batchImportData': {
            path: import_map.get(path, [])
            for path in batch_paths
        },
        'neighborMap': neighbor_data,
        'estimatedTokens': sum(f.get('sizeLines', 100) * 2 for f in batch_files)  # rough estimate
    }
    batches_output['batches'].append(batch)

# Write output
with open(OUTPUT_FILE, 'w') as f:
    json.dump(batches_output, f, indent=2)

print(f"\n✓ Phase 1.5 complete. Created {len(batches_output['batches'])} batches")
for batch in batches_output['batches']:
    files_in_batch = len(batch['batchFiles'])
    tokens = batch['estimatedTokens']
    print(f"  Batch {batch['index']}: {files_in_batch} files (~{tokens} tokens)")

print(f"\nBatches written to: {OUTPUT_FILE}")
