#!/usr/bin/env python3
"""
Script to test the parser against raw websocket data
"""
import json
import re
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def analyze_raw_data(filepath):
    """Analyze raw data structure"""
    print(f"\n{'='*80}")
    print(f"Analyzing: {filepath}")
    print(f"{'='*80}")
    
    with open(filepath, 'r') as f:
        raw_data = f.read()
    
    print(f"\n[*] File size: {len(raw_data)} bytes")
    print(f"\n[*] First 500 characters:")
    print(raw_data[:500])
    
    print(f"\n[*] Last 300 characters:")
    print(raw_data[-300:])
    
    # Look for the delimiters
    delimiter_count = raw_data.count('~m~')
    print(f"\n[*] Delimiter count (~m~): {delimiter_count}")
    
    # Split by delimiter
    parts = raw_data.split('~m~')
    print(f"\n[*] Number of parts after split: {len(parts)}")
    
    # Show first few parts
    for i, part in enumerate(parts[:3]):
        print(f"\n[*] Part {i} (first 100 chars): {part[:100]}")

def test_current_parser(filepath):
    """Test the current parser"""
    print(f"\n{'='*80}")
    print(f"Testing Current Parser: {filepath}")
    print(f"{'='*80}")
    
    with open(filepath, 'r') as f:
        raw_data = f.read()
    
    # Step 1: Remove escaped quotes
    print("\n[STEP 1] Remove escaped quotes (\\\")")
    step1 = re.sub(r"\\\"", "", raw_data)
    print(f"  Before: {len(raw_data)} bytes")
    print(f"  After: {len(step1)} bytes")
    
    # Step 2: Remove backslashes
    print("\n[STEP 2] Remove backslashes (\\)")
    step2 = re.sub(r"\\", "", step1)
    print(f"  Before: {len(step1)} bytes")
    print(f"  After: {len(step2)} bytes")
    
    # Step 3: Replace ~m~...~m~ with comma
    print("\n[STEP 3] Replace ~m~...~m~ with comma")
    step3 = re.sub(r"~m~(.+?)~m~", ",", step2)
    print(f"  Before: {len(step2)} bytes")
    print(f"  After: {len(step3)} bytes")
    print(f"  First 200 chars: {step3[:200]}")
    
    # Step 4: Wrap in brackets and try to parse JSON
    print("\n[STEP 4] Wrap in brackets [...]")
    step4 = "[" + step3[1:] + "]"
    print(f"  Length: {len(step4)} bytes")
    print(f"  First 200 chars: {step4[:200]}")
    print(f"  Last 100 chars: {step4[-100:]}")
    
    # Try to parse JSON
    print("\n[STEP 5] Parse JSON")
    try:
        dataDict = json.loads(step4)
        print(f"  ✓ Successfully parsed!")
        print(f"  ✓ Number of items: {len(dataDict)}")
        print(f"  ✓ First item type: {type(dataDict[0])}")
        if len(dataDict) > 0 and isinstance(dataDict[0], dict):
            print(f"  ✓ First item keys: {list(dataDict[0].keys())}")
        
        # Try to extract financial data
        print("\n[STEP 6] Extract Financial Fields")
        fields_to_find = ['revenues_fq_h', 'earnings_fq_h', 'revenues_fy_h', 'earnings_fy_h']
        
        for field in fields_to_find:
            try:
                # Try current regex method
                out = re.search(f'"{field}":\[(.+?)\]', raw_data).group(1)
                parsed = json.loads("[" + out + "]")
                print(f"  ✓ {field}: Found {len(parsed)} items")
            except Exception as e:
                print(f"  ✗ {field}: {type(e).__name__}")
        
        # Print structure of merged data
        print("\n[STEP 7] Check merged data structure")
        header = {}
        merged = {}
        for i, toplevelItem in enumerate(dataDict):
            try:
                if isinstance(toplevelItem, dict) and "p" in toplevelItem:
                    if len(toplevelItem["p"]) > 1 and isinstance(toplevelItem["p"][1], dict) and "v" in toplevelItem["p"][1]:
                        v = toplevelItem["p"][1]["v"]
                        print(f"  Item {i}: Found 'v' with {len(v)} keys (type: {type(v).__name__})")
                        # Check for financial fields
                        for field in fields_to_find:
                            if field in v:
                                print(f"    -> Contains '{field}'")
                        merged = {**merged, **v}
            except Exception as e:
                pass
        
        print(f"\n  ✓ Total merged keys: {len(merged.keys())}")
        
    except json.JSONDecodeError as e:
        print(f"  ✗ JSON Parse Error: {e}")
        print(f"  ✗ Error at position: {e.pos}")
        # Show context around error
        start = max(0, e.pos - 100)
        end = min(len(step4), e.pos + 100)
        print(f"  ✗ Context around error:")
        print(f"     ...{step4[start:end]}...")

if __name__ == '__main__':
    # Test with KLAC
    test_file = os.path.join(os.path.dirname(__file__), 'KLAC_NASDAQ.ws')
    
    if not os.path.exists(test_file):
        print(f"Error: {test_file} not found!")
        sys.exit(1)
    
    analyze_raw_data(test_file)
    test_current_parser(test_file)
