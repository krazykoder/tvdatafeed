# tvDatafeed Parser Fix - Debug Summary

## Problem Identified
The `get_financials()` function was failing to parse websocket JSON data into proper DataFrames. The issue was in the `__create_earnings_df()` method in [main.py](../tvDatafeed/main.py#L256).

## Root Cause Analysis
The original code used `pd.read_json(..., lines=True)` which expects JSONL format (JSON Lines - one JSON object per line). However, the extracted financial data from the websocket is in **array format** `[{...}, {...}, ...]`, causing a `FileNotFoundError` as pandas tried to interpret the JSON string as a file path.

### Original Code (Broken)
```python
def __create_earnings_df(raw_data):
    """Extracts Revenues and Earnings : FY and FQ"""
    try:
        out = re.search('"revenues_fq_h":\[(.+?)\]', raw_data).group(1)
        df_revenue_q = pd.read_json(out, lines=True)  # ❌ FAILS HERE
        # ... more code
```

**Error:**
```
FileNotFoundError: File {"Actual":89584000000,"Estimate":77088700724,...} does not exist
```

## Solution Implemented
Changed the parsing approach to:
1. Extract the JSON array as a string
2. Parse it with `json.loads()` first
3. Convert the parsed data to a DataFrame

### Fixed Code
```python
def __create_earnings_df(raw_data):
    """Extracts Revenues and Earnings : FY and FQ"""
    try:
        out = re.search(r'"revenues_fq_h":\[(.+?)\]', raw_data).group(1)
        data = json.loads("[" + out + "]")  # ✓ Parse JSON first
        df_revenue_q = pd.DataFrame(data)   # ✓ Then create DataFrame
        # ... more code
```

## Changes Made
- **File**: [tvDatafeed/main.py](../tvDatafeed/main.py#L256-L276)
- **Function**: `__create_earnings_df()` (lines 256-276)
- **Changes**:
  - Replaced 4 `pd.read_json(out, lines=True)` calls with `json.loads("[" + out + "]")` followed by `pd.DataFrame(data)`
  - Improved exception handling to catch `json.JSONDecodeError` and `ValueError` in addition to `AttributeError`
  - Added descriptive error messages

## Testing & Verification

### Test Coverage
Created comprehensive debug scripts in [debug/](./):

1. **download_raw_data.py** - Downloads raw websocket data for 5 test symbols
   - AAPL, AMD, AVGO, KLAC, MU (NASDAQ)
   - Saves as `.ws` files for offline testing

2. **test_parser.py** - Analyzes raw data structure and tests parsing steps

3. **test_parsing_approaches.py** - Tests 4 different parsing approaches
   - Approach 1: Original (broken) ❌
   - Approach 2: Parse JSON first ✅ **SELECTED**
   - Approach 3: Using DataFrame.from_records() ✅
   - Approach 4: Direct list comprehension ❌

4. **test_actual_functions.py** - Tests with original functions (shows the bug)

5. **verify_fix.py** - Verifies the fix works on all 5 test symbols ✅

6. **test_end_to_end.py** - End-to-end test with tvData class ✅

### Test Results

#### Before Fix
```
✗ FileNotFoundError for all 5 symbols
```

#### After Fix
```
================================================================================
Results: 5 PASSED, 0 FAILED
================================================================================
✓ All tests PASSED! The parser is now fixed.

Sample output for KLAC:
  ✓ Revenue FQ: 34 rows, cols: ['Actual', 'Estimate', 'FiscalPeriod', 'IsReported', 'Type']
  ✓ Earnings FQ: 34 rows, cols: ['Actual', 'Estimate', 'FiscalPeriod', 'IsReported', 'Type']
  ✓ Revenue FY: 14 rows, cols: ['Actual', 'Estimate', 'FiscalPeriod', 'IsReported', 'Type']
  ✓ Earnings FY: 14 rows, cols: ['Actual', 'Estimate', 'FiscalPeriod', 'IsReported', 'Type']
  ✓ Total keys: 1430
  ✓ Symbol: KLAC
  ✓ Market Cap: 235693835721
  ✓ Contains earnings_fq_h: 34 items
  ✓ Contains revenues_fq_h: 34 items
```

## How to Use the Debug Tools

### 1. Download Raw Data
```bash
~/.venv/venv38/bin/python debug/download_raw_data.py
```
This creates `.ws` files for offline testing without API calls.

### 2. Verify the Fix
```bash
~/.venv/venv38/bin/python debug/verify_fix.py
```
Tests the fixed parser against all downloaded data files.

### 3. End-to-End Test
```bash
~/.venv/venv38/bin/python debug/test_end_to_end.py
```
Tests with the actual `tvData` class.

## Data Structure Notes
The websocket data is structured as:
```json
~m~<size>~m~{JSON object 1}~m~<size>~m~{JSON object 2}...~m~<size>~m~{final message}
```

Financial fields are nested within:
- `dataDict[4]['p'][1]['v']['revenues_fq_h']` - Array of quarterly revenue data
- `dataDict[4]['p'][1]['v']['earnings_fq_h']` - Array of quarterly earnings data
- `dataDict[4]['p'][1]['v']['revenues_fy_h']` - Array of annual revenue data
- `dataDict[4]['p'][1]['v']['earnings_fy_h']` - Array of annual earnings data

Each financial data point contains: `Actual`, `Estimate`, `FiscalPeriod`, `IsReported`, `Type`

## Additional Observations

### Syntax Warnings
There are some regex escape sequence warnings in the code (lines 153, 159 in main.py) that should be fixed by using raw strings (`r"..."`) for all regex patterns.

### Future Improvements
1. Fix remaining regex syntax warnings throughout main.py
2. Add type hints to the parser functions
3. Consider validating the DataFrame structure (required columns, data types)
4. Add more comprehensive error messages for debugging

## Impact
- ✅ Fixes the `get_financials()` function entirely
- ✅ Returns proper DataFrames for Revenue/Earnings (FY and FQ)
- ✅ Returns complete financial dictionary with 1400+ keys
- ✅ All financial metrics are now accessible
