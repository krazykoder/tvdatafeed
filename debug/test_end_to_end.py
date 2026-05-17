#!/usr/bin/env python3
"""
End-to-end test with the actual tvData class
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tvDatafeed import tvData

# Read a test file
debug_dir = os.path.dirname(__file__)
test_file = os.path.join(debug_dir, 'KLAC_NASDAQ.ws')

with open(test_file, 'r') as f:
    raw_data = f.read()

print("\n" + "="*80)
print("End-to-End Test with Fixed Parser")
print("="*80 + "\n")

# Create tvData instance (not calling the function, just using the methods)
tv = tvData()

# Test the earnings dataframe method
print("[*] Testing __create_earnings_df()...")
result = tv._tvData__create_earnings_df(raw_data)  # Access private method

if result is not None:
    df_revenue_q, df_earnings_q, df_revenue_f, df_earnings_f = result
    print(f"  ✓ Revenue FQ: {len(df_revenue_q)} rows")
    print(f"    Columns: {list(df_revenue_q.columns)}")
    print(f"    Sample:")
    print(f"    {df_revenue_q.head(2).to_string()}")
    
    print(f"\n  ✓ Earnings FQ: {len(df_earnings_q)} rows")
    print(f"    Columns: {list(df_earnings_q.columns)}")
    print(f"    Sample:")
    print(f"    {df_earnings_q.head(2).to_string()}")
    
    print(f"\n  ✓ Revenue FY: {len(df_revenue_f)} rows")
    print(f"  ✓ Earnings FY: {len(df_earnings_f)} rows")
else:
    print("  ✗ FAILED")
    sys.exit(1)

# Test the financial dict method
print("\n[*] Testing __create_financial_dict_full()...")
merged = tv._tvData__create_financial_dict_full(raw_data)  # Access private method

if merged is not None:
    print(f"  ✓ Total keys: {len(merged.keys())}")
    print(f"  ✓ Symbol: {merged.get('short_name', 'N/A')}")
    print(f"  ✓ Market Cap: {merged.get('market_cap_basic', 'N/A')}")
    print(f"  ✓ Contains earnings_fq_h: {len(merged.get('earnings_fq_h', []))} items")
    print(f"  ✓ Contains revenues_fq_h: {len(merged.get('revenues_fq_h', []))} items")
else:
    print("  ✗ FAILED")
    sys.exit(1)

print("\n" + "="*80)
print("✓ All end-to-end tests PASSED!")
print("="*80 + "\n")
