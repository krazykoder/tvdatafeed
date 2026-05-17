#!/usr/bin/env python3
"""
Compare .ws and .json formats and show conversion benefits
"""
import json
import os
from pathlib import Path

def show_format_comparison(ws_file, json_file):
    """Show a comparison of the two formats"""
    
    print(f"\n{'='*80}")
    print(f"Format Comparison: {os.path.basename(ws_file)}")
    print(f"{'='*80}\n")
    
    # Read files
    with open(ws_file, 'r', errors='ignore') as f:
        ws_data = f.read()
    
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    
    ws_size = os.path.getsize(ws_file)
    json_size = os.path.getsize(json_file)
    
    # Display comparison
    print(f"[WebSocket Format (.ws)]")
    print(f"  Raw format: ~m~<length>~m~<json_data>~m~...\n")
    print(f"  Sample (first 300 chars):")
    print(f"  {ws_data[:300]}\n")
    print(f"  File size: {ws_size:,} bytes")
    print(f"  Format: Binary websocket protocol with delimiters\n")
    
    print(f"[JSON Format (.json)]")
    print("  Structure:")
    print("    {")
    print("      'metadata': {...}  # Metadata about conversion")
    print("      'frames': [...]    # List of JSON objects")
    print("    }\n")
    print(f"  Sample structure:")
    sample = {
        'metadata': json_data['metadata'],
        'frames': f"[{len(json_data['frames'])} JSON objects]"
    }
    print(f"  {json.dumps(sample, indent=4)}\n")
    print(f"  File size: {json_size:,} bytes")
    print(f"  Format: Standard JSON (easily parseable)\n")
    
    # Benefits
    print(f"[Conversion Benefits]")
    print(f"  ✓ Easy to parse with any JSON parser")
    print(f"  ✓ Human-readable format")
    print(f"  ✓ Metadata preserved (source file, conversion time, frame count)")
    print(f"  ✓ Can be imported into databases")
    print(f"  ✓ Compatible with web services/APIs")
    print(f"  ✓ Size: {ws_size:,} → {json_size:,} bytes (compression-friendly)")
    print(f"  ✓ Easy to filter/search specific fields")
    print(f"  ✓ IDE support for JSON schema validation\n")

def show_usage_examples():
    """Show examples of how to use converted JSON files"""
    
    print(f"{'='*80}")
    print(f"Usage Examples with Converted JSON")
    print(f"{'='*80}\n")
    
    code_example = '''
# Load converted JSON file
import json

with open('KLAC_NASDAQ.json', 'r') as f:
    data = json.load(f)

# Access metadata
print(data['metadata'])
# {'source_file': 'KLAC_NASDAQ.ws', 
#  'total_objects': 6, 
#  'conversion_date': '2026-05-17...'}

# Access websocket frames
frames = data['frames']
print(f"Total frames: {len(frames)}")

# Extract financial data
for frame in frames:
    if 'p' in frame and isinstance(frame['p'], list) and len(frame['p']) > 1:
        if isinstance(frame['p'][1], dict) and 'v' in frame['p'][1]:
            financial_data = frame['p'][1]['v']
            
            # Access specific financial fields
            if 'short_name' in financial_data:
                print(f"Symbol: {financial_data['short_name']}")
            
            if 'market_cap_basic' in financial_data:
                print(f"Market Cap: {financial_data['market_cap_basic']}")
            
            if 'earnings_fq_h' in financial_data:
                earnings = financial_data['earnings_fq_h']
                print(f"Quarterly Earnings: {len(earnings)} quarters")

# Save specific data to CSV
import pandas as pd

# Extract earnings data
if 'earnings_fq_h' in financial_data:
    df = pd.DataFrame(financial_data['earnings_fq_h'])
    df.to_csv('earnings.csv', index=False)

# Search for specific fields
all_keys = financial_data.keys()
revenue_keys = [k for k in all_keys if 'revenue' in k.lower()]
print(f"Revenue-related fields: {revenue_keys}")
'''
    
    print(code_example)

if __name__ == '__main__':
    debug_dir = os.path.dirname(__file__)
    
    # Find a pair of files to compare
    ws_files = sorted(Path(debug_dir).glob('*_NASDAQ.ws'))
    
    if ws_files:
        ws_file = str(ws_files[0])
        json_file = ws_file.replace('.ws', '.json')
        
        if os.path.exists(json_file):
            show_format_comparison(ws_file, json_file)
            show_usage_examples()
        else:
            print(f"JSON file not found: {json_file}")
    else:
        print("No .ws files found")
