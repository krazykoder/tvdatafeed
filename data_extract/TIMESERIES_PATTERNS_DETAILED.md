# Advanced Timeseries Patterns — Analysis & Classification

**Generated:** 2026-05-17  
**Scope:** Beyond `_fq_h` and `_fy_h` — comprehensive enumeration of all timeseries structures  
**Data Source:** KLAC_NASDAQ.json, AMD_NASDAQ.json, and 3 other samples

---

## Overview: Complete Timeseries Pattern Taxonomy

The TradingView API uses **7 major timeseries pattern families**:

1. **Simple Numeric Arrays** — `_fq_h`, `_fy_h`, `_h` (most common)
2. **Object Arrays** — `_fq_h`, `_fy_h` with Actual/Estimate/Period structure
3. **Temporal Object Arrays** — Date + metadata tuples (ratings, forecasts)
4. **Nested Segment Arrays** — Multi-dimensional breakdown (revenue by segment)
5. **Rolling TTM Variants** — Trailing 12-month history
6. **Forecast/Future Fields** — `_next_`, `_forecast_` prefixes
7. **Snapshot Ratios** — Market-based metrics updated in real-time

---

## Pattern Family 1: Simple Numeric Arrays (Most Common)

### Description
Flat arrays of floating-point or integer values, ordered newest-to-oldest. No nesting.

### Examples

**Floating-point metrics (ratios, margins):**
```json
"pre_tax_margin_fy_h": [
  18.1346973702966,
  30.7078936575404,
  34.9334635760047,
  37.9215634490955,
  34.1187421856367
  // ... ~14 values, newest first
],

"return_on_assets_fy_h": [
  8.88669528909521,
  5.64883509738586,
  -12.3757970037106,
  7.5822779985597
  // ... ~20 values
]
```

**Integer metrics (dollars, counts):**
```json
"total_debt_fy_h": [
  6043090000,
  5952000000,
  6015000000,
  5965000000,
  6012000000
  // ... ~20 values
]
```

**Nullable arrays (some periods have no data):**
```json
"deferred_income_non_current_fy_h": [
  null, null, null, null, null,
  0, 0, 0,
  18000000
  // ... mixed nulls and values
],

"capital_expenditures_fy_h": [
  73810000, 83782000, 57323000, 22226000,
  // ... values only
]
```

### Characteristics
- **Element count:** 14–32 (FY), 31–34 (FQ)
- **Data type:** Float (ratios, per-share) or Int (dollars)
- **Nulls allowed:** Yes
- **Nested:** No
- **Sorted:** Reverse chronological (newest first)

### Usage
```python
df = pd.DataFrame({
    'value': field_name_fy_h[::-1],  # Reverse to chronological
    'year': range(2024 - len(field_name_fy_h), 2025)
})
```

---

## Pattern Family 2: Object Arrays with Actual/Estimate Structure

### Description
Most formal representation for earnings/revenue. Each array element is a dict with:
- `Actual`: Reported value
- `Estimate`: Analyst consensus estimate
- `FiscalPeriod`: String identifier (e.g., "2024-Q3")
- `IsReported`: Boolean
- `Type`: Numeric code (22 = earnings)

### Real Examples

**From KLAC_NASDAQ.json:**
```json
"earnings_fq_h": [
  {
    "Actual": 9.4,
    "Estimate": 9.2,
    "FiscalPeriod": "2024-Q3",
    "IsReported": true,
    "Type": 22
  },
  {
    "Actual": 8.7,
    "Estimate": 8.9,
    "FiscalPeriod": "2024-Q2",
    "IsReported": true,
    "Type": 22
  },
  {
    "Actual": 7.9,
    "Estimate": 8.1,
    "FiscalPeriod": "2024-Q1",
    "IsReported": true,
    "Type": 22
  }
  // ... 28 more quarters back to 2016
],

"earnings_fy_h": [
  {
    "Actual": 35.52,
    "Estimate": 35.0,
    "FiscalPeriod": "2024-FY",
    "IsReported": true,
    "Type": 22
  },
  {
    "Actual": 30.3674,
    "Estimate": 30.5,
    "FiscalPeriod": "2023-FY",
    "IsReported": true,
    "Type": 22
  }
  // ... 12 more years back to 2012
]
```

### Type Codes Observed
- `22` = Earnings report (most common)
- Other codes exist but less frequent in data

### Characteristics
- **Element count:** Up to 34 quarters, 14–20 years
- **Reporting lag:** 1–2 days post-earnings
- **Consensus data:** Updated monthly by analysts
- **Revision history:** Not included (only current estimate)

### Usage Pattern
```python
import pandas as pd

# Load and parse
earnings_df = pd.DataFrame(earnings_fq_h)
earnings_df['FiscalPeriod'] = pd.to_datetime(earnings_df['FiscalPeriod'])
earnings_df = earnings_df.sort_values('FiscalPeriod')

# Extract columns
actual = earnings_df['Actual'].values
estimates = earnings_df['Estimate'].values
beats = actual > estimates
```

---

## Pattern Family 3: Temporal Object Arrays (Ratings, Dates, Metadata)

### Description
Objects containing a date/timestamp plus metadata (rating, outlook, status). Used for credit ratings, status changes.

### Real Examples

**S&P Rating History:**
```json
"issuer_snp_rating_st_h": [
  {
    "date": 1736380800,    // Unix timestamp: 2025-01-08
    "outlook": null,
    "rating": 700          // Numeric code for rating (e.g., 700 = A+ equivalent)
  },
  {
    "date": 1667952000,    // Unix timestamp: 2022-11-09
    "outlook": null,
    "rating": 680          // Numeric code for A-equivalent
  }
]
```

**Fitch Rating History (may be empty):**
```json
"issuer_fitch_rating_lt_h": [
  // Empty array if not Fitch-rated
]
```

**Earnings Release Dates (implicit temporal series):**
```json
"earnings_release_date_fy_h": [
  1777493220,  // Unix seconds: 2025-04-25
  1746098220,  // Unix seconds: 2024-04-30
  // ... more dates
]
```

### Characteristics
- **Timestamp format:** Unix seconds (epoch)
- **Rating codes:** Numeric (not human-readable in raw data)
- **Outlooks:** null, "Positive", "Stable", "Negative"
- **Frequency:** Rare updates (annual or less)

### Usage Pattern
```python
import pandas as pd
from datetime import datetime

df = pd.DataFrame(issuer_snp_rating_st_h)
df['date'] = pd.to_datetime(df['date'], unit='s')
df = df.sort_values('date')
```

---

## Pattern Family 4: Nested Segment & Dimension Arrays

### Description
Revenue or metrics broken down by business segment, product line, or geographic region. Complex nested structure.

### Real Example (from AMD data)

```json
"revenue_seg_by_business_h": [
  {
    "date": 2025,
    "segments": [
      { "label": "Data Center", "value": 16635000000 },
      { "label": "Client and Gaming", "value": 14550000000 },
      { "label": "Embedded", "value": 3454000000 }
    ]
  },
  {
    "date": 2024,
    "segments": [
      { "label": "Data Center", "value": 12579000000 },
      { "label": "Client", "value": 7054000000 },
      { "label": "Embedded", "value": 3557000000 },
      { "label": "Gaming", "value": 2595000000 }
    ]
  },
  {
    "date": 2023,
    "segments": [
      { "label": "Data Center", "value": 6496000000 },
      { "label": "Gaming", "value": 6212000000 },
      { "label": "Embedded", "value": 5321000000 },
      { "label": "Client", "value": 5240000000 }
    ]
  }
  // ... more years, segments may vary by year
]
```

### Characteristics
- **Dimensionality:** 2D (year/segment)
- **Variable segments:** Different segments per year (restructuring, M&A)
- **Data type:** Integer (dollars, units)
- **Years only:** FY-level granularity (not quarterly)
- **Ordering:** Newest year first in array

### Usage Pattern
```python
import pandas as pd

# Explode segments into rows
records = []
for item in revenue_seg_by_business_h:
    for seg in item['segments']:
        records.append({
            'year': item['date'],
            'segment': seg['label'],
            'revenue': seg['value']
        })

df = pd.DataFrame(records)
pivot = df.pivot(index='year', columns='segment', values='revenue')
```

---

## Pattern Family 5: Trailing Twelve Months (TTM) Variants

### Description
Rolling 12-month aggregates. Less common than FY/FQ arrays, but provide continuous updated metrics.

### Observed Fields

**Single TTM value (most common):**
```json
"earnings_per_share_basic_ttm": 35.52,
"free_cash_flow_ttm": 4012475000,
"ebitda_per_share_ttm": 44.4785275142315,
"price_earnings_growth_ttm": 1.8738915986139728
```

**TTM History (rare):**
```json
"net_income_ttm_h": [
  5009000000,    // Latest rolling 12 months
  4335000000,    // Previous rolling period
  3306000000,
  2834000000,
  2227000000,
  1641000000,
  1826000000,
  1354000000     // ~8 rolling periods
]
```

### Characteristics
- **Update frequency:** Monthly (not quarterly/annual)
- **Overlap:** Each TTM includes last 12 months (rolling window)
- **Element count:** Typically 8 (one per year of history)
- **Use case:** Continuous monitoring of annual run-rate

### Differences vs. FY

| Metric | TTM | FY |
|--------|-----|-----|
| **Update** | Monthly | After earnings release |
| **Overlap** | 12-month rolling window | Clean fiscal year, no overlap |
| **Data points** | ~8 (monthly updates × years) | ~14 (one per fiscal year) |
| **Use** | Forward-looking annualized | Historical actual results |

---

## Pattern Family 6: Forecast & Future Fields

### Description
Forward-looking estimates and dates for upcoming events.

### Examples

**Analyst EPS forecasts:**
```json
"earnings_per_share_forecast_next_fq": 9.932792,
"earnings_per_share_forecast_next_fy": [values...],
"revenue_forecast_next_fy": 13519336095,
"revenue_forecast_next_fh": 7491769421  // Half-year forecast
```

**Upcoming event dates:**
```json
"earnings_release_next_date": 1785844800,            // Unix seconds
"earnings_release_next_date_fq": 1784808000,
"earnings_release_next_date_fy": 1784808000,
"earnings_release_next_calendar_date": 1782777600,
"earnings_release_next_trading_date_fy": [timestamp...]
```

**Dividend info:**
```json
"dividends_per_share_fq": 1.9,
"ex_date_upcoming": 1779105540,
"ex_dividend_date_recent": 1771286400
```

### Characteristics
- **Data:** Analyst consensus (for EPS/revenue forecasts)
- **Timing:** Dates are Unix seconds (epoch)
- **Frequency:** Updated monthly by consensus providers
- **Nullable:** Can be null if forecast not available

### Usage Pattern
```python
import pandas as pd
from datetime import datetime

next_earnings = datetime.fromtimestamp(earnings_release_next_date)
print(f"Next earnings: {next_earnings.strftime('%Y-%m-%d')}")

# Calculate days to earnings
days_to_earnings = (next_earnings - datetime.now()).days
```

---

## Pattern Family 7: Snapshot & Market-Based Metrics

### Description
Real-time or latest-snapshot metrics that don't have historical arrays. Updated continuously or at market close.

### Examples

**Market cap variations:**
```json
"market_cap_basic": 235693835721,          // Latest (real-time)
"market_cap_basic_fq": 192458711100,       // Quarter-end snapshot
"market_cap_basic_fq_h": [192458711100, 159349236440, ...],  // Quarterly history
"market_cap_basic_fy": 118258282020,       // FY-end snapshot
"market_cap_basic_fy_h": [118258282020, 8278416080, ...],    // Annual history
```

**Enterprise value:**
```json
"enterprise_value_current": 236881257721.0,  // Real-time EV
"enterprise_value_fy": 121398884000,         // FY snapshot
```

**Valuation ratios (computed, not stored):**
```json
"price_earnings": 53.51339432112447,         // Latest P/E
"price_earnings_ttm": 53.51339432112447,     // TTM-based P/E
"price_earnings_growth_ttm": 1.8738915986139728,  // PEG ratio
"price_book_ratio": 33.009,                  // P/B
```

### Characteristics
- **Update:** Real-time for `_current`, at market close for `_fq`/`_fy`
- **History:** May have `_fq_h` or `_fy_h` variants
- **Computation:** Often calculated on-the-fly from price + fundamentals
- **Nullable:** Usually non-null (derived from price + metrics)

---

## Cross-Field Pattern Summary

### By Update Frequency

| Frequency | Patterns | Examples |
|-----------|----------|----------|
| **Real-time** | `_current`, bare scalar | `lp`, `bid`, `ask`, `price_earnings` |
| **Daily** | `price_*`, `_current` | `market_cap_basic`, `enterprise_value_current` |
| **Monthly** | `_ttm_h`, consensus estimates | `earnings_per_share_forecast_next_fq` |
| **Quarterly** | `_fq_h`, `_fq` | `earnings_fq_h`, `net_income_fq` |
| **Annually** | `_fy_h`, `_fy` | `total_revenue_fy_h`, `free_cash_flow_fy` |
| **Rare** | `_h` (status/rating) | `issuer_snp_rating_st_h` |

### By Data Dimensionality

| Dimensionality | Patterns | Examples |
|---|---|---|
| **1D (scalar)** | Single values | `lp`, `earnings_per_share_fq`, `market_cap_basic` |
| **1D (array)** | Time series | `earnings_fq_h`, `total_debt_fy_h` |
| **2D (tuple)** | Date + metadata | `issuer_snp_rating_st_h`, `earnings_release_date_fy_h` |
| **3D (nested)** | Time + segments | `revenue_seg_by_business_h` |

### By Nesting Depth

| Depth | Nesting | Examples |
|-------|---------|----------|
| **None** | Scalar | `lp: 1804.32` |
| **Shallow (1)** | Array of scalars | `earnings_fy_h: [35.52, 30.37, ...]` |
| **Shallow (2)** | Array of objects | `earnings_fq_h: [{ Actual, Estimate, ... }]` |
| **Deep (3+)** | Nested objects + arrays | `revenue_seg_by_business_h: [{ date, segments: [] }]` |

---

## Completeness & Coverage

### Standard Coverage by Field Family

| Family | Fields in API | `_fq` variant | `_fq_h` variant | `_fy` variant | `_fy_h` variant | `_ttm` variant |
|--------|---|---|---|---|---|---|
| Income statement | ~30 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Balance sheet | ~40 | ✓ | ✓ | ✓ | ✓ | — |
| Cash flow | ~20 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Ratios | ~50 | ✓ | ✓ | ✓ | ✓ | ~ |
| Per-share | ~25 | ✓ | ✓ | ~ | ✓ | ✓ |
| Valuation | ~15 | ✓ | ~ | ✓ | ~ | ✓ |
| **Total** | **~180** | **High** | **High** | **High** | **High** | **Medium** |

---

## Extraction & Processing Patterns

### Pattern Recognition Heuristics

```python
def classify_field_pattern(field_name, value):
    """Identify which pattern family a field belongs to."""
    
    if isinstance(value, list):
        if len(value) == 0:
            return "empty_array"
        
        elem = value[0]
        
        if isinstance(elem, dict):
            if 'Actual' in elem and 'FiscalPeriod' in elem:
                return "earnings_object_array"  # Pattern 2
            elif 'date' in elem and 'outlook' in elem:
                return "temporal_metadata_array"  # Pattern 3
            elif 'date' in elem and 'segments' in elem:
                return "segment_array"  # Pattern 4
            else:
                return "generic_object_array"
        
        elif isinstance(elem, (int, float)):
            if any(v is None for v in value):
                return "nullable_numeric_array"  # Pattern 1 variant
            else:
                return "numeric_array"  # Pattern 1
        
        else:
            return "unknown_array"
    
    elif isinstance(value, dict):
        if 'time' in value and len(value) <= 15:
            return "rates_object"  # Pattern 7 (currency/rates)
        else:
            return "generic_object"
    
    else:  # scalar
        if "_current" in field_name:
            return "snapshot_scalar"  # Pattern 7
        elif "_next_" in field_name or "_forecast_" in field_name:
            return "forecast_scalar"  # Pattern 6
        else:
            return "metric_scalar"  # Pattern 1 variant
```

---

## Key Insights from Analysis

### 1. **Consistency in Ordering**
All `_h` arrays are ordered newest-to-oldest. Never chronological.  
**Action:** Always reverse before plotting/analysis.

### 2. **Dual Representation is Standard**
Most fields have both scalar and `_h` array:
- Scalar = latest/current
- Array = full history

**Action:** Use scalar for quick lookups, array for trends.

### 3. **Null Values are Semantic**
Nulls indicate missing data, not errors. Common in:
- Deferred items (balance sheet)
- Discontinued operations
- Accounting changes
- Non-applicable metrics

**Action:** Preserve nulls; don't auto-fill.

### 4. **Forecasts Have Shorter History**
TTM forecasts: ~8 values  
FY/FQ forecasts: 1 value (next period)

**Action:** Don't extrapolate from TTM history alone.

### 5. **Segment Data is Sparse**
Segment revenue/metrics only available at FY level, not quarterly.  
Segment count varies by year (M&A, restructuring).

**Action:** Expect variable-length segment arrays.

---

## Validation Checklist

When parsing new financial data:

- [ ] Check array ordering (should be newest-first)
- [ ] Verify `FiscalPeriod` matches field type (`Q3 2024` for `_fq_h`, `2024-FY` for `_fy_h`)
- [ ] Confirm array length (14–20 for FY, 31–34 for FQ)
- [ ] Test for nulls; document handling strategy
- [ ] Cross-check totals (FY sum ≈ 4×average quarterly for revenue)
- [ ] Validate TTM (should ≈ sum of last 4 quarters)
- [ ] Ensure timestamp fields are Unix seconds, not milliseconds

---

## References & Related Documentation

- [TIMESERIES_NOMENCLATURE_REFERENCE.md](TIMESERIES_NOMENCLATURE_REFERENCE.md) — Main nomenclature guide
- [variables_definitions.md](variables_definitions.md) — Field glossary
- [../debug/METRICS_ANALYSIS_REPORT.md](../debug/METRICS_ANALYSIS_REPORT.md) — Data validation report
