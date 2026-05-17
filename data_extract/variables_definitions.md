# Variables Definitions — Quick Reference

**Version:** 2026-05-17  
**See Also:** 
- `NON_TIMESERIES_NOMENCLATURE.md` — **Comprehensive reference for scalar fields, metadata, and current-period metrics** ← Start here
- `TIMESERIES_NOMENCLATURE_REFERENCE.md` — Historical timeseries (`_h`, `_fq_h`, `_fy_h` arrays)
- `TIMESERIES_PATTERNS_DETAILED.md` — JSON structure patterns for timeseries extraction

---

## Quick Field Categories

### Real-Time Quote Data
- `lp` (last price), `bid`, `ask`, `bid_size`, `ask_size`
- `ch` (absolute change), `chp` (percent change), `volume`

### Company & Trading Identifiers
- `symbol`, `exchange`, `currency_code`, `isin`, `cusip`
- `sector`, `industry`, `country_code`

### Current Market Metrics
- `price_earnings`, `price_book_current`, `market_cap_basic`
- `beta_1_year`, `dividend_yield`, `price_52_week_high`

### Financial Snapshots (Latest Period, Not Arrays)
- `earnings_per_share_fq` / `_fy` / `_ttm` — EPS for FQ/FY/TTM (single values)
- `net_income_fq` / `_fy` — Net income (single values)
- `total_revenue_fy`, `free_cash_flow_fy` — Revenue & FCF (single values)
- See `NON_TIMESERIES_NOMENCLATURE.md` **§6** for complete list

### Session & Trading Configuration
- `timezone`, `minmov` / `minmove2`, `pricescale`
- `open_time`, `regular_close_time`, `is_tradable`

### Nested Objects
- `broker_names`: Broker symbol mappings
- `options-info`: Options chain metadata (families, series, strikes)
- `rates_ttm` / `rates_fy`: Currency conversion rates
- `figi`: Financial Instrument Global Identifier

---

## Timeseries Datasets (Arrays with Historical Data)

| Field | Type | Description |
|-------|------|-------------|
| `t` | int (seconds) | Frame message timestamp |
| `t_ms` | int (milliseconds) | Frame message timestamp (millisecond resolution) |
| `lp_time` | int (seconds) | Last trade time |
| `bar[0]` | int (seconds) | Bar timestamp (within timeseries arrays) |

---

## Scaling & Interpretation Rules

**Price Scaling:**
- When `pricescale` is present: `actual_price = raw_price / pricescale`
- Example: If `pricescale=10000`, raw price 195000 = actual price $19.50

**Timestamp Conversion:**
- Unix seconds → Datetime: `datetime.fromtimestamp(timestamp)`
- Unix milliseconds: Divide by 1000 first

**Financial Ratios:**
- All percentages (e.g., `chp`, `dividend_yield`): Divide by 100 for decimal form
- Example: `chp=2.5` means +2.5%, or 0.025 in decimal

**Per-Share Metrics:**
- Always verify `total_shares_outstanding > 0` before dividing
- Watch for stock splits: Use `has_adjustment` and `last_splits` to normalize historical data

---

## Extraction Priority

**Tier 1 — Always Available (Real-time)**
- `lp`, `bid`, `ask`, `volume`, `ch`, `chp`, `symbol`, `exchange`, `currency_code`

**Tier 2 — Usually Available (Fundamental)**
- `market_cap_basic`, `total_revenue_fy`, `net_income_fy`, `earnings_per_share_fq`
- `price_earnings`, `dividend_yield`, `pricescale`, `is_tradable`

**Tier 3 — Often Null (Small-cap, ADR, Foreign)**
- TTM arrays (`_ttm_h`), detailed balance sheet (`_fq_h` fields)
- Segment data, earnings forecasts, analyst ratings

**Tier 4 — Specialized**
- Options chain (`options-info`), regional popularity, broker mappings

---

## Cross-Reference Guide

| Use Case | Fields to Extract |
|----------|------------------|
| Real-time Quote Display | `lp`, `bid`, `ask`, `volume`, `ch`, `chp`, `currency_code` |
| Fundamental Valuation | `price_earnings`, `price_book_current`, `market_cap_basic`, `enterprise_value_current` |
| Dividend Screening | `dividend_yield`, `dps_common_stock_prim_issue_fy`, `dividend_payout_ratio_fy` |
| Company Research | `sector`, `industry`, `founded`, `ceo`, `web_site_url`, `business_description` |
| Financial Analysis | `net_income_fy_h`, `free_cash_flow_fy_h`, `total_debt_fy_h`, `return_on_equity_fy` |
| Risk Assessment | `beta_1_year`, `debt_to_equity_current`, `altman_z_score_ttm`, `current_ratio_fq` |

---

## Where to Find Each Type

| Field Category | Location |
|---|---|
| **Scalar Metrics & Metadata** | **`NON_TIMESERIES_NOMENCLATURE.md`** (comprehensive reference) |
| **Timeseries Arrays & Patterns** | **`TIMESERIES_NOMENCLATURE_REFERENCE.md`** |
| **Pattern Families & Extraction** | **`TIMESERIES_PATTERNS_DETAILED.md`** |
