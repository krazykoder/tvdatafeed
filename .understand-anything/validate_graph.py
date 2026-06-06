#!/usr/bin/env python3
"""
Final graph validation before saving.
"""

import json
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path("/Users/towshif/code/python/tvdatafeed")
INTERMEDIATE_DIR = PROJECT_ROOT / ".understand-anything" / "intermediate"

print("[Phase 6/7] Validating knowledge graph...")

# Load all components
with open(INTERMEDIATE_DIR / 'assembled-graph.json') as f:
    graph = json.load(f)

with open(INTERMEDIATE_DIR / 'layers.json') as f:
    layers = json.load(f)

with open(INTERMEDIATE_DIR / 'tour.json') as f:
    tour = json.load(f)

nodes = graph.get('nodes', [])
edges = graph.get('edges', [])

# Collect all node IDs
node_ids = set(n['id'] for n in nodes)

print(f"  Nodes: {len(nodes)}")
print(f"  Edges: {len(edges)}")
print(f"  Layers: {len(layers)}")
print(f"  Tour steps: {len(tour)}")

# Validation
issues = []

# Validate layers
print("\n  Validating layers...")
for layer in layers:
    if not layer.get('id'):
        issues.append(f"Layer missing id: {layer.get('name')}")
    if not layer.get('name'):
        issues.append(f"Layer missing name: {layer.get('id')}")
    if not layer.get('description'):
        issues.append(f"Layer '{layer.get('name')}' missing description")
    
    # Check nodeIds
    for node_id in layer.get('nodeIds', []):
        if node_id not in node_ids:
            issues.append(f"Layer '{layer['name']}' references missing node '{node_id}'")

# Validate tour
print("  Validating tour steps...")
for i, step in enumerate(tour):
    if 'order' not in step:
        issues.append(f"Tour step {i} missing order")
    if not step.get('title'):
        issues.append(f"Tour step {i} missing title")
    if not step.get('description'):
        issues.append(f"Tour step {i} missing description")
    
    for node_id in step.get('nodeIds', []):
        if node_id not in node_ids:
            issues.append(f"Tour step '{step.get('title')}' references missing node '{node_id}'")

# Statistics
file_level_types = {'file', 'config', 'document', 'service', 'pipeline', 'table', 'schema', 'resource', 'endpoint'}
file_nodes = [n for n in nodes if n['type'] in file_level_types]

print(f"\n  File-level nodes: {len(file_nodes)}")

# Check coverage
files_in_layers = set()
for layer in layers:
    for node_id in layer.get('nodeIds', []):
        for n in nodes:
            if n['id'] == node_id and n['type'] in file_level_types:
                files_in_layers.add(n['id'])

uncovered_files = set(n['id'] for n in file_nodes) - files_in_layers
if uncovered_files:
    print(f"  Uncovered files: {len(uncovered_files)}")
    for f_id in list(uncovered_files)[:3]:
        print(f"    - {f_id}")

# Generate validation report
validation_report = {
    'timestamp': '2026-05-25T16:00:00Z',
    'graphSize': {
        'nodes': len(nodes),
        'edges': len(edges),
        'layers': len(layers),
        'tourSteps': len(tour)
    },
    'nodeTypes': dict(sorted(__import__('collections').Counter(n['type'] for n in nodes).items())),
    'edgeTypes': dict(sorted(__import__('collections').Counter(e['type'] for e in edges).items())),
    'issues': issues,
    'issueCount': len(issues),
    'filesCoverage': {
        'total': len(file_nodes),
        'inLayers': len(files_in_layers),
        'uncovered': len(uncovered_files)
    },
    'validated': True if len(issues) == 0 else False
}

review_file = INTERMEDIATE_DIR / 'review.json'
with open(review_file, 'w') as f:
    json.dump(validation_report, f, indent=2)

print(f"\n  Issues found: {validation_report['issueCount']}")
print(f"  Status: {'✓ VALID' if validation_report['validated'] else '✗ NEEDS FIXES'}")

print(f"\n✓ Phase 6 complete")
print(f"  Review: {review_file}")
