#!/usr/bin/env python3
"""
Merge and normalize batch analysis results into assembled graph.
Compatible with understand-anything merge-batch-graphs.py behavior.
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Any

PROJECT_ROOT = Path("/Users/towshif/code/python/tvdatafeed")
INTERMEDIATE_DIR = PROJECT_ROOT / ".understand-anything" / "intermediate"

def normalize_node_id(node_id: str) -> str:
    """Normalize node ID to remove duplicates and prefixes."""
    # Strip project name prefix if present
    node_id = re.sub(r'^(tvdatafeed|tvDatafeed):', '', node_id)
    return node_id

def normalize_complexity(complexity: str) -> str:
    """Normalize complexity values."""
    mapping = {
        'low': 'simple',
        'medium': 'moderate',
        'high': 'complex',
        'simple': 'simple',
        'moderate': 'moderate',
        'complex': 'complex'
    }
    return mapping.get(complexity.lower(), 'moderate')

def merge_batch_graphs():
    """Merge all batch-*.json files into a single graph."""
    print("[Phase 2 merge] Merging batch results...")
    
    all_nodes = {}
    all_edges = []
    nodes_by_file = defaultdict(list)
    errors = []
    warnings = []
    
    # Find all batch files
    batch_files = sorted(INTERMEDIATE_DIR.glob('batch-[0-9]*.json'))
    print(f"  Found {len(batch_files)} batch files")
    
    # Load and merge nodes and edges
    for batch_file in batch_files:
        try:
            with open(batch_file) as f:
                batch_data = json.load(f)
            
            batch_idx = batch_file.stem.split('-')[1]
            
            # Process nodes
            for node in batch_data.get('nodes', []):
                # Normalize node ID
                orig_id = node.get('id', '')
                node['id'] = normalize_node_id(orig_id)
                
                # Validate required fields
                if not node.get('id'):
                    errors.append(f"Node missing id in {batch_file.name}")
                    continue
                if not node.get('type'):
                    node['type'] = 'file'
                if not node.get('name'):
                    node['name'] = node['id'].split(':')[-1]
                if not node.get('summary'):
                    node['summary'] = f'No summary available for {node["name"]}'
                if not node.get('tags'):
                    node['tags'] = ['untagged']
                
                # Normalize complexity
                if 'complexity' in node:
                    node['complexity'] = normalize_complexity(node['complexity'])
                else:
                    node['complexity'] = 'moderate'
                
                # Track by file
                if 'filePath' in node:
                    nodes_by_file[node['filePath']].append(node['id'])
                
                # Add or update node (last occurrence wins in deduplication)
                all_nodes[node['id']] = node
            
            # Process edges
            for edge in batch_data.get('edges', []):
                # Normalize edge node IDs
                edge['source'] = normalize_node_id(edge.get('source', ''))
                edge['target'] = normalize_node_id(edge.get('target', ''))
                
                if not edge.get('type'):
                    edge['type'] = 'related'
                if 'weight' not in edge:
                    edge['weight'] = 0.5
                
                all_edges.append(edge)
        
        except Exception as e:
            errors.append(f"Error processing {batch_file.name}: {e}")
    
    print(f"  Loaded {len(all_nodes)} nodes")
    print(f"  Loaded {len(all_edges)} edges")
    
    # Deduplicate edges by (source, target, type)
    edge_key_to_edge = {}
    for edge in all_edges:
        key = (edge['source'], edge['target'], edge['type'])
        # Keep edge with highest weight if duplicates exist
        if key not in edge_key_to_edge or edge.get('weight', 0.5) > edge_key_to_edge[key].get('weight', 0.5):
            edge_key_to_edge[key] = edge
    
    unique_edges = list(edge_key_to_edge.values())
    print(f"  Deduplicated to {len(unique_edges)} unique edges")
    
    # Remove dangling edges
    node_ids = set(all_nodes.keys())
    valid_edges = []
    dangling_count = 0
    
    for edge in unique_edges:
        if edge['source'] in node_ids and edge['target'] in node_ids:
            valid_edges.append(edge)
        else:
            dangling_count += 1
            if dangling_count <= 5:  # Log first 5 dangling edges
                warnings.append(f"Dangling edge: {edge['source']} -> {edge['target']}")
    
    if dangling_count > 5:
        warnings.append(f"... and {dangling_count - 5} more dangling edges")
    
    print(f"  Dropped {dangling_count} dangling edges")
    
    # Add 'tested' tag to nodes that have incoming tested_by edges
    test_nodes = set()
    for edge in valid_edges:
        if edge['type'] == 'tested_by':
            test_nodes.add(edge['target'])
            if 'tags' in all_nodes.get(edge['source'], {}):
                if 'tested' not in all_nodes[edge['source']]['tags']:
                    all_nodes[edge['source']]['tags'].append('tested')
    
    # Statistics
    node_types = Counter(node['type'] for node in all_nodes.values())
    edge_types = Counter(edge['type'] for edge in valid_edges)
    
    print(f"\n  Node types: {dict(node_types)}")
    print(f"  Edge types: {dict(edge_types)}")
    
    if warnings:
        print(f"\n  Warnings ({len(warnings)}):")
        for w in warnings[:5]:
            print(f"    - {w}")
    
    if errors:
        print(f"\n  Errors ({len(errors)}):")
        for e in errors[:5]:
            print(f"    - {e}")
    
    return list(all_nodes.values()), valid_edges, warnings, errors

# Run merge
nodes, edges, warnings, errors = merge_batch_graphs()

# Write assembled graph
assembled_graph = {
    'nodes': nodes,
    'edges': edges
}

output_file = INTERMEDIATE_DIR / 'assembled-graph.json'
with open(output_file, 'w') as f:
    json.dump(assembled_graph, f, indent=2)

print(f"\n✓ Phase 2 merge complete")
print(f"  Output: {output_file}")
print(f"  Nodes: {len(nodes)}, Edges: {len(edges)}")
