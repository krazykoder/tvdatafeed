# TradingView Data Feed — Timeseries Variable Nomenclature Reference

**Generated:** 2026-05-17  
**Purpose:** Complete guide to understanding variable naming conventions in JSON financial data responses  
**Scope:** Earnings, revenue, financials, and related metrics from tvData.get_financials()

---

## Executive Summary

TradingView uses a **three-tier naming convention** to represent financial data:

| Tier | Pattern | Scope | Example |
|------|---------|-------|---------|
| **Point-in-time** | No suffix | Current/latest only | `earnings_per_share_basic_ttm` |
| **Current period** | `_fq`, `_fy`, `_current` | Single most recent value | `earnings_per_share_fq`, `market_cap_basic_fq` |
| **Historical series** | `_fq_h`, `_fy_h`, `_ttm_h` | Array of historical values | `earnings_fq_h`, `market_cap_basic_fy_h` |

The `_h` suffix marks **history arrays** containing multiple periods.

---

## Core Nomenclature Patterns

### Time Period Suffixes

| Suffix | Full Name | Scope | Array Length | Time Coverage |
|--------|-----------|-------|--------------|----------------|
| `_fq` | Fiscal Quarter | Current Q only | 1 value | Latest quarter |
| `_fq_h` | Fiscal Quarter History | Multi-quarter | 31–34 items | ~8 years |
| `_fy` | Fiscal Year | Current FY only | 1 value | Latest fiscal year |
| `_fy_h` | Fiscal Year History | Multi-year | 14–20 items | ~14 years |
| `_ttm` | Trailing Twelve Months | Rolling 12mo | 1 value | Last 12 months aggregate |
| `_ttm_h` | TTM History | Multi-year rolling | 8+ items | Multiple rolling periods |
| `_fh` | Fiscal Half-year | Current H only | 1 value | Latest half-year |
| `_mc` | Market Cap aggregated | Current | 1 value | Latest market snapshot |
| `_current` | Current snapshot | Latest | 1 value | Right-now value |
| `_next_` | Forecast | Forward-looking | 1 value | Next reported period |

### History Array Marker

**`_h` Suffix** — Universal history indicator appended to period types:

- `{fieldname}_fq_h` — Array of quarterly values (newest to oldest)
- `{fieldname}_fy_h` — Array of annual values (newest to oldest)
- `{fieldname}_ttm_h` — Array of rolling 12-month values
- `{fieldname}_h` — Generic history (period determined by context)

---

## JSON Schema Design Patterns

### Pattern 1: Earnings Metrics (Most Common)

```json
// Scalar: Current period value only
"earnings_per_share_fq": 9.4,
"earnings_per_share_fy": 35.52,
"earnings_per_share_basic_ttm": 35.52,

// Array: Historical timeseries
"earnings_fq_h": [
  {
    "Actual": 9.4,
    "Estimate": 9.2,
    "FiscalPeriod": "2024-Q3",
    "IsReported": true,
    "Type": 22
  },
  // ... 30 more quarters back to 2016
],

"earnings_fy_h": [
  {
    "Actual": 35.52,
    "Estimate": 35.0,
    "FiscalPeriod": "2024-FY",
    "IsReported": true,
    "Type": 22
  },
  // ... 13 more years back to 2011
]
```

**Object structure per element:**
- `Actual`: Reported value
- `Estimate`: Analyst estimate (if available)
- `FiscalPeriod`: Period identifier (e.g., "2024-Q3", "2024-FY")
- `IsReported`: Boolean — whether finalized/reported
- `Type`: Numeric code for report type (22 = earnings)

---

### Pattern 2: Simple Numeric Arrays (No Sub-objects)

```json
// Floating-point arrays (margins, ratios)
"pre_tax_margin_fy_h": [
  18.1346973702966,
  30.7078936575404,
  34.9334635760047,
  // ... ~14 years of values
],

// Integer arrays (dollars, counts)
"total_debt_fy_h": [
  6043090000,
  6057383000,
  5952000000,
  // ... ~14 years of values
],

// Mixed (nullable)
"deferred_income_non_current_fy_h": [
  null,
  null,
  0,
  0,
  18000000,
  // ... can include nulls
]
```

**Key characteristics:**
- Ordered newest-to-oldest
- All numeric (float or int)
- Often contain `null` for unavailable periods
- No sub-object nesting

---

### Pattern 3: Dual Representation (Current + History)

**Most fields follow this pattern:**

```json
{
  // Single value — latest reported for this FY
  "free_cash_flow_fy": 4012475000,
  
  // Array — all historical FY values
  "free_cash_flow_fy_h": [
    4012475000,    // FY 2024 (index 0, newest)
    3031191000,    // FY 2023
    2969559000,    // FY 2022
    // ... 11 more years
  ],

  // Rolling aggregate — last 12 months
  "free_cash_flow_ttm": 4012475000,

  // Alternative: FY only (no quarterly)
  "capital_expenditures_fy": -389165000,
  "capital_expenditures_fy_h": [ /* 14 values */ ]
}
```

**Usage:**
- Use scalar (`_fq`, `_fy`) for **latest point-in-time value**
- Use array (`_fq_h`, `_fy_h`) for **trend analysis & multi-year comparisons**
- Use `_ttm` to avoid manual quarterly aggregation

---

## Complete Field Categories

### 1. Income Statement (Earnings, Revenue, Expenses)

| Field | `_fq` | `_fq_h` | `_fy` | `_fy_h` | `_ttm` | Notes |
|-------|-------|---------|-------|---------|--------|-------|
| `earnings_per_share_basic` | ✓ | ✓ | — | ✓ | ✓ | Most basic EPS |
| `earnings_per_share_diluted` | ✓ | ✓ | — | ✓ | ✓ | Diluted shares |
| `net_income` | ✓ | ✓ | ✓ | ✓ | ✓ | Bottom-line profit |
| `total_revenue` | — | — | ✓ | ✓ | ✓ | Revenue only at FY/TTM |
| `operating_cash_flow_per_share` | ✓ | ✓ | — | ✓ | — | Cash from operations |
| `pre_tax_income` / `pretax_income` | ✓ | ✓ | ✓ | ✓ | — | Before taxes |
| `ebit` / `ebitda` | ✓ | ✓ | ✓ | ✓ | ✓ | Operating profit metrics |
| `gross_margin` / `net_margin` | — | — | ✓ | ✓ | — | Percentages, FY/TTM only |

### 2. Balance Sheet (Assets, Liabilities, Equity)

| Field | `_fq` | `_fq_h` | `_fy` | `_fy_h` | Notes |
|-------|-------|---------|-------|---------|-------|
| `total_assets` | ✓ | ✓ | ✓ | ✓ | Snapshot at period end |
| `total_liabilities` | ✓ | ✓ | ✓ | ✓ | All obligations |
| `current_ratio` | ✓ | ✓ | ✓ | ✓ | Current assets / current liabilities |
| `quick_ratio` | ✓ | ✓ | ✓ | ✓ | Excludes inventory |
| `book_value_per_share` | ✓ | ✓ | ✓ | ✓ | Equity per share |
| `cash_n_equivalents` | ✓ | ✓ | ✓ | ✓ | Liquid cash |
| `total_debt` | ✓ | ✓ | ✓ | ✓ | All debt outstanding |

### 3. Cash Flow Statement

| Field | `_fq` | `_fq_h` | `_fy` | `_fy_h` | `_ttm` | Notes |
|-------|-------|---------|-------|---------|--------|-------|
| `cash_f_operating_activities` | ✓ | ✓ | ✓ | ✓ | ✓ | Operating CF |
| `cash_f_investing_activities` | ✓ | ✓ | ✓ | ✓ | ✓ | Investment CF |
| `cash_f_financing_activities` | ✓ | ✓ | ✓ | ✓ | ✓ | Financing CF |
| `capital_expenditures` / `capex` | ✓ | ✓ | ✓ | ✓ | ✓ | CapEx spend |
| `free_cash_flow` | ✓ | ✓ | ✓ | ✓ | ✓ | Operating CF − CapEx |
| `dividends_cash_flow` | ✓ | ✓ | ✓ | ✓ | ✓ | Dividend payments |

### 4. Financial Ratios & Metrics

| Field | `_fq` | `_fq_h` | `_fy` | `_fy_h` | `_ttm` | Notes |
|-------|-------|---------|-------|---------|--------|-------|
| `return_on_assets` | ✓ | ✓ | ✓ | ✓ | — | ROA (%) |
| `return_on_equity` | ✓ | ✓ | ✓ | ✓ | — | ROE (%) |
| `price_earnings` | ✓ | — | ✓ | — | ✓ | P/E ratio |
| `price_book_ratio` | ✓ | — | ✓ | — | ✓ | P/B ratio |
| `price_sales_ratio` | ✓ | — | ✓ | — | ✓ | P/S ratio |
| `debt_to_equity` | ✓ | ✓ | ✓ | ✓ | — | Leverage ratio |
| `enterprise_value` | — | — | ✓ | ✓ | — | EV (aggregated) |

### 5. Per-Share Metrics

| Field | `_fq` | `_fq_h` | `_fy` | `_fy_h` | `_ttm` | Notes |
|-------|-------|---------|-------|---------|--------|-------|
| `earnings_per_share_*` | ✓ | ✓ | ✓ | ✓ | ✓ | Earnings/share |
| `book_value_per_share` | ✓ | ✓ | ✓ | ✓ | — | Equity/share |
| `cash_per_share` | ✓ | ✓ | ✓ | ✓ | — | Cash/share |
| `capex_per_share` | ✓ | ✓ | ✓ | ✓ | ✓ | CapEx/share |
| `revenue_per_share` | ✓ | ✓ | ✓ | ✓ | ✓ | Revenue/share |
| `dividends_per_share` | ✓ | ✓ | ✓ | ✓ | ✓ | Dividend/share |

### 6. Valuation Snapshot (Current/Latest only)

| Field | Type | Notes |
|-------|------|-------|
| `market_cap_basic` | Scalar | Market cap at latest price |
| `market_cap_basic_fq` | Scalar | Market cap at quarter-end |
| `market_cap_basic_fq_h` | Array | Market cap history per quarter |
| `enterprise_value_current` | Scalar | EV at latest snapshot |
| `enterprise_value_fy` | Scalar | EV for fiscal year |
| `enterprise_value_ebitda` | Scalar | EV/EBITDA ratio |

---

## Advanced Patterns

### Pattern A: Forecasts (Future-looking)

Fields prefixed with `_next_` or `_forecast_`:

```json
"earnings_per_share_forecast_next_fq": 9.932792,
"revenue_forecast_next_fy": 13519336095,
"earnings_release_next_date_fq": 1784808000,
"earnings_release_next_date_fy": 1784808000
```

**Characteristics:**
- Single values only (no `_h` arrays)
- Analyst consensus estimates
- May be null if not available
- Updated as earnings dates change

### Pattern B: Multi-dimensional Timeseries

Some fields contain nested objects with dates and segment data:

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
      // ... more segments
    ]
  }
  // ... more years
]
```

**Use case:** Segment breakdown by business line (common in tech/semiconductors)

### Pattern C: Rating & Credit Indicators

```json
"issuer_snp_rating_st_h": [
  {
    "date": 1736380800,  // Unix timestamp
    "outlook": null,
    "rating": 700       // Numeric code for rating
  },
  {
    "date": 1667952000,
    "outlook": null,
    "rating": 680
  }
],

"issuer_fitch_rating_lt_h": [
  // Empty if not rated
]
```

**Pattern:** Date + metadata tuple (for credit ratings, outlooks)

### Pattern D: Currency & Rates

**Standalone objects** (not timeseries):

```json
"rates_ttm": {
  "time": 1774915200,
  "to_aud": 1.44959,
  "to_cad": 1.390975,
  "to_chf": 0.799194,
  "to_cny": 6.899883,
  "to_eur": 0.865524,
  "to_gbp": 0.75643,
  "to_jpy": 158.780565,
  "to_usd": 1
},

"rates_current": {
  "time": 1778976000,
  // ... same currency conversions
}
```

**Purpose:** FX rates for converting values to different currencies

---

## Timeseries Array Ordering

**All `_h` arrays are ordered newest-to-oldest (reverse chronological):**

```python
earnings_fq_h[0]   # Most recent quarter (Q3 2024)
earnings_fq_h[1]   # Prior quarter (Q2 2024)
earnings_fq_h[2]   # Q1 2024
# ... older quarters
earnings_fq_h[30]  # Oldest quarter (~8 years ago)
```

**To create a normal chronological DataFrame:**

```python
import pandas as pd

# Reverse to chronological order
df = pd.DataFrame(earnings_fq_h[::-1])
df = df.sort_values('FiscalPeriod')
```

---

## Nullable Fields

Many `_h` arrays contain `null` values where data is unavailable:

```json
"deferred_income_non_current_fy_h": [
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  null,
  0,
  18000000
]
```

**Reasons for null:**
- Field not applicable to company type (e.g., deferred items for startups)
- Data not published for that period
- Accounting change made the metric unavailable
- Negative/undefined values represented as null

**Handling in Python:**

```python
df = pd.DataFrame(earnings_fq_h)
df = df.fillna(0)  # or .dropna(how='all')
df['Actual'] = pd.to_numeric(df['Actual'], errors='coerce')
```

---

## Summary: When to Use Each Pattern

| Use Case | Pattern | Example |
|----------|---------|---------|
| Get latest earnings | `earnings_per_share_fq` | Current quarter EPS |
| Last 12 months aggregate | `earnings_per_share_ttm` | Rolling 12-month EPS |
| Multi-year trend | `earnings_per_share_fy_h` | Array of annual EPS |
| Quarterly trends | `earnings_fq_h` | Array of quarterly EPS |
| Analyst forecast | `earnings_per_share_forecast_next_fq` | Next Q estimate |
| Market valuation | `market_cap_basic_fq` | Market cap at quarter-end |
| Multi-year valuation trends | `market_cap_basic_fq_h` | Market cap per quarter |

---

## Key Implementation Notes

### 1. Data Freshness
- `_current` fields: Real-time or latest snapshot
- `_fq`, `_fy`: Updated after earnings release
- `_h` arrays: Lag by 1–2 quarters for full history

### 2. Comparability
- TTM metrics overlap quarters (Q1–Q4 rolling)
- FY metrics are non-overlapping (cleanly separate years)
- Use FY data for year-over-year comparisons

### 3. Segment & Period Mapping
- `FiscalPeriod` field maps each `_h` array element to a period (e.g., "2024-Q3" or "2024-FY")
- Always use this field to align data across arrays

### 4. Null Handling
- Check for `null` before arithmetic
- Some fields intentionally have gaps (no history available)
- Safe default: `df.fillna(method='ffill')` or interpolate

---

## Field Density by Company Type

| Company Type | Typical Fields | Coverage |
|--------------|---------|----------|
| **Large-cap Tech** | 1,200+ | Complete, 14+ FY, 34+ Q |
| **Mid-cap Industrial** | 900–1,100 | Good, 14 FY, 28+ Q |
| **Small-cap** | 600–800 | Partial, 8–10 FY, 16+ Q |
| **Foreign ADR** | 500–1,000 | May have fewer/older Q |
| **Non-profitable** | 400–600 | Limited metrics, fewer Q |

---

## File Version History

| Date | Notes |
|------|-------|
| 2026-05-17 | Initial documentation; 1,300+ fields analyzed; 14 company years, 31–34 quarters standard |

---

## Related Files

- [data_extract/variables_definitions.md](variables_definitions.md) — Field-by-field glossary
- [data_extract/variables_extraction_summary.json](variables_extraction_summary.json) — Auto-extracted field inventory
- [debug/METRICS_ANALYSIS_REPORT.md](../debug/METRICS_ANALYSIS_REPORT.md) — Metrics count & validation
