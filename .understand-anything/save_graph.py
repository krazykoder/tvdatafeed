#!/usr/bin/env python3
"""
Assemble final knowledge graph and save.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path("/Users/towshif/code/python/tvdatafeed")
INTERMEDIATE_DIR = PROJECT_ROOT / ".understand-anything" / "intermediate"
OUTPUT_DIR = PROJECT_ROOT / ".understand-anything"

print("[Phase 7/7] Saving knowledge graph...")

# Load all components
with open(INTERMEDIATE_DIR / 'assembled-graph.json') as f:
    graph = json.load(f)

with open(INTERMEDIATE_DIR / 'layers.json') as f:
    layers = json.load(f)

with open(INTERMEDIATE_DIR / 'tour.json') as f:
    tour = json.load(f)

# Get commit hash
try:
    commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], 
                                         cwd=PROJECT_ROOT, text=True).strip()
except:
    commit_hash = "unknown"

# Get project metadata
project_info = {
    'name': 'tvdatafeed',
    'languages': ['python'],
    'frameworks': [],
    'description': 'A Python library for downloading historical market data (OHLCV, financials, earnings, dividends) from TradingView via WebSocket.'
}

# Assemble final graph
final_graph = {
    'version': '1.0.0',
    'project': {
        'name': project_info['name'],
        'languages': project_info['languages'],
        'frameworks': project_info['frameworks'],
        'description': project_info['description'],
        'analyzedAt': datetime.utcnow().isoformat() + 'Z',
        'gitCommitHash': commit_hash
    },
    'nodes': graph['nodes'],
    'edges': graph['edges'],
    'layers': layers,
    'tour': tour
}

# Write final graph
output_file = OUTPUT_DIR / 'knowledge-graph.json'
with open(output_file, 'w') as f:
    json.dump(final_graph, f, indent=2)

print(f"  ✓ Knowledge graph: {output_file}")
print(f"    - {len(final_graph['nodes'])} nodes")
print(f"    - {len(final_graph['edges'])} edges")
print(f"    - {len(final_graph['layers'])} layers")
print(f"    - {len(final_graph['tour'])} tour steps")

# Write metadata
meta = {
    'lastAnalyzedAt': datetime.utcnow().isoformat() + 'Z',
    'gitCommitHash': commit_hash,
    'version': '1.0.0',
    'analyzedFiles': len([n for n in final_graph['nodes'] if n['type'] in ['file', 'config', 'document']])
}

meta_file = OUTPUT_DIR / 'meta.json'
with open(meta_file, 'w') as f:
    json.dump(meta, f, indent=2)

print(f"  ✓ Metadata: {meta_file}")

# Print summary statistics
node_types = {}
for node in final_graph['nodes']:
    t = node['type']
    node_types[t] = node_types.get(t, 0) + 1

edge_types = {}
for edge in final_graph['edges']:
    t = edge['type']
    edge_types[t] = edge_types.get(t, 0) + 1

print(f"\n  Analysis Summary:")
print(f"    Project: {project_info['name']}")
print(f"    Commit: {commit_hash[:8]}")
print(f"    Languages: {', '.join(project_info['languages'])}")
print(f"\n    Nodes by type:")
for node_type in sorted(node_types.keys()):
    print(f"      {node_type}: {node_types[node_type]}")
print(f"\n    Edges by type:")
for edge_type in sorted(edge_types.keys()):
    print(f"      {edge_type}: {edge_types[edge_type]}")
print(f"\n    Layers: {', '.join([l['name'] for l in layers])}")

print(f"\n✓ Phase 7 complete - Knowledge graph saved!")
print(f"\nOutput file: {output_file}")
print(f"Ready for dashboard: yes")
