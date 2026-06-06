#!/usr/bin/env python3
"""
Validate assembled graph for completeness and correctness.
Produces assemble-review.json.
"""

import json
from pathlib import Path
from collections import defaultdict, Counter

PROJECT_ROOT = Path("/Users/towshif/code/python/tvdatafeed")
INTERMEDIATE_DIR = PROJECT_ROOT / ".understand-anything" / "intermediate"

# Load graph
graph_file = INTERMEDIATE_DIR / 'assembled-graph.json'
with open(graph_file) as f:
    graph = json.load(f)

nodes = graph.get('nodes', [])
edges = graph.get('edges', [])

print("[Phase 3/7] Reviewing assembled graph...")

issues = []
warnings = []
recommendations = []

# Validate nodes
print(f"\n  Validating {len(nodes)} nodes...")
node_ids = set()
node_types = Counter()
nodes_by_type = defaultdict(list)

for i, node in enumerate(nodes):
    # Check required fields
    if not node.get('id'):
        issues.append(f"Node[{i}] missing id")
        continue
    
    node_ids.add(node['id'])
    node_types[node.get('type', 'unknown')] += 1
    nodes_by_type[node.get('type', 'unknown')].append(node['id'])
    
    if not node.get('type'):
        issues.append(f"Node '{node['id']}' missing type")
    if not node.get('name'):
        issues.append(f"Node '{node['id']}' missing name")
    if not node.get('summary'):
        warnings.append(f"Node '{node['id']}' missing summary")
    if not node.get('tags'):
        warnings.append(f"Node '{node['id']}' missing tags")

# Validate edges
print(f"  Validating {len(edges)} edges...")
edge_types = Counter()
dangling = 0

for i, edge in enumerate(edges):
    source = edge.get('source')
    target = edge.get('target')
    edge_type = edge.get('type', 'related')
    
    edge_types[edge_type] += 1
    
    if source not in node_ids:
        issues.append(f"Edge[{i}] source '{source}' not found")
        dangling += 1
    if target not in node_ids:
        issues.append(f"Edge[{i}] target '{target}' not found")
        dangling += 1

print(f"\n  Summary:")
print(f"    Nodes: {len(nodes)} ({dict(node_types)})")
print(f"    Edges: {len(edges)} ({dict(edge_types)})")
print(f"    Issues: {len(issues)}")
print(f"    Warnings: {len(warnings)}")
print(f"    Dangling edges: {dangling}")

# File coverage
file_nodes = [n for n in nodes if n['type'] == 'file']
files_in_inventory = set()
try:
    with open(INTERMEDIATE_DIR / 'scan-result.json') as f:
        scan = json.load(f)
        files_in_inventory = set(f['path'] for f in scan.get('files', []))
except:
    pass

print(f"\n  File coverage:")
print(f"    Files in inventory: {len(files_in_inventory)}")
print(f"    File nodes in graph: {len(file_nodes)}")

missing_files = files_in_inventory - set(n.get('filePath', '') for n in file_nodes)
if missing_files:
    print(f"    Missing from graph: {len(missing_files)}")
    for f in list(missing_files)[:5]:
        print(f"      - {f}")

# Recommendations
if dangling > 0:
    recommendations.append(f"Remove {dangling} dangling edges")
if len(issues) > 0:
    recommendations.append("Fix validation issues")
if any('untagged' in n.get('tags', []) for n in nodes):
    recommendations.append("Add tags to untagged nodes")

# Write review
review = {
    'timestamp': json.dumps({}),  # Will be replaced with actual timestamp
    'graphSize': {
        'nodes': len(nodes),
        'edges': len(edges)
    },
    'issues': issues[:50],  # Limit to first 50
    'warnings': warnings[:50],
    'issueCount': len(issues),
    'warningCount': len(warnings),
    'nodeTypesCount': dict(node_types),
    'edgeTypesCount': dict(edge_types),
    'recommendations': recommendations,
    'filesCoverage': {
        'total': len(files_in_inventory),
        'inGraph': len(file_nodes),
        'missing': len(missing_files)
    }
}

review_file = INTERMEDIATE_DIR / 'assemble-review.json'
with open(review_file, 'w') as f:
    json.dump(review, f, indent=2)

print(f"\n✓ Phase 3 complete")
print(f"  Review: {review_file}")
