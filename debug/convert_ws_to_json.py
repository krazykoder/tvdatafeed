#!/usr/bin/env python3
"""
Bulk convert .ws (websocket) files to .json format
"""
import json
import re
import sys
import os
from pathlib import Path

def parse_websocket_data(raw_data):
    """Parse websocket protocol data and extract JSON objects"""
    """
    Websocket format: ~m~<length>~m~<json_data>~m~<length>~m~<json_data>...
    Returns: List of parsed JSON objects
    """
    try:
        # Split by the frame delimiters
        # Pattern: ~m~<number>~m~<json_data>
        parts = raw_data.split('~m~')
        
        json_objects = []
        i = 1  # Skip first empty part (before first ~m~)
        
        while i < len(parts):
            # Skip the length indicator
            if i + 1 < len(parts):
                json_str = parts[i + 1]
                try:
                    # Try to parse as JSON
                    obj = json.loads(json_str)
                    json_objects.append(obj)
                except json.JSONDecodeError:
                    # If it fails, try to extract a valid JSON object
                    # Look for valid JSON boundaries
                    match = re.match(r'^(\{.*\})(?:~m~|$)', json_str, re.DOTALL)
                    if match:
                        try:
                            obj = json.loads(match.group(1))
                            json_objects.append(obj)
                        except json.JSONDecodeError:
                            pass
            i += 2  # Move to next frame
        
        return json_objects
    except Exception as e:
        print(f"  Error parsing websocket data: {e}")
        return []

def count_metrics_in_json(json_objects):
    """Count metrics in parsed JSON objects"""
    stats = {
        'total_keys': set(),
        'financial_metrics': 0,
        'array_fields': 0,
        'scalar_fields': 0,
        'dict_fields': 0,
        'data_rows': 0,
    }
    
    financial_keywords = ['revenue', 'earning', 'profit', 'margin', 'equity', 'assets', 
                         'liabilities', 'cash', 'debt', 'income', 'expense', 'dividend',
                         'eps', 'pe_ratio', 'market_cap', 'fiscal', 'quarter', 'year',
                         'actual', 'estimate', 'reported', 'growth']
    
    for obj in json_objects:
        # Find the frame with financial data (usually frame with most keys)
        if isinstance(obj, dict) and 'p' in obj:
            if isinstance(obj['p'], list) and len(obj['p']) > 1:
                if isinstance(obj['p'][1], dict) and 'v' in obj['p'][1]:
                    v = obj['p'][1]['v']
                    if isinstance(v, dict) and len(v) > 100:  # Financial data frame
                        stats['financial_metrics'] = len(v)
                        
                        for key, value in v.items():
                            stats['total_keys'].add(key)
                            
                            if isinstance(value, list):
                                stats['array_fields'] += 1
                                # Count rows in array
                                if value and isinstance(value[0], dict):
                                    stats['data_rows'] += len(value)
                            elif isinstance(value, dict):
                                stats['dict_fields'] += 1
                            else:
                                stats['scalar_fields'] += 1
    
    return stats

def convert_ws_to_json(ws_file, output_file=None):
    """Convert a .ws file to .json format"""
    
    if output_file is None:
        output_file = ws_file.replace('.ws', '.json')
    
    try:
        print(f"[*] Converting: {os.path.basename(ws_file)}")
        
        # Read the .ws file
        with open(ws_file, 'r', encoding='utf-8', errors='ignore') as f:
            raw_data = f.read()
        
        print(f"    Input size: {len(raw_data):,} bytes")
        
        # Parse websocket data
        json_objects = parse_websocket_data(raw_data)
        print(f"    Extracted {len(json_objects)} JSON objects")
        
        # Create output structure
        output = {
            'metadata': {
                'source_file': os.path.basename(ws_file),
                'total_objects': len(json_objects),
                'conversion_date': str(__import__('datetime').datetime.now()),
            },
            'frames': json_objects
        }
        
        # Count metrics
        metrics = count_metrics_in_json(json_objects)
        
        # Write to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        output_size = os.path.getsize(output_file)
        print(f"    ✓ Output: {os.path.basename(output_file)} ({output_size:,} bytes)")
        
        # Print metrics summary
        if metrics['financial_metrics'] > 0:
            print(f"    ✓ Metrics: {metrics['financial_metrics']:,} financial fields")
            print(f"      - Time series (arrays): {metrics['array_fields']}")
            print(f"      - Single values (scalars): {metrics['scalar_fields']}")
            print(f"      - Nested data (dicts): {metrics['dict_fields']}")
            print(f"      - Data rows: {metrics['data_rows']}")
        
        return True
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False

def bulk_convert_ws_to_json(directory=None, pattern='*.ws'):
    """Convert all .ws files in a directory to .json"""
    
    if directory is None:
        directory = os.path.dirname(__file__)
    
    # Find all .ws files
    ws_files = sorted(Path(directory).glob(pattern))
    
    if not ws_files:
        print(f"No {pattern} files found in {directory}")
        return 0
    
    print(f"\n{'='*80}")
    print(f"Bulk Converting WebSocket Files to JSON")
    print(f"{'='*80}\n")
    print(f"Directory: {directory}")
    print(f"Found {len(ws_files)} files to convert\n")
    
    converted = 0
    failed = 0
    
    for ws_file in ws_files:
        if convert_ws_to_json(str(ws_file)):
            converted += 1
        else:
            failed += 1
        print()
    
    print(f"{'='*80}")
    print(f"Results: {converted} converted, {failed} failed")
    print(f"{'='*80}\n")
    
    return converted

if __name__ == '__main__':
    # Get directory from command line or use current directory
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.path.dirname(__file__)
    
    converted = bulk_convert_ws_to_json(directory)
    sys.exit(0 if converted > 0 else 1)
