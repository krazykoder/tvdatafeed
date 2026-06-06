#!/usr/bin/env python3
"""
Comprehensive project scanner for tvdatafeed.
Generates scan-result.json for the understand-anything knowledge graph.
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path("/Users/towshif/code/python/tvdatafeed")
OUTPUT_DIR = PROJECT_ROOT / ".understand-anything" / "intermediate"
OUTPUT_FILE = OUTPUT_DIR / "scan-result.json"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def count_lines(file_path):
    """Count lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return len(f.readlines())
    except:
        return 0

def get_file_category(path_str, language):
    """Determine file category based on filename and language."""
    p = path_str.lower()
    
    if language == "python":
        if 'test' in p or 'debug' in p:
            return "script" if 'test_' in p else "data"
        return "code"
    elif language == "markdown":
        return "docs"
    elif language == "json":
        return "data"
    elif language == "yaml" or language == "yml":
        return "config"
    elif p.endswith(('setup.py', 'requirements.txt', 'pyproject.toml', 'setup.cfg')):
        return "config"
    elif p.endswith(('dockerfile', '.dockerignore')):
        return "infra"
    elif p.endswith(('.sh', '.bash')):
        return "script"
    else:
        return "markup" if language in ["html", "xml"] else "data"

def get_language(file_path):
    """Determine language based on file extension."""
    ext = Path(file_path).suffix.lower()
    
    language_map = {
        '.py': 'python',
        '.md': 'markdown',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.txt': 'text',
        '.csv': 'csv',
        '.ws': 'text',
        '.html': 'html',
        '.sh': 'shell',
        '.ipynb': 'jupyter',
    }
    
    return language_map.get(ext, 'unknown')

def should_ignore(rel_path):
    """Check if path should be ignored."""
    ignore_patterns = [
        '.git', '__pycache__', '.DS_Store', '*.egg-info',
        '.venv', 'venv', 'env', '.pytest_cache',
        '.understand-anything'
    ]
    
    parts = rel_path.split('/')
    for part in parts:
        for pattern in ignore_patterns:
            if '*' in pattern:
                if re.match(pattern.replace('*', '.*'), part):
                    return True
            elif part == pattern or part.startswith(pattern):
                return True
    
    return False

def extract_imports(file_path):
    """Extract imports from Python file."""
    imports = set()
    
    if file_path.suffix != '.py':
        return list(imports)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Extract 'import X' and 'from X import Y'
            import_pattern = r'(?:^|\n)(?:from\s+([\w.]+)|import\s+([\w.]+))'
            matches = re.findall(import_pattern, content)
            
            for match in matches:
                module = match[0] or match[1]
                # Get top-level module
                top_level = module.split('.')[0]
                if top_level and not top_level.startswith('_'):
                    imports.add(top_level)
    except:
        pass
    
    return sorted(list(imports))

def scan_project():
    """Scan project and return comprehensive inventory."""
    files = []
    import_map = defaultdict(list)
    language_set = set()
    ignored_count = 0
    
    # Walk through project directory
    for root, dirs, filenames in os.walk(PROJECT_ROOT):
        # Filter directories to ignore
        dirs[:] = [d for d in dirs if not should_ignore(d)]
        
        for filename in filenames:
            file_path = Path(root) / filename
            rel_path = str(file_path.relative_to(PROJECT_ROOT))
            
            if should_ignore(rel_path):
                ignored_count += 1
                continue
            
            language = get_language(rel_path)
            if language == 'unknown':
                continue
            
            size_lines = count_lines(file_path)
            category = get_file_category(rel_path, language)
            
            language_set.add(language)
            
            file_info = {
                "path": rel_path,
                "language": language,
                "sizeLines": size_lines,
                "fileCategory": category
            }
            files.append(file_info)
            
            # Extract imports for Python files
            if language == 'python':
                imports = extract_imports(file_path)
                if imports:
                    import_map[rel_path] = imports
    
    # Sort files by path
    files.sort(key=lambda f: f["path"])
    
    # Create scan result
    scan_result = {
        "projectName": "tvdatafeed",
        "projectDescription": "A Python library for downloading historical market data (OHLCV, financials, earnings, dividends) from TradingView via WebSocket. Version 2.0.1 - WebSocket-based, no Selenium dependency.",
        "languages": sorted(list(language_set)),
        "frameworks": [],
        "files": files,
        "importMap": dict(import_map),
        "totalFiles": len(files),
        "filteredByIgnore": ignored_count,
        "complexityEstimate": "moderate"
    }
    
    return scan_result

# Run scan
print("[Phase 1/7] Scanning project files...")
result = scan_project()

# Write output
with open(OUTPUT_FILE, 'w') as f:
    json.dump(result, f, indent=2)

print(f"✓ Phase 1 complete. Found {result['totalFiles']} files")
print(f"  Languages: {', '.join(result['languages'])}")
print(f"  Files filtered: {result['filteredByIgnore']}")
print(f"\nScan result written to: {OUTPUT_FILE}")

# Print summary by category
from collections import Counter
categories = Counter(f['fileCategory'] for f in result['files'])
print(f"\nFiles by category:")
for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count}")
