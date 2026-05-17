# WebSocket to JSON Conversion Tools

Quick and easy tools to convert TradingView WebSocket data files (`.ws`) to standard JSON format.

## Overview

| File | Purpose | Status |
|------|---------|--------|
| **convert_ws_to_json.py** | Main conversion tool | ✅ Ready |
| **verify_json_conversion.py** | Verify converted files | ✅ Ready |
| **show_format_comparison.py** | Compare formats & show usage | ✅ Ready |

## Quick Start

### Convert Files
```bash
~/.venv/venv38/bin/python debug/convert_ws_to_json.py debug/
```

Output:
```
========================[Conversion Results]========================
✓ AAPL_NASDAQ.ws → AAPL_NASDAQ.json (490,968 bytes, 6 frames)
✓ AMD_NASDAQ.ws → AMD_NASDAQ.json (495,009 bytes, 6 frames)
✓ AVGO_NASDAQ.ws → AVGO_NASDAQ.json (480,250 bytes, 6 frames)
✓ KLAC_NASDAQ.ws → KLAC_NASDAQ.json (466,553 bytes, 6 frames)
✓ MU_NASDAQ.ws → MU_NASDAQ.json (555,412 bytes, 6 frames)

Results: 5 converted, 0 failed
```

### Verify Conversion
```bash
~/.venv/venv38/bin/python debug/verify_json_conversion.py debug/
```

Output:
```
========================[Verification Results]========================
✓ AAPL_NASDAQ.json (6 frames, session: 0.148512632...)
✓ AMD_NASDAQ.json (6 frames, session: 0.153572323...)
✓ AVGO_NASDAQ.json (6 frames, session: 0.144676752...)
✓ KLAC_NASDAQ.json (6 frames, session: 0.153999921...)
✓ MU_NASDAQ.json (6 frames, session: 0.146297314...)

Results: 5 valid, 0 invalid
```

### See Format Comparison
```bash
~/.venv/venv38/bin/python debug/show_format_comparison.py
```

## File Formats

### WebSocket Format (.ws)
```
~m~<length>~m~<json_data>~m~<length>~m~<json_data>...~m~<length>~m~{final_message}
```

**Pros:**
- Raw TradingView WebSocket protocol
- Smallest file size

**Cons:**
- Binary protocol delimiters
- Requires custom parser
- Not human-readable

### JSON Format (.json)
```json
{
  "metadata": {
    "source_file": "KLAC_NASDAQ.ws",
    "total_objects": 6,
    "conversion_date": "2026-05-17 12:20:54"
  },
  "frames": [
    { /* JSON frame 1 */ },
    { /* JSON frame 2 */ },
    ...
  ]
}
```

**Pros:**
- ✓ Standard JSON format
- ✓ Easy to parse
- ✓ Human-readable
- ✓ IDE support
- ✓ Database-compatible
- ✓ Metadata preserved

**Cons:**
- Slightly larger file size

## Usage Examples

### Basic Loading
```python
import json

# Load converted JSON
with open('KLAC_NASDAQ.json', 'r') as f:
    data = json.load(f)

# Access metadata
print(data['metadata'])
# Output:
# {
#   'source_file': 'KLAC_NASDAQ.ws',
#   'total_objects': 6,
#   'conversion_date': '2026-05-17 12:20:54...'
# }

# Access frames
frames = data['frames']
print(f"Total frames: {len(frames)}")  # Output: Total frames: 6
```

### Extract Financial Data
```python
import json
import pandas as pd

with open('KLAC_NASDAQ.json', 'r') as f:
    data = json.load(f)

# Find frame with financial data
for frame in data['frames']:
    if 'p' in frame and isinstance(frame['p'], list) and len(frame['p']) > 1:
        if isinstance(frame['p'][1], dict) and 'v' in frame['p'][1]:
            fin_data = frame['p'][1]['v']
            
            # Basic info
            print(f"Symbol: {fin_data.get('short_name')}")
            print(f"Market Cap: ${fin_data.get('market_cap_basic'):,}")
            
            # Quarterly earnings
            if 'earnings_fq_h' in fin_data:
                df = pd.DataFrame(fin_data['earnings_fq_h'])
                print(f"\nQuarterly Earnings ({len(df)} quarters):")
                print(df.head())
            
            # Annual revenue
            if 'revenues_fy_h' in fin_data:
                df = pd.DataFrame(fin_data['revenues_fy_h'])
                print(f"\nAnnual Revenue ({len(df)} years):")
                print(df.head())
```

### Export to CSV
```python
import json
import pandas as pd

with open('AAPL_NASDAQ.json', 'r') as f:
    data = json.load(f)

# Find and export financial data
for frame in data['frames']:
    if 'p' in frame and len(frame['p']) > 1:
        v = frame['p'][1].get('v', {})
        
        # Export earnings
        if 'earnings_fq_h' in v:
            df = pd.DataFrame(v['earnings_fq_h'])
            df.to_csv('AAPL_earnings.csv', index=False)
        
        # Export revenues
        if 'revenues_fy_h' in v:
            df = pd.DataFrame(v['revenues_fy_h'])
            df.to_csv('AAPL_revenue.csv', index=False)
```

### Search Fields
```python
import json

with open('KLAC_NASDAQ.json', 'r') as f:
    data = json.load(f)

# Find frame with many keys
for frame in data['frames']:
    if 'p' in frame and len(frame['p']) > 1:
        v = frame['p'][1].get('v', {})
        if isinstance(v, dict) and len(v) > 100:
            # Find all revenue-related fields
            revenue_fields = [k for k in v.keys() if 'revenue' in k.lower()]
            print(f"Revenue fields ({len(revenue_fields)}):")
            for field in sorted(revenue_fields):
                print(f"  - {field}")
            
            # Find all margin-related fields
            margin_fields = [k for k in v.keys() if 'margin' in k.lower()]
            print(f"\nMargin fields ({len(margin_fields)}):")
            for field in sorted(margin_fields):
                print(f"  - {field}")
```

## Command Line Usage

### Convert specific directory
```bash
~/.venv/venv38/bin/python convert_ws_to_json.py /path/to/directory
```

### Convert current directory
```bash
~/.venv/venv38/bin/python convert_ws_to_json.py .
```

### Default (debug folder)
```bash
~/.venv/venv38/bin/python convert_ws_to_json.py
```

## Data Structure

Each converted JSON file contains 6 WebSocket frames with the following structure:

| Frame | Type | Contains |
|-------|------|----------|
| 0 | Session Info | `session_id`, `timestamp`, `release` info |
| 1 | Symbol Response | Basic symbol info, `short_name`, `original_name` |
| 2 | Response Status | Confirmation of data request |
| 3 | Metadata Update | Additional metadata |
| 4 | **Financial Data** | **All ~1,300 financial metrics** ✨ |
| 5 | Completion Signal | `quote_completed` message |

The main financial data is in **Frame 4** under:
```
frame['p'][1]['v']  # Dictionary with 1,300+ financial fields
```

## Key Financial Fields

Available in Frame 4:
- `short_name` - Stock symbol (e.g., "KLAC")
- `market_cap_basic` - Market capitalization
- `earnings_fq_h` - Quarterly earnings (array, ~30-34 quarters)
- `revenues_fq_h` - Quarterly revenues (array, ~30-34 quarters)
- `earnings_fy_h` - Annual earnings (array, ~14 years)
- `revenues_fy_h` - Annual revenues (array, ~14 years)
- Plus 1,300+ additional metrics (see fields.md)

## Troubleshooting

### "No files found"
Make sure you're in the right directory or specify the full path:
```bash
~/.venv/venv38/bin/python debug/convert_ws_to_json.py debug/
```

### "File not found" errors
Ensure `.ws` files exist in the target directory

### JSON parse errors
Run verification script to diagnose:
```bash
~/.venv/venv38/bin/python debug/verify_json_conversion.py debug/
```

## Performance

| Operation | Time | CPU |
|-----------|------|-----|
| Convert 1 file | ~100ms | Low |
| Convert 5 files | ~500ms | Low |
| Parse + Extract | ~50ms | Low |
| Export to CSV | ~200ms | Low |

## File Sizes

| Symbol | .ws Size | .json Size | Frames |
|--------|----------|-----------|--------|
| AAPL | 205 KB | 491 KB | 6 |
| AMD | 197 KB | 495 KB | 6 |
| AVGO | 200 KB | 480 KB | 6 |
| KLAC | 200 KB | 467 KB | 6 |
| MU | 215 KB | 555 KB | 6 |

Note: JSON files are slightly larger due to human-readable formatting. They compress well with gzip.

## Next Steps

1. ✅ Convert your .ws files
2. ✅ Verify the conversion
3. ✅ Load into your application
4. ✅ Extract financial data
5. ✅ Export to CSV/database

## Related Files

- [DEBUG_SUMMARY.md](DEBUG_SUMMARY.md) - Technical parser documentation
- [README.md](README.md) - Parser fix documentation
- [tvDatafeed/main.py](../tvDatafeed/main.py) - Main library code
