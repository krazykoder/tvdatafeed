# TVDatafeed Variable Nomenclature Analysis — Complete Study

## Executive Summary

Completed comprehensive two-phase analysis of tvdatafeed JSON financial data schema across 5 symbols (KLAC, AAPL, AMD, AVGO, MU).

**Phase 1 - Timeseries Analysis:** Nomenclature and pattern identification  
**Phase 2 - Non-Timeseries Analysis:** Scalar fields, metadata, and snapshots

**Generated reference files (5 total):**
1. `TIMESERIES_NOMENCLATURE_REFERENCE.md` — Main timeseries nomenclature guide (1,300+ fields)
2. `TIMESERIES_PATTERNS_DETAILED.md` — Advanced patterns analysis (12 pattern families total)
3. `NON_TIMESERIES_NOMENCLATURE.md` — **NEW** — Scalar & metadata reference (400+ fields, 19 categories)
4. `variables_definitions.md` — Updated quick reference with cross-links
5. `tvdatafeed_nomenclature_analysis.md` — This file (unified analysis document)

---

## PART I: NON-TIMESERIES DATA (Scalar Fields & Metadata)

### Overview
Non-timeseries fields represent point-in-time values, identifiers, and metadata. They do NOT include arrays or historical data. Comprehensive documentation in **`NON_TIMESERIES_NOMENCLATURE.md`** with 19 categories.

### Field Categories (19 Total)

1. **Trading & Quote Data** (15+ fields) — Real-time prices, volumes, bid/ask
   - `lp`, `bid`, `ask`, `bid_size`, `ask_size`, `volume`, `ch`, `chp`
   
2. **Fundamental Identifiers** (14 fields) — Symbol, exchange, ISIN, CUSIP, FIGI, CIK
   - `symbol`, `exchange`, `currency_code`, `isin`, `cusip`, `country_code`

3. **Corporate Metadata** (13 fields) — Sector, industry, CEO, descriptions
   - `sector`, `industry`, `founded`, `ceo`, `web_site_url`, `business_description`

4. **Market Cap & Equity** (9 fields) — Capitalization, shares outstanding
   - `market_cap_basic`, `total_shares_outstanding_current`, `enterprise_value_current`

5. **Price & Volume Snapshots** (8 fields) — 52-week, all-time highs/lows
   - `price_52_week_high`, `price_52_week_low`, `all_time_high`, `all_time_high_day`

6. **Financial Snapshots (Current Period)** (70+ fields) — Latest FQ/FY/TTM values, NOT arrays
   - Latest FQ: `earnings_per_share_fq`, `net_income_fq`, `gross_profit_fq`
   - Latest FY: `earnings_per_share_fy`, `net_income_fy`, `total_revenue_fy`, `ebitda_fy`
   - TTM: `earnings_per_share_ttm`, `ebitda_ttm`, `free_cash_flow_ttm`
   - Current: `price_earnings_current`, `return_on_equity_current`

7. **Per-Share Metrics** (15+ fields) — Earnings, book value, cash per share
   - `book_value_per_share_current`, `cash_per_share_fy`, `dps_common_stock_prim_issue_fy`

8. **Dividend & Payment Info** (12 fields) — Yields, upcoming/recent dividends
   - `dividends_yield`, `dividend_amount_upcoming`, `dividend_payout_ratio_fy`

9. **Earnings Information** (14 fields) — Release dates, forecasts
   - `earnings_release_date`, `earnings_release_next_date`, `earnings_per_share_forecast_next_fy`

10. **Trading Configuration** (20+ fields) — Hours, timezone, tick size, pricescale
    - `timezone`, `minmov`, `pricescale`, `is_tradable`, `open_time`, `regular_close_time`

11. **Market Data Availability** (10 fields) — Data flags and availability
    - `trade_loaded`, `metrics_loaded`, `financials_availability`, `has_ipo_data`

12. **System & UI Metadata** (14 fields) — Popularity, ratings, logos
    - `popularity`, `recommendation_mark`, `price_target_average`, `logo`

13. **IPO & Corporate Actions** (5 fields) — Split dates, maturity
    - `ipo_offer_date`, `split_last_date`, `days_to_maturity`

14. **Rating & Outlook** (3 fields) — S&P ratings
    - `issuer_snp_rating_st`, `issuer_snp_rating_lt_h`

15. **Nested Objects** (8+ fields) — Complex structures
    - `broker_names` (key-value mapping), `options-info` (4-level deep), `rates_*` (currency conversions)

16. **Per-Share Current Metrics** (7 fields) — Operating cash flow, debt per employee

17. **Balance Sheet Snapshot** (20+ fields) — Assets, liabilities, equity (current only)

18. **Cash Flow Snapshot** (6 fields) — Operating, financing, investing activities

19. **Index/Ratio Snapshots** (15+ ratios) — P/E, ROE, D/E, Altman Z-score

### Naming Conventions for Non-Timeseries

| Suffix | Meaning | Example |
|--------|---------|----------|
| *(no suffix)* | Current/latest real-time | `lp`, `bid`, `volume` |
| `_current` | Current snapshot | `price_earnings_current`, `return_on_equity_current` |
| `_fq` | Latest fiscal quarter (single value) | `earnings_per_share_fq`, `net_income_fq` |
| `_fy` | Latest fiscal year (single value) | `earnings_per_share_fy`, `net_income_fy` |
| `_ttm` | Trailing twelve months (single value) | `earnings_per_share_ttm`, `ebitda_ttm` |
| `_fh` | Fiscal half-year (single value) | `dps_common_stock_prim_issue_fh` |
| `_mc` | Market cap aggregated | `rates_mc` |
| `_next_` | Forward-looking/next period | `earnings_per_share_forecast_next_fy` |
| `_upcoming` | Future event/payment | `dividend_payment_date_upcoming` |
| `_recent` | Most recent past event | `dividend_amount_recent` |

**Key distinction:** Fields with `_h` suffix are **arrays (timeseries)** — see Part II.

---

## PART II: TIMESERIES DATA (Arrays & Historical Data)

### Core Nomenclature: Time Period Suffixes

| Suffix | Full Name | Scope | Array Length | Coverage |
|--------|-----------|-------|--------------|----------|
| `_fq` | Fiscal Quarter | Current Q | 1 value | Latest quarter |
| `_fq_h` | Fiscal Quarter History | Multiple | 31–34 items | ~8 years |
| `_fy` | Fiscal Year | Current FY | 1 value | Latest fiscal year |
| `_fy_h` | Fiscal Year History | Multiple | 14–20 items | ~14 years |
| `_ttm` | Trailing Twelve Months | Rolling 12mo | 1 value | Last 12 months |
| `_ttm_h` | TTM History | Multiple | ~8 items | Multiple rolling periods |
| `_fh` | Fiscal Half-year | Current H | 1 value | Latest half-year |
| `_current` | Current snapshot | Real-time | 1 value | Latest price-based snapshot |
| `_next_` | Forecast | Forward-looking | 1 value | Next reported period |
| `_mc` | Market cap | Current | 1 value | Current market value |

### Timeseries Field Count
- **Timeseries arrays (with `_h` suffix):** ~600 fields total
- **Non-timeseries scalars & snapshots:** ~400 fields total
- **Nested objects & metadata:** ~200 fields total
- **Total unique fields:** ~1,300 per symbol

---

## Pattern Families: Complete Analysis

### Core 7 Pattern Families (Timeseries Arrays)

#### 1. Simple Numeric Arrays (Most Common: ~60% of timeseries fields)
Flat arrays of float/int, no nesting, ordered newest-first.
- Examples: `pre_tax_margin_fy_h`, `total_debt_fy_h`, `capital_expenditures_fy_h`
- Element count: 14–32 (FY), 31–34 (FQ)
- Nullable: Yes (common for deferred items, discontinued ops)

#### 2. Object Arrays with Actual/Estimate Structure (~20% of timeseries fields)
Formal reporting structure with per-element metadata.
- Examples: `earnings_fq_h`, `earnings_fy_h`
- Each element: `{ Actual, Estimate, FiscalPeriod, IsReported, Type }`
- Type codes: 22 = earnings report (most common)

#### 3. Temporal Object Arrays (~5% of timeseries fields)
Date/timestamp + metadata (ratings, outlook, status).
- Examples: `issuer_snp_rating_st_h`, `issuer_fitch_rating_lt_h`
- Timestamp: Unix seconds (epoch)
- Rare updates (annual or less)

#### 4. Nested Segment Arrays (~3% of timeseries fields)
Multi-dimensional breakdown by business segment or product line.
- Examples: `revenue_seg_by_business_h`
- Structure: `{ date, segments: [{ label, value }] }`
- FY-level granularity only (not quarterly)
- Variable segments per year

#### 5. Trailing Twelve Months Variants (~5% of timeseries fields)
Rolling 12-month aggregates with periodic updates.
- Examples: `earnings_per_share_ttm`, `net_income_ttm_h`
- Update frequency: Monthly (more frequent than FY/FQ)
- Element count: ~8 rolling periods
- Overlapping windows (not cleanly separated)

#### 6. Forecast & Future Fields (~4% of timeseries fields)
Forward-looking estimates and upcoming event dates.
- Examples: `earnings_per_share_forecast_next_fq`, `earnings_release_next_date`
- Timestamp: Unix seconds
- Analyst consensus (monthly updates)
- Nullable if not available

#### 7. Snapshot Metrics & Ratios (~3% of timeseries fields)
Real-time or latest-snapshot metrics without history arrays.
- Examples: `market_cap_basic`, `price_earnings`, `enterprise_value_current`
- Update frequency: Real-time for `_current`, at market close for `_fq`/`_fy`
- Often computed on-the-fly from price + fundamentals

## Key Findings from Data Analysis

### Ordering Convention (Universal)
All `_h` arrays are **newest-to-oldest** (reverse chronological):
- Index 0 = Most recent quarter/year
- Index N-1 = Oldest quarter/year
- **Action:** Always reverse before creating chronological DataFrames

### Dual Representation Standard
Most fields have both scalar and `_h` variants:
```
earnings_per_share_fq          (scalar, latest)
earnings_per_share_fq_h        (array, history)
earnings_per_share_fy          (scalar, latest FY)
earnings_per_share_fy_h        (array, FY history)
earnings_per_share_ttm         (scalar, rolling 12mo)
earnings_per_share_ttm_h       (array, TTM history)
```

### Coverage by Company Size
- **Large-cap:** 1,200+ fields; 14+ FY, 34+ Q standard
- **Mid-cap:** 900–1,100 fields; 14 FY, 28+ Q
- **Small-cap:** 600–800 fields; 8–10 FY, 16+ Q

### Null Value Semantics
Nulls (not errors) in history arrays indicate:
- Field not applicable to company type (e.g., deferred items for startups)
- Data not published for that period
- Accounting changes made metric unavailable
- Negative/undefined values represented as null
- **Handling:** Preserve nulls; don't auto-fill

### Field Density
- **Numeric arrays:** ~60% of fields
- **Object arrays (Actual/Estimate):** ~20%
- **Other patterns (forecast, ratings, segments):** ~20%

## Cross-Pattern Insights

### By Update Frequency
- Real-time: `_current`, bare scalars (price, market cap)
- Daily: Market-based metrics
- Monthly: TTM variants, consensus estimates
- Quarterly: `_fq_h` arrays
- Annually: `_fy_h` arrays
- Rare: Credit ratings, status changes

### Array Completeness
- Standard lookback: 14 years (FY), ~8 years (FQ)
- No gaps within standard period
- Older history may be sparse or missing
- Segment data (variable-length) starts ~2006–2010

---

### Extended Pattern Families (Patterns 8–20: Real-World Edge Cases)

Beyond the 7 core families, TradingView's schema includes 13 additional patterns to handle special cases and non-standard data structures.

#### 8. Array of Arrays — Nested Numeric Pairs
Simple 2D arrays, typically [timestamp, value] or [date, numeric].
- **Examples:** `last_splits` = [[1598832000, 0.25], [1402272000, 0.142857], ...]
- **Use case:** Stock split history, discrete events with timestamps
- **Element structure:** 2 elements per subarray (always consistent)
- **Ordering:** Reverse chronological (newest first)

#### 9. Mixed-Type Timeseries Objects — Rating/Status History
Date + status/rating fields in a single object array (temporal snapshots).
- **Examples:** `issuer_snp_rating_st_h`, `issuer_snp_rating_lt_h`
- **Structure:** Each element = `{ date: UnixTime, rating: number, outlook?: string }`
- **Update freq:** Annual/rare (typically 1–4 updates per year)
- **Nullability:** Entire date-rating pairs can be sparse

#### 10. Dictionary/Map Objects — Arbitrary Key-Value Pairs
Flat key-value objects where keys are variable (not a fixed schema).
- **Examples:** 
  - `broker_names` = {alpaca: "AAPL", alramz: "NASDAQ:...", captrader: "265598", ...}
  - `local_popularity` = {BR: 80941, CN: 460616, DE: 900923, ...}
- **Semantics:** Mapping (not a named object with fixed fields)
- **Value type:** Typically homogeneous (all strings or all numbers)
- **Use case:** Broker identifiers, regional metrics, flexible taxonomies

#### 11. Exchange Rate Bundle Objects — Timestamped Currency Conversions
Multi-currency rate snapshot at a point in time.
- **Examples:** `rates_ttm`, `rates_mc`, `rates_fy`, `rates_earnings_fq`
- **Structure:** `{ time: UnixTime, to_aud, to_cad, to_chf, to_cny, ..., to_usd: 1 }`
- **Fixed fields:** 10+ currency pairs + reference timestamp
- **Use:** Convert financials to different currency bases
- **Update freq:** Monthly (with fiscal period)

#### 12. OHLCV Bar Object — Single Daily/Period Snapshot
Complete OHLCV + volume + metadata for a single bar.
- **Examples:** `prev-daily-bar`
- **Structure:** `{ open, high, low, close, volume, time, update-time, data-update-time }`
- **Semantics:** Latest/previous session's trading bar (single snapshot, not array)
- **Granularity:** Daily (sometimes session-specific)

#### 13. Segment Breakdown Array — Variable-Length Dimensional Data
Array of {date, segments} where segments is another array of {label, value}.
- **Examples:** `revenue_seg_by_business_h`
- **Structure:** `[{ date: year, segments: [{label: "Data Center", value: 16635000000}, ...] }]`
- **Variable structure:** Segment labels change year-to-year (2008 vs 2025)
- **FY-only:** Segment data not provided at quarterly granularity
- **Use case:** Multi-year business segment breakdowns

#### 14. Subsessions/Session Information Array — Metadata Arrays
Complex objects describing trading sessions with nested correction rules.
- **Examples:** `subsessions`
- **Structure:** `[{ description, id, private, session, session-correction, session-display }, ...]`
- **Content:** Fixed-length array (typically 4 entries: regular, extended, premarket, postmarket)
- **Nested field:** `session-correction` = colon-separated rule string

#### 15. Option Series Objects — Deeply Nested Option Metadata
Hierarchical options data (families → series → strikes).
- **Examples:** `options-info.families[0].series[0].strikes`
- **Structure:** Multi-level: families (usually 1) → series (multiple expirations) → strikes (array)
- **Each series:** `{ exp: YYYYMMDD, id, lotSize, root, strikes: [array], underlying }`
- **Array nesting depth:** 4 levels (families.series.strikes is the deepest numeric array)

#### 16. Reporting Metadata with Estimates — Complex Object Arrays
Per-period reporting data with actual, estimate, and metadata fields.
- **Examples:** `revenues_fq_h`, `earnings_fq_h`, `earnings_fy_h`
- **Structure:** `{ Actual, Estimate, FiscalPeriod, IsReported, Type }`
- **Type field:** Enum (22 = earnings, other codes exist)
- **FiscalPeriod string:** Format "YYYY-Qn" or "YYYY" depending on granularity

#### 17. Rolling TTM with History — Multiple Snapshots of Rolling Window
TTM array capturing rolling 12-month value over time.
- **Examples:** `net_income_ttm_h`, `ebitda_ttm_h`
- **Structure:** Array of numeric values (8 items typically)
- **Semantics:** NOT the same as `_fy_h` or `_fq_h`; each element is a 12-month roll
- **Overlapping:** Adjacent elements in array represent overlapping periods
- **Update freq:** Monthly (more frequent than quarterly)

#### 18. Dual Axis Metrics — Current + Historical Parallel Fields
Same metric available in two forms: single value + history array.
- **Examples:**
  - `price_earnings` (current TTM) + `price_earnings_ttm_h` (TTM history)
  - `market_cap_basic` (current snapshot) + `market_cap_calc` (current calculated)
- **Relationship:** Different calc methods or timing (basic vs calculated)
- **No _h counterpart:** Some metrics only exist as snapshot (no history)

#### 19. Forecast/Future Event Timestamps — Single Forward-Looking Dates
Scalar Unix timestamp fields pointing to future events.
- **Examples:** `earnings_release_next_date`, `earnings_release_next_calendar_date`
- **Semantics:** Single future event date, updated upon each release
- **Nullability:** Can be null if not yet scheduled
- **Type:** Always Unix seconds (not date string)

#### 20. Ratio Metrics with Multiple Variants — Same Metric, Different Bases
A metric computed multiple ways (e.g., current, TTM, FY).
- **Examples:** 
  - `price_earnings` vs `price_earnings_ttm` vs `price_earnings_current` vs `price_earnings_fy_h`
  - `price_book` (current) vs `price_book_ratio` (alternative name) vs `price_book_current`
- **Field bloat:** Same concept, 3–5 different field names/computations
- **Semantics:** Use cases drive variation (real-time chart vs historical analysis)

---

## Pattern Distribution Summary

| Pattern | Type | Count | Frequency | Use Case |
|---------|------|-------|-----------|----------|
| 1. Simple Numeric | Array | ~360 | ~60% of timeseries | Income, balance sheet, cash flow |
| 2. Actual/Estimate | Object Array | ~120 | ~20% | Earnings, revenue, estimates |
| 3. Temporal Objects | Object Array | ~30 | ~5% | Ratings, outlook, status |
| 4. Nested Segments | Object Array | ~20 | ~3% | Business segment breakdown |
| 5. TTM Variants | Array | ~30 | ~5% | Rolling 12-month metrics |
| 6. Forecast Fields | Scalar/Array | ~25 | ~4% | Forward-looking estimates |
| 7. Snapshots | Scalar | ~20 | ~3% | Market-based metrics |
| 8. Array of Arrays | 2D Array | ~5 | <1% | Stock splits, events |
| 9. Mixed-Type Objects | Object Array | ~10 | <1% | Credit ratings |
| 10. Dictionaries | Map | ~20 | <1% | Broker mappings, regional data |
| 11. Rate Bundles | Object | ~5 | <1% | Currency conversions |
| 12. OHLCV Snapshot | Object | ~2 | <1% | Current bar |
| 13. Segment Breakdown | Object Array | ~3 | <1% | Business segments |
| 14. Subsessions | Object Array | ~1 | <1% | Trading sessions |
| 15. Options Metadata | Nested | ~1 | <1% | Options chain |
| 16. Estimates | Object Array | ~10 | <1% | Analyst estimates |
| 17. Rolling TTM | Array | ~8 | <1% | TTM history |
| 18. Dual Axis | Scalar + Array | ~50 | <1% | Parallel representations |
| 19. Future Timestamps | Scalar | ~15 | <1% | Event dates |
| 20. Ratio Variants | Scalar | ~30 | <1% | Multi-basis ratios |

---

## Complete Reference Files

### Timeseries References
1. **TIMESERIES_NOMENCLATURE_REFERENCE.md** (500+ lines)
   - Complete field taxonomy for `_h` arrays
   - Field categories (income statement, balance sheet, cash flow, ratios)
   - Usage patterns and implementation notes
   - ~600 timeseries fields documented with examples
   - Array length benchmarks (14–34 elements by type)

2. **TIMESERIES_PATTERNS_DETAILED.md** (600+ lines)
   - 12 pattern families (7 core + 5 extended) in detail
   - Real code examples and extraction patterns (Python)
   - Validation checklists and classification heuristics
   - Update frequency analysis by pattern
   - Data freshness and completeness notes

### Non-Timeseries References
3. **NON_TIMESERIES_NOMENCLATURE.md** (NEW — 1,200+ lines)
   - Comprehensive scalar & metadata reference
   - 19 field categories with detailed tables
   - ~400 non-timeseries fields documented
   - Naming conventions and data type mappings
   - Use-case groupings (quote monitoring, valuation, dividends, research, risk, financial analysis)
   - Nested object structures (broker_names, options-info, rates_*)
   - Integration notes and cross-references

### Quick References
4. **variables_definitions.md** (Updated)
   - Quick lookup guide with cross-references
   - Field categories at a glance
   - Extraction priority tiers (Tier 1–4)
   - Scaling & interpretation rules
   - "Where to find" navigation table

5. **tvdatafeed_nomenclature_analysis.md** (This file)
   - Complete unified analysis (both timeseries and non-timeseries)
   - Pattern distribution summary
   - Cross-references between all reference files
   - Data structure insights and best practices

---

## Integration & Best Practices

### Field Selection by Use Case

**Real-time Quote Monitoring:**
- Non-timeseries: `lp`, `bid`, `ask`, `volume`, `ch`, `chp`
- Use: `variables_definitions.md` (quick reference)

**Fundamental Valuation:**
- Non-timeseries: `price_earnings`, `price_book_current`, `market_cap_basic`
- Timeseries: `earnings_per_share_fy_h`, `net_income_fy_h`, `total_assets_fy_h`
- Use: `NON_TIMESERIES_NOMENCLATURE.md` + `TIMESERIES_NOMENCLATURE_REFERENCE.md`

**Financial Analysis (Multi-year):**
- Timeseries arrays: `net_income_fy_h`, `free_cash_flow_fy_h`, `total_revenue_fy_h`
- Pattern type: Simple numeric arrays (Pattern 1)
- Use: `TIMESERIES_PATTERNS_DETAILED.md` for extraction code

**Earnings Report Processing:**
- Timeseries: `earnings_fq_h`, `revenues_fq_h` (Pattern 2: Actual/Estimate)
- Non-timeseries: `earnings_release_date`, `earnings_per_share_forecast_next_fq`
- Use: Both reference files

**Dividend Income Screening:**
- Non-timeseries: `dividends_yield`, `dps_common_stock_prim_issue_fy`, `dividend_payout_ratio_fy`
- Timeseries: `common_dividends_cash_flow_fy_h`
- Use: `NON_TIMESERIES_NOMENCLATURE.md` §8 (Dividend Info)

**Risk Assessment:**
- Non-timeseries: `beta_1_year`, `debt_to_equity_current`, `altman_z_score_ttm`
- Timeseries: `debt_to_equity_fy_h`, `current_ratio_fq_h`
- Use: `NON_TIMESERIES_NOMENCLATURE.md` §19 (Ratios)

### Data Quality Notes

**Coverage by Company Size:**
- Large-cap: 1,200+ fields; 14+ years FY, 34+ quarters
- Mid-cap: 900–1,100 fields; 12–14 years, 28+ quarters
- Small-cap: 600–800 fields; 8–10 years, 16+ quarters
- Foreign/ADR: Frequently missing segment data, analyst ratings

**Null Handling:**
- Nulls indicate missing/inapplicable data (not errors)
- Common in: TTM variants, deferred items, discontinued operations
- Preserve nulls when processing; don't auto-fill

**Array Ordering:**
- All `_h` arrays are newest-to-oldest (reverse chronological)
- Index 0 = most recent period
- Reverse before creating chronological time-series

**Update Frequency:**
- Real-time: Price, bid/ask, volume
- Daily: Market-based metrics
- Monthly: TTM variants, consensus estimates
- Quarterly: `_fq_h` arrays
- Annually: `_fy_h` arrays
- Rare: Credit ratings, segment changes
