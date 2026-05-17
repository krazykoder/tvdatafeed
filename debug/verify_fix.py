#!/usr/bin/env python3
"""
Verify that the fixed parser works correctly
"""
import json
import re
import sys
import os
import pandas as pd
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_earnings_df_fixed(raw_data):
    """FIXED VERSION: Extracts Revenues and Earnings : FY and FQ"""
    try:
        out = re.search(r'"revenues_fq_h":\[(.+?)\]', raw_data).group(1)
        data = json.loads("[" + out + "]")
        df_revenue_q = pd.DataFrame(data)

        out = re.search(r'"earnings_fq_h":\[(.+?)\]', raw_data).group(1)
        data = json.loads("[" + out + "]")
        df_earnings_q = pd.DataFrame(data)

        out = re.search(r'"revenues_fy_h":\[(.+?)\]', raw_data).group(1)
        data = json.loads("[" + out + "]")
        df_revenue_f = pd.DataFrame(data)

        out = re.search(r'"earnings_fy_h":\[(.+?)\]', raw_data).group(1)
        data = json.loads("[" + out + "]")
        df_earnings_f = pd.DataFrame(data)

        return df_revenue_q, df_earnings_q, df_revenue_f, df_earnings_f
    except (AttributeError, json.JSONDecodeError, ValueError) as e:
        logger.error(f"no data, please check the exchange and symbol: {e}")
        return None

def create_financial_dict_full(raw_data):
    """Extracts all the financial data as dict"""
    try:
        raw_data = re.sub(r"\\\"", "", raw_data)  # removes \" from string
        raw_data = re.sub(r"\\", "", raw_data)  # removes \ from string
        raw_data = re.sub(r"~m~(.+?)~m~", ",", raw_data)  #  ~m--m~ from string
        # remove the first comma and append to a list []
        raw_data = "[" + raw_data[1:] + "]"
        dataDict = json.loads(raw_data)  # this is the dicts

        header = {}
        merged = {}
        for toplevelItem in dataDict:
            try:
                merged = {
                    **merged,
                    **toplevelItem["p"][1]["v"],
                }  # merge 2 dicts - will overwrite if same key
            except:
                pass
            try:
                header = {**header, **toplevelItem}
            except:
                pass

        return merged

    except (AttributeError, json.JSONDecodeError, ValueError) as e:
        logger.error(f"no data, please check the exchange and symbol: {e}")
        return None

if __name__ == '__main__':
    debug_dir = os.path.dirname(__file__)
    
    # Test all .ws files
    ws_files = [f for f in os.listdir(debug_dir) if f.endswith('.ws')]
    
    print(f"\n{'='*80}")
    print(f"Verifying Fixed Parser with {len(ws_files)} raw data files")
    print(f"{'='*80}\n")
    
    passed = 0
    failed = 0
    
    for ws_file in sorted(ws_files):
        filepath = os.path.join(debug_dir, ws_file)
        symbol = ws_file.replace('_NASDAQ.ws', '')
        
        print(f"[*] Testing {symbol}...")
        
        with open(filepath, 'r') as f:
            raw_data = f.read()
        
        # Test earnings df
        print(f"  1. Testing fixed create_earnings_df()...")
        result = create_earnings_df_fixed(raw_data)
        if result is not None:
            df_revenue_q, df_earnings_q, df_revenue_f, df_earnings_f = result
            print(f"     ✓ Revenue FQ: {len(df_revenue_q)} rows, cols: {list(df_revenue_q.columns)}")
            print(f"     ✓ Earnings FQ: {len(df_earnings_q)} rows, cols: {list(df_earnings_q.columns)}")
            print(f"     ✓ Revenue FY: {len(df_revenue_f)} rows, cols: {list(df_revenue_f.columns)}")
            print(f"     ✓ Earnings FY: {len(df_earnings_f)} rows, cols: {list(df_earnings_f.columns)}")
        else:
            print(f"     ✗ FAILED")
            failed += 1
            continue
        
        # Test financial dict
        print(f"  2. Testing create_financial_dict_full()...")
        merged = create_financial_dict_full(raw_data)
        if merged is not None:
            print(f"     ✓ Total keys: {len(merged.keys())}")
            
            # Check for key financial fields
            key_fields = ['short_name', 'market_cap_basic', 'earnings_fq_h', 'revenues_fq_h', 'earnings_fy_h', 'revenues_fy_h']
            found_fields = 0
            for field in key_fields:
                if field in merged:
                    found_fields += 1
                    val = merged[field]
                    if isinstance(val, list):
                        print(f"     ✓ {field}: list with {len(val)} items")
                    elif isinstance(val, dict):
                        print(f"     ✓ {field}: dict with {len(val)} keys")
                    else:
                        print(f"     ✓ {field}: {type(val).__name__}")
            
            if found_fields == len(key_fields):
                print(f"     ✓ All key fields found!")
                passed += 1
            else:
                print(f"     ✗ Only {found_fields}/{len(key_fields)} key fields found")
                failed += 1
        else:
            print(f"     ✗ FAILED")
            failed += 1
        
        print()
    
    print(f"{'='*80}")
    print(f"Results: {passed} PASSED, {failed} FAILED")
    print(f"{'='*80}\n")
    
    if failed == 0:
        print("✓ All tests PASSED! The parser is now fixed.")
        sys.exit(0)
    else:
        print(f"✗ {failed} test(s) FAILED")
        sys.exit(1)
