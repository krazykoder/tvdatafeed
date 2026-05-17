#!/usr/bin/env python3
"""
Test different approaches to fix the parser
"""
import json
import re
import sys
import os
import pandas as pd
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_parsing_approaches(raw_data):
    """Test different parsing approaches"""
    
    print("\n" + "="*80)
    print("Testing Different Parsing Approaches")
    print("="*80)
    
    # Extract the earnings_fq_h data
    out = re.search(r'"earnings_fq_h":\[(.+?)\]', raw_data).group(1)
    
    print(f"\n[*] Extracted data length: {len(out)} bytes")
    print(f"[*] First 200 chars: {out[:200]}")
    
    # ========== APPROACH 1: Current (BROKEN) ==========
    print("\n[APPROACH 1] Current approach with pd.read_json(lines=True)")
    try:
        df = pd.read_json(out, lines=True)
        print(f"  ✓ Success: {len(df)} rows")
        print(df.head())
    except Exception as e:
        print(f"  ✗ Failed: {type(e).__name__}: {str(e)[:100]}")
    
    # ========== APPROACH 2: Parse JSON first ==========
    print("\n[APPROACH 2] Parse JSON first, then create DataFrame")
    try:
        # Parse the JSON array
        data = json.loads("[" + out + "]")
        df = pd.DataFrame(data)
        print(f"  ✓ Success: {len(df)} rows, {len(df.columns)} columns")
        print(f"  ✓ Columns: {list(df.columns)}")
        print(df.head())
    except Exception as e:
        print(f"  ✗ Failed: {type(e).__name__}: {e}")
    
    # ========== APPROACH 3: Using StringIO ==========
    print("\n[APPROACH 3] Using StringIO with orient='records'")
    try:
        data = json.loads("[" + out + "]")
        df = pd.DataFrame.from_records(data)
        print(f"  ✓ Success: {len(df)} rows, {len(df.columns)} columns")
        print(f"  ✓ Columns: {list(df.columns)}")
        print(df.head())
    except Exception as e:
        print(f"  ✗ Failed: {type(e).__name__}: {e}")
    
    # ========== APPROACH 4: Direct list comprehension ==========
    print("\n[APPROACH 4] Direct JSON parsing")
    try:
        # The data is like: {item1},{item2},...
        # Split by ,{ and reconstruct
        items = []
        current_item = "{"
        for char in out:
            if char == '{' and len(current_item) > 1 and current_item[-1] != '\\':
                items.append(current_item)
                current_item = "{"
            else:
                current_item += char
        items.append(current_item)
        
        data = [json.loads(item) for item in items if item.strip()]
        df = pd.DataFrame(data)
        print(f"  ✓ Success: {len(df)} rows, {len(df.columns)} columns")
        print(f"  ✓ Columns: {list(df.columns)}")
        print(df.head())
    except Exception as e:
        print(f"  ✗ Failed: {type(e).__name__}: {str(e)[:100]}")

if __name__ == '__main__':
    debug_dir = os.path.dirname(__file__)
    test_file = os.path.join(debug_dir, 'KLAC_NASDAQ.ws')
    
    if not os.path.exists(test_file):
        print(f"Error: {test_file} not found!")
        sys.exit(1)
    
    with open(test_file, 'r') as f:
        raw_data = f.read()
    
    test_parsing_approaches(raw_data)
