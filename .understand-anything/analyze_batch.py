#!/usr/bin/env python3
"""
File analyzer for tvdatafeed - extracts nodes and edges from source files.
Produces batch-*.json output compatible with merge-batch-graphs.py
"""

import json
import re
import sys
import ast
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict

PROJECT_ROOT = Path("/Users/towshif/code/python/tvdatafeed")
INTERMEDIATE_DIR = PROJECT_ROOT / ".understand-anything" / "intermediate"

class PythonAnalyzer:
    """Analyze Python files to extract structure and dependencies."""
    
    def __init__(self, file_path: Path, project_root: Path):
        self.file_path = file_path
        self.project_root = project_root
        self.rel_path = str(file_path.relative_to(project_root))
        self.nodes = []
        self.edges = []
        self.imports = []
        
    def analyze(self) -> Tuple[List[Dict], List[Dict]]:
        """Analyze Python file and extract nodes/edges."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = len(content.split('\n'))
        except:
            return [], []
        
        # Create file node
        file_node = {
            'id': f'file:{self.rel_path}',
            'type': 'file',
            'name': self.file_path.name,
            'filePath': self.rel_path,
            'summary': self._extract_module_docstring(content) or f'Python module {self.file_path.stem}',
            'tags': ['python', 'module'],
            'complexity': 'moderate' if lines > 500 else 'simple',
            'languageNotes': f'{lines} lines'
        }
        self.nodes.append(file_node)
        
        # Parse Python AST for classes and functions
        try:
            tree = ast.parse(content)
            self._extract_from_ast(tree)
        except SyntaxError:
            pass
        
        # Extract imports
        self._extract_imports(content)
        
        # Create import edges
        self._create_import_edges()
        
        return self.nodes, self.edges
    
    def _extract_module_docstring(self, content: str) -> str:
        """Extract module docstring."""
        try:
            match = re.search(r'^(""".*?"""|\'\'\'.*?\'\'\')', content, re.DOTALL | re.MULTILINE)
            if match:
                doc = match.group(1).strip('"\' \n')
                return doc[:100]
        except:
            pass
        return None
    
    def _extract_from_ast(self, tree):
        """Extract classes, functions, and methods from AST."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_id = f'class:{self.rel_path}:{node.name}'
                doc = ast.get_docstring(node) or f'Class {node.name}'
                
                class_node = {
                    'id': class_id,
                    'type': 'class',
                    'name': node.name,
                    'filePath': self.rel_path,
                    'summary': doc[:100] if doc else f'Class {node.name}',
                    'tags': ['class'],
                    'complexity': 'simple'
                }
                self.nodes.append(class_node)
                
                # Class is contained in file
                self.edges.append({
                    'source': f'file:{self.rel_path}',
                    'target': class_id,
                    'type': 'contains',
                    'weight': 1.0
                })
                
                # Extract methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_id = f'function:{self.rel_path}:{node.name}.{item.name}'
                        method_doc = ast.get_docstring(item) or f'Method {item.name}'
                        
                        method_node = {
                            'id': method_id,
                            'type': 'function',
                            'name': f'{node.name}.{item.name}',
                            'filePath': self.rel_path,
                            'summary': method_doc[:100],
                            'tags': ['method'],
                            'complexity': 'simple'
                        }
                        self.nodes.append(method_node)
                        
                        # Method is contained in class
                        self.edges.append({
                            'source': class_id,
                            'target': method_id,
                            'type': 'contains',
                            'weight': 1.0
                        })
            
            elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                # Top-level function
                func_id = f'function:{self.rel_path}:{node.name}'
                doc = ast.get_docstring(node) or f'Function {node.name}'
                
                func_node = {
                    'id': func_id,
                    'type': 'function',
                    'name': node.name,
                    'filePath': self.rel_path,
                    'summary': doc[:100] if doc else f'Function {node.name}',
                    'tags': ['function'],
                    'complexity': 'simple'
                }
                self.nodes.append(func_node)
                
                # Function is contained in file
                self.edges.append({
                    'source': f'file:{self.rel_path}',
                    'target': func_id,
                    'type': 'contains',
                    'weight': 1.0
                })
    
    def _extract_imports(self, content: str):
        """Extract import statements."""
        # Find 'import X' and 'from X import Y'
        import_pattern = r'(?:^from\s+([\w.]+)\s+import|^import\s+([\w.]+))'
        
        for match in re.finditer(import_pattern, content, re.MULTILINE):
            module = match.group(1) or match.group(2)
            self.imports.append(module)
    
    def _create_import_edges(self):
        """Create edges for external imports."""
        project_modules = {'tvDatafeed', 'tvdatafeed'}
        
        for import_name in self.imports:
            top_module = import_name.split('.')[0]
            
            # Skip standard library and project imports
            if top_module not in project_modules:
                edge = {
                    'source': f'file:{self.rel_path}',
                    'target': f'module:{top_module}',
                    'type': 'imports',
                    'weight': 0.7
                }
                self.edges.append(edge)

class MarkdownAnalyzer:
    """Analyze Markdown documentation files."""
    
    def __init__(self, file_path: Path, project_root: Path):
        self.file_path = file_path
        self.project_root = project_root
        self.rel_path = str(file_path.relative_to(project_root))
        
    def analyze(self) -> Tuple[List[Dict], List[Dict]]:
        """Analyze Markdown file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return [], []
        
        # Extract first heading as summary
        match = re.search(r'#+ (.+?)$', content, re.MULTILINE)
        title = match.group(1).strip() if match else self.file_path.stem
        
        doc_node = {
            'id': f'document:{self.rel_path}',
            'type': 'document',
            'name': title,
            'filePath': self.rel_path,
            'summary': self._extract_summary(content),
            'tags': ['documentation', 'markdown'],
            'complexity': 'simple'
        }
        
        return [doc_node], []
    
    def _extract_summary(self, content: str) -> str:
        """Extract first paragraph as summary."""
        lines = []
        for line in content.split('\n'):
            if line.strip() and not line.startswith('#'):
                lines.append(line.strip())
                if len(lines) >= 2:
                    break
        
        summary = ' '.join(lines)[:150]
        return summary or 'Documentation'

class JSONAnalyzer:
    """Analyze JSON data files."""
    
    def __init__(self, file_path: Path, project_root: Path):
        self.file_path = file_path
        self.project_root = project_root
        self.rel_path = str(file_path.relative_to(project_root))
        
    def analyze(self) -> Tuple[List[Dict], List[Dict]]:
        """Analyze JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                size_kb = len(content) / 1024
        except:
            size_kb = 0
        
        data_node = {
            'id': f'data:{self.rel_path}',
            'type': 'config' if 'config' in self.rel_path.lower() else 'config',
            'name': self.file_path.stem,
            'filePath': self.rel_path,
            'summary': f'JSON data file ({size_kb:.1f} KB)',
            'tags': ['json', 'data'],
            'complexity': 'simple'
        }
        
        return [data_node], []

def analyze_batch(batch_index: int):
    """Analyze a single batch of files."""
    batches_file = INTERMEDIATE_DIR / 'batches.json'
    
    with open(batches_file) as f:
        batches_data = json.load(f)
    
    if batch_index >= len(batches_data['batches']):
        print(f"Error: Batch {batch_index} not found")
        return
    
    batch = batches_data['batches'][batch_index]
    all_nodes = []
    all_edges = []
    
    print(f"\nAnalyzing batch {batch_index}: {batch['category']}")
    
    for file_info in batch['batchFiles']:
        file_path = PROJECT_ROOT / file_info['path']
        language = file_info['language']
        
        if not file_path.exists():
            print(f"  ⚠ Skipping {file_info['path']} (not found)")
            continue
        
        analyzer = None
        
        if language == 'python':
            analyzer = PythonAnalyzer(file_path, PROJECT_ROOT)
        elif language == 'markdown':
            analyzer = MarkdownAnalyzer(file_path, PROJECT_ROOT)
        elif language == 'json':
            analyzer = JSONAnalyzer(file_path, PROJECT_ROOT)
        
        if analyzer:
            nodes, edges = analyzer.analyze()
            all_nodes.extend(nodes)
            all_edges.extend(edges)
            print(f"  ✓ {file_info['path']}: {len(nodes)} nodes, {len(edges)} edges")
    
    # Write batch output
    output_file = INTERMEDIATE_DIR / f'batch-{batch_index}.json'
    output_data = {
        'batchIndex': batch_index,
        'nodes': all_nodes,
        'edges': all_edges
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"  Output: {output_file}")
    return len(all_nodes), len(all_edges)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        batch_idx = int(sys.argv[1])
    else:
        batch_idx = 0
    
    analyze_batch(batch_idx)
