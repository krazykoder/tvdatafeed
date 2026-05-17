#!/usr/bin/env python3
"""
Script to test the actual parser functions from main.py
"""
import json
import re
import sys
import os
import pandas as pd

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_earnings_df(raw_data):
    """Extracts Revenues and Earnings : FY and FQ"""
    try:
        out = re.search(r'"revenues_fq_h":\[(.+?)\]', raw_data).group(1)
        df_revenue_q = pd.read_json(out, lines=True)

        out = re.search(r'"earnings_fq_h":\[(.+?)\]', raw_data).group(1)
        df_earnings_q = pd.read_json(out, lines=True)

        out = re.search(r'"revenues_fy_h":\[(.+?)\]', raw_data).group(1)
        df_revenue_f = pd.read_json(out, lines=True)

        out = re.search(r'"earnings_fy_h":\[(.+?)\]', raw_data).group(1)
        df_earnings_f = pd.read_json(out, lines=True)

        return df_revenue_q, df_earnings_q, df_revenue_f, df_earnings_f
    except AttributeError as e:
        print(f"  ✗ AttributeError: {e}")
        return None
    except Exception as e:
        print(f"  ✗ {type(e).__name__}: {e}")
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

    except AttributeError as e:
        print(f"  ✗ AttributeError: {e}")
        return None
    except Exception as e:
        print(f"  ✗ {type(e).__name__}: {e}")
        return None

if __name__ == '__main__':
    debug_dir = os.path.dirname(__file__)
    
    # Test all .ws files
    ws_files = [f for f in os.listdir(debug_dir) if f.endswith('.ws')]
    
    print(f"\n{'='*80}")
    print(f"Testing {len(ws_files)} raw data files with actual parser functions")
    print(f"{'='*80}\n")
    
    for ws_file in sorted(ws_files):
        filepath = os.path.join(debug_dir, ws_file)
        
        print(f"[*] Testing {ws_file}...")
        
        with open(filepath, 'r') as f:
            raw_data = f.read()
        
        # Test earnings df
        print(f"  Testing create_earnings_df()...")
        result = create_earnings_df(raw_data)
        if result is not None:
            df_revenue_q, df_earnings_q, df_revenue_f, df_earnings_f = result
            print(f"    ✓ Revenue FQ: {len(df_revenue_q)} rows")
            print(f"    ✓ Earnings FQ: {len(df_earnings_q)} rows")
            print(f"    ✓ Revenue FY: {len(df_revenue_f)} rows")
            print(f"    ✓ Earnings FY: {len(df_earnings_f)} rows")
        
        # Test financial dict
        print(f"  Testing create_financial_dict_full()...")
        merged = create_financial_dict_full(raw_data)
        if merged is not None:
            print(f"    ✓ Total keys: {len(merged.keys())}")
            # Check for key financial fields
            key_fields = ['short_name', 'market_cap_basic', 'earnings_fq_h', 'revenues_fq_h']
            for field in key_fields:
                if field in merged:
                    val = merged[field]
                    if isinstance(val, list):
                        print(f"    ✓ {field}: list with {len(val)} items")
                    elif isinstance(val, dict):
                        print(f"    ✓ {field}: dict with {len(val)} keys")
                    else:
                        print(f"    ✓ {field}: {type(val).__name__}")
        
        print()
    
    print(f"{'='*80}")
    print("All tests completed!")
    print(f"{'='*80}")
