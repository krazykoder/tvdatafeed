#!/usr/bin/env python3
"""
Analyze and compare metrics between .ws and .json files
Ensures complete conversion with detailed metrics counting
"""
import json
import re
import sys
import os
from pathlib import Path
from collections import defaultdict

def count_ws_metrics(raw_data):
    """Count metrics in raw websocket data"""
    stats = {
        'total_size': len(raw_data),
        'frames': len(raw_data.split('~m~')) // 2,  # Approximate
        'json_objects': 0,
        'total_keys': set(),
        'financial_fields': set(),
    }
    
    # Count JSON objects in the data
    json_count = raw_data.count('{"')
    stats['json_objects'] = json_count
    
    # Find all financial field names using regex
    # Look for field names in the format "field_name":
    field_pattern = r'"([a-z_0-9]+)":\s*(?:\[|\{|"[^"]*"|[\d\.]+|true|false|null)'
    fields = re.findall(field_pattern, raw_data)
    stats['total_keys'] = set(fields)
    
    # Count financial-specific fields
    financial_keywords = ['revenue', 'earning', 'profit', 'margin', 'equity', 'assets', 
                         'liabilities', 'cash', 'debt', 'income', 'expense', 'dividend',
                         'eps', 'pe_ratio', 'market_cap', 'fiscal', 'quarter', 'year',
                         'actual', 'estimate', 'reported', 'growth']
    
    financial_fields = [f for f in fields if any(kw in f.lower() for kw in financial_keywords)]
    stats['financial_fields'] = set(financial_fields)
    
    return stats

def count_json_metrics(json_data):
    """Count metrics in converted JSON data"""
    stats = {
        'total_size': sum(len(json.dumps(f)) for f in json_data.get('frames', [])),
        'frames': len(json_data.get('frames', [])),
        'total_keys': set(),
        'financial_fields': set(),
        'data_density': 0,  # Ratio of actual data to structure
    }
    
    # Collect all keys from all frames
    all_keys = set()
    financial_keywords = ['revenue', 'earning', 'profit', 'margin', 'equity', 'assets', 
                         'liabilities', 'cash', 'debt', 'income', 'expense', 'dividend',
                         'eps', 'pe_ratio', 'market_cap', 'fiscal', 'quarter', 'year',
                         'actual', 'estimate', 'reported', 'growth']
    
    def extract_keys(obj, keys=None):
        if keys is None:
            keys = set()
        if isinstance(obj, dict):
            for k, v in obj.items():
                keys.add(k)
                extract_keys(v, keys)
        elif isinstance(obj, list):
            for item in obj:
                extract_keys(item, keys)
        return keys
    
    for frame in json_data.get('frames', []):
        all_keys = extract_keys(frame, all_keys)
    
    stats['total_keys'] = all_keys
    financial_fields = [f for f in all_keys if any(kw in f.lower() for kw in financial_keywords)]
    stats['financial_fields'] = set(financial_fields)
    
    return stats

def analyze_financial_frame(json_data):
    """Analyze the financial data frame in detail"""
    stats = {
        'has_financial_data': False,
        'symbol': None,
        'financial_metrics_count': 0,
        'quarterly_data_count': 0,
        'annual_data_count': 0,
        'array_fields': [],
        'scalar_fields': [],
        'dict_fields': [],
    }
    
    # Find frame with most keys (usually frame 4 with financial data)
    max_keys_frame = None
    max_keys_count = 0
    
    for frame in json_data.get('frames', []):
        if isinstance(frame, dict) and 'p' in frame:
            if isinstance(frame['p'], list) and len(frame['p']) > 1:
                if isinstance(frame['p'][1], dict) and 'v' in frame['p'][1]:
                    v = frame['p'][1]['v']
                    if isinstance(v, dict):
                        keys_count = len(v)
                        if keys_count > max_keys_count:
                            max_keys_count = keys_count
                            max_keys_frame = v
    
    if max_keys_frame:
        stats['has_financial_data'] = True
        stats['symbol'] = max_keys_frame.get('short_name', 'N/A')
        stats['financial_metrics_count'] = len(max_keys_frame)
        
        # Count different types of fields
        for key, value in max_keys_frame.items():
            if isinstance(value, list):
                stats['array_fields'].append(key)
                # Count rows in arrays
                if value and isinstance(value[0], dict):
                    stats['quarterly_data_count'] += len(value)
            elif isinstance(value, dict):
                stats['dict_fields'].append(key)
            else:
                stats['scalar_fields'].append(key)
    
    return stats

def compare_metrics(ws_file, json_file):
    """Compare metrics between .ws and .json files"""
    
    print(f"\n{'='*80}")
    print(f"Metrics Analysis: {os.path.basename(ws_file)}")
    print(f"{'='*80}\n")
    
    # Read .ws file
    with open(ws_file, 'r', errors='ignore') as f:
        ws_data = f.read()
    
    # Read .json file
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    
    # Count metrics
    ws_stats = count_ws_metrics(ws_data)
    json_stats = count_json_metrics(json_data)
    fin_stats = analyze_financial_frame(json_data)
    
    # Display results
    print(f"[WebSocket File Analysis]")
    print(f"  File size: {ws_stats['total_size']:,} bytes")
    print(f"  Estimated frames: {ws_stats['frames']}")
    print(f"  Unique keys found: {len(ws_stats['total_keys'])}")
    print(f"  Financial fields: {len(ws_stats['financial_fields'])}")
    
    print(f"\n[JSON File Analysis]")
    print(f"  Actual frames: {json_stats['frames']}")
    print(f"  Unique keys preserved: {len(json_stats['total_keys'])}")
    print(f"  Financial fields preserved: {len(json_stats['financial_fields'])}")
    
    print(f"\n[Financial Data Frame Analysis]")
    if fin_stats['has_financial_data']:
        print(f"  ✓ Financial data found")
        print(f"  Symbol: {fin_stats['symbol']}")
        print(f"  Total metrics: {fin_stats['financial_metrics_count']}")
        print(f"  Array fields (time series): {len(fin_stats['array_fields'])}")
        if fin_stats['array_fields']:
            print(f"    Examples: {', '.join(fin_stats['array_fields'][:5])}")
        print(f"  Scalar fields (single values): {len(fin_stats['scalar_fields'])}")
        if fin_stats['scalar_fields']:
            print(f"    Examples: {', '.join(fin_stats['scalar_fields'][:5])}")
        print(f"  Dict fields (nested data): {len(fin_stats['dict_fields'])}")
        if fin_stats['dict_fields']:
            print(f"    Examples: {', '.join(fin_stats['dict_fields'][:5])}")
        print(f"  Total data points: {fin_stats['quarterly_data_count']}")
    else:
        print(f"  ✗ No financial data found")
    
    # Check for data loss
    print(f"\n[Data Integrity Check]")
    key_difference = len(ws_stats['total_keys']) - len(json_stats['total_keys'])
    if key_difference == 0:
        print(f"  ✓ All keys preserved")
    else:
        print(f"  ⚠ Key difference: {key_difference}")
        lost_keys = ws_stats['total_keys'] - json_stats['total_keys']
        if lost_keys:
            print(f"    Lost keys: {lost_keys}")
        extra_keys = json_stats['total_keys'] - ws_stats['total_keys']
        if extra_keys:
            print(f"    Extra keys (added): {extra_keys}")
    
    return {
        'ws_stats': ws_stats,
        'json_stats': json_stats,
        'fin_stats': fin_stats,
        'key_loss': key_difference
    }

def analyze_all_files(directory=None):
    """Analyze all .ws and .json file pairs"""
    
    if directory is None:
        directory = os.path.dirname(__file__)
    
    # Find all .ws files
    ws_files = sorted(Path(directory).glob('*_NASDAQ.ws'))
    
    if not ws_files:
        print(f"No .ws files found in {directory}")
        return
    
    print(f"\n{'='*80}")
    print(f"WebSocket Metrics Conversion Analysis")
    print(f"{'='*80}")
    
    results = {}
    total_metrics = 0
    total_data_points = 0
    
    for ws_file in ws_files:
        symbol = os.path.basename(ws_file).replace('_NASDAQ.ws', '')
        json_file = str(ws_file).replace('.ws', '.json')
        
        if not os.path.exists(json_file):
            print(f"\n⚠ JSON file not found for {symbol}")
            continue
        
        result = compare_metrics(str(ws_file), json_file)
        results[symbol] = result
        
        total_metrics += result['fin_stats']['financial_metrics_count']
        total_data_points += result['fin_stats']['quarterly_data_count']
    
    # Summary
    print(f"\n{'='*80}")
    print(f"Summary Report")
    print(f"{'='*80}\n")
    
    print(f"Files analyzed: {len(results)}")
    print(f"Total financial metrics: {total_metrics:,}")
    print(f"Total data points: {total_data_points:,}")
    
    # Check for any data loss
    any_loss = False
    for symbol, result in results.items():
        if result['key_loss'] != 0:
            any_loss = True
            print(f"⚠ {symbol}: {result['key_loss']} key differences")
    
    if not any_loss:
        print(f"\n✅ All conversions complete - No data loss detected")
    
    return results

if __name__ == '__main__':
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.path.dirname(__file__)
    
    analyze_all_files(directory)
