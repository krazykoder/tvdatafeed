#!/usr/bin/env python3
"""
Identify architectural layers in the tvdatafeed codebase.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path("/Users/towshif/code/python/tvdatafeed")
INTERMEDIATE_DIR = PROJECT_ROOT / ".understand-anything" / "intermediate"

# Load assembled graph
with open(INTERMEDIATE_DIR / 'assembled-graph.json') as f:
    graph = json.load(f)

nodes = graph['nodes']
edges = graph['edges']

print("[Phase 4/7] Identifying architectural layers...")

# Get file-level nodes
file_nodes = [n for n in nodes if n['type'] == 'file']
function_nodes = [n for n in nodes if n['type'] == 'function']
class_nodes = [n for n in nodes if n['type'] == 'class']
config_nodes = [n for n in nodes if n['type'] == 'config']
doc_nodes = [n for n in nodes if n['type'] == 'document']

print(f"  Found {len(file_nodes)} files, {len(class_nodes)} classes, {len(function_nodes)} functions")

# Analyze file paths and purposes
def categorize_file(path: str) -> str:
    """Categorize file by its path and purpose."""
    path_lower = path.lower()
    
    if path.startswith('tvDatafeed/'):
        if path == 'tvDatafeed/__init__.py':
            return 'API'
        elif path == 'tvDatafeed/main.py':
            return 'Core'
        elif path.endswith('.md'):
            return 'Documentation'
    elif path.startswith('debug/'):
        return 'Testing & Validation'
    elif path.startswith('data_extract/'):
        return 'Data Analysis'
    elif path.startswith('archive/'):
        return 'Archive'
    elif path == 'setup.py' or path == 'requirements.txt':
        return 'Build & Configuration'
    elif path.endswith('.ipynb'):
        return 'Examples'
    elif path.endswith('.md'):
        return 'Documentation'
    
    return 'Utilities'

# Group nodes by layer
layers_dict = {}
for file_node in file_nodes:
    layer = categorize_file(file_node['filePath'])
    if layer not in layers_dict:
        layers_dict[layer] = {
            'id': f'layer:{layer.lower().replace(" & ", "-").replace(" ", "-")}',
            'name': layer,
            'description': '',
            'nodeIds': []
        }
    
    file_id = file_node['id']
    layers_dict[layer]['nodeIds'].append(file_id)
    
    # Add all functions and classes within this file to the layer
    for func in [n for n in function_nodes if n.get('filePath') == file_node['filePath']]:
        layers_dict[layer]['nodeIds'].append(func['id'])
    for cls in [n for n in class_nodes if n.get('filePath') == file_node['filePath']]:
        layers_dict[layer]['nodeIds'].append(cls['id'])

# Add descriptions
layer_descriptions = {
    'Core': 'Main WebSocket communication engine and protocol handler',
    'API': 'Public API exports and module initialization',
    'Testing & Validation': 'Debug scripts, parsers, and data validation tools',
    'Data Analysis': 'Extracted nomenclature and financial data analysis',
    'Build & Configuration': 'Package setup, dependencies, and build configuration',
    'Documentation': 'Project documentation and API references',
    'Examples': 'Interactive examples and usage demonstrations',
    'Archive': 'Legacy code and experimental implementations',
    'Utilities': 'Supporting utilities and helper modules'
}

for layer_name, layer_desc in layer_descriptions.items():
    if layer_name in layers_dict:
        layers_dict[layer_name]['description'] = layer_desc

# Convert to list and sort by typical order
layer_order = ['API', 'Core', 'Build & Configuration', 'Documentation', 'Testing & Validation', 
               'Data Analysis', 'Examples', 'Utilities', 'Archive']

layers = []
for layer_name in layer_order:
    if layer_name in layers_dict:
        layers.append(layers_dict[layer_name])

# Add any missing layers
for layer_name in layers_dict:
    if layer_name not in layer_order:
        layers.append(layers_dict[layer_name])

print(f"\n  Identified {len(layers)} layers:")
for layer in layers:
    print(f"    - {layer['name']}: {len(layer['nodeIds'])} nodes")

# Write layers
layers_file = INTERMEDIATE_DIR / 'layers.json'
with open(layers_file, 'w') as f:
    json.dump(layers, f, indent=2)

print(f"\n✓ Phase 4 complete")
print(f"  Output: {layers_file}")
