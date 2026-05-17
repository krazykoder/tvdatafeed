# Non-Timeseries Data Nomenclature Reference
**tvdatafeed v2.0.1** — Scalar fields, metadata, and snapshot metrics

Generated: 2026-05-17

---

## Overview

Non-timeseries fields represent point-in-time values, identifiers, metadata, and configuration. They do NOT include arrays or historical data. This reference covers:

1. **Trading & Quote Data** — Real-time prices, volumes, bid/ask
2. **Fundamental Identifiers** — Symbol, exchange, ISIN, CUSIP, FIGI
3. **Corporate Metadata** — Company name, sector, industry, description
4. **Market Metrics** — Market cap, enterprise value, shares outstanding
5. **Price & Volume Metadata** — 52-week highs/lows, open/close, averages
6. **Financial Snapshots** — Current-period values (not historical arrays)
7. **Trading Configuration** — Hours, session, timezone, tick size
8. **System/UI Fields** — Popularity, permissions, display settings
9. **Rating & Consensus** — Current S&P rating, recommendation counts
10. **Nested Objects** — Broker mappings, currency rates, options info

---

## 1. Trading & Quote Data (Real-time Prices)

| Field | Type | Description | Unit/Range |
|-------|------|-------------|-----------|
| `lp` | float | Last price (most recent trade) | Currency |
| `lp_time` | int | Timestamp of last price | Unix epoch (seconds) |
| `bid` | float | Current best bid price | Currency |
| `ask` | float | Current best ask price | Currency |
| `bid_size` | int/float | Quantity available at bid | Shares/contracts |
| `ask_size` | int/float | Quantity available at ask | Shares/contracts |
| `ch` | float | Absolute price change from prev_close | Currency (usually +/-) |
| `chp` | float | Percent change from prev_close | Percent (e.g., 2.5 = +2.5%) |
| `prev_close_price` | float | Previous session close | Currency |
| `volume` | int | Cumulative session volume | Shares/contracts |
| `average_volume` | int | Average daily volume (recent) | Shares |
| `open_price` | float | Current session open | Currency |
| `high_price` | float | Current session high | Currency |
| `low_price` | float | Current session low | Currency |
| `regular_close` | float | Regular trading session close | Currency |

**Usage:**
- Calculate spreads: `ask - bid`
- Session P/L: `(lp - open_price) / open_price * 100`
- Price momentum: Compare `chp` to historical averages

---

## 2. Fundamental Identifiers

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `symbol` | str | Trading symbol (ticker) | `AAPL`, `KLAC`, `0001.HK` |
| `short_name` | str | Short company name | `Apple` |
| `exchange` | str | Primary exchange code | `NASDAQ`, `NYSE`, `HKEX` |
| `listed_exchange` | str | Official listed exchange | `NASDAQ` |
| `currency_code` | str | Trading currency | `USD`, `EUR`, `CNY` |
| `currency_id` | str | Internal currency identifier | e.g., `4` for USD |
| `isin` | str | ISIN code | `US0378331005` (AAPL) |
| `cusip` | str | CUSIP code | `037833100` |
| `figi` | str or object | FIGI identifier (object: `SHARE_CLASS_FIGI`, `SECURITY_ID`, etc.) | `BBG000B9XRY4` |
| `cik-code` | str | SEC CIK number | `0000320193` (AAPL) |
| `type` | str | Instrument type | `stock`, `etf`, `bond`, `fund`, `index`, `forex`, `crypto` |
| `typespecs` | str | Additional type specification | `1` or `11` (internal codes) |
| `country_code` | str | Country of incorporation | `US`, `JP`, `CN` |
| `country` | str | Country name | `United States` |
| `region` | str | Geographic region | `North America`, `Asia-Pacific` |

**Usage:**
- Validate symbol format: Check `exchange` + `symbol` combination
- Regulatory lookups: Use `isin`, `cusip`, or `cik-code`
- Currency conversion: Use `currency_code` to determine rate application

---

## 3. Corporate Metadata

| Field | Type | Description |
|-------|------|-------------|
| `base_name` | str | Legal/base company name |
| `original_name` | str | Original/alternate company name |
| `short_description` | str | One-line company description |
| `description` | str | Medium-length company overview |
| `business_description` | str | Detailed business description |
| `sector` | str | Industry sector | 
| `industry` | str | Specific industry classification |
| `ceo` | str | Chief Executive Officer name |
| `web_site_url` | str | Official website URL |
| `founded` | int | Year founded | 
| `number_of_employees` | int | Current headcount |
| `number_of_shareholders` | int | Registered shareholder count |
| `logo` | object | Logo metadata (id, style, url) |
| `local_description` | str | Localized description (i18n) |

**Related i18n fields:**
- `industry-i18n-en` — English industry name
- `description-i18n-en` — English description
- `business_description-i18n-en` — English business description

---

## 4. Market Capitalization & Equity

| Field | Type | Description | Typical Range |
|-------|------|-------------|---------------|
| `market_cap_basic` | float/int | Market cap (price × shares outstanding) | Varies |
| `market_cap_calc` | float/int | Calculated market cap (alternative method) | Varies |
| `total_shares_outstanding_current` | float/int | Current shares outstanding (latest snapshot) | Millions/billions |
| `total_shares_outstanding_calculated` | float/int | Calculated shares outstanding | Millions/billions |
| `float_shares_outstanding` | float/int | Publicly tradeable shares | Millions/billions |
| `market_cap_basic_fq` | float/int | Market cap as of latest fiscal quarter | Varies |
| `total_shares_outstanding_fq` | float/int | Shares outstanding at FQ end | Varies |
| `enterprise_value_current` | float/int | EV = Market Cap + Debt - Cash (current) | Varies |
| `sum_for_enterprise_value` | float/int | Sum of EV components | Varies |

**Relationship:**
```
Market Cap = Price × Total Shares Outstanding
Enterprise Value = Market Cap + Total Debt - Cash
```

---

## 5. Price & Volume Snapshots (52-Week & Session)

| Field | Type | Description |
|-------|------|-------------|
| `price_52_week_high` | float | Highest price in last 52 weeks |
| `price_52_week_low` | float | Lowest price in last 52 weeks |
| `price_percent_change_52_week` | float | Percent change from 52-week low (%) |
| `all_time_high` | float | Highest price ever recorded |
| `all_time_high_day` | int | Date of all-time high (Unix timestamp) |
| `all_time_low` | float | Lowest price ever recorded |
| `all_time_low_day` | int | Date of all-time low (Unix timestamp) |
| `all_time_open` | float | First recorded open price |

**Usage:**
- Identify overbought/oversold: Compare `lp` to 52-week ranges
- Calculate momentum: `(lp - price_52_week_low) / (price_52_week_high - price_52_week_low)`

---

## 6. Financial Snapshot Metrics (Current Period Only)

These are **single values** for the most recent period, NOT historical arrays.

### Current Fiscal Quarter (Latest `_fq` without `_h` suffix)

| Field | Type | Description |
|-------|------|-------------|
| `earnings_per_share_fq` | float | EPS for latest fiscal quarter |
| `earnings_fiscal_period_fq` | str | Fiscal period label (e.g., `"2024-Q3"`) |
| `fiscal_period_fq` | str | Current fiscal period |
| `fiscal_period_end_fq` | int | Fiscal period end date (Unix timestamp) |
| `net_income_fq` | float/int | Net income (latest FQ) |
| `diluted_net_income_fq` | float/int | Diluted net income (latest FQ) |
| `gross_profit_fq` | float/int | Gross profit (latest FQ) |
| `operating_expenses_fq` | int | Operating expenses (latest FQ) |
| `pretax_income_fq` | float/int | Pre-tax income (latest FQ) |
| `income_tax_fq` | float/int | Income tax (latest FQ) |
| `ebit_fq` | float/int | EBIT earnings before interest/tax |
| `capital_expenditures_fq` | float/int | Capex (latest FQ) |
| `dividend_payout_ratio_fq` | float | Payout ratio as % |
| `earnings_publication_type_fq_h` | str | Publication type (array, but treated as lookup) |

### Current Fiscal Year (Latest `_fy` without `_h` suffix)

| Field | Type | Description |
|-------|------|-------------|
| `earnings_per_share_fy` | float | EPS for fiscal year |
| `earnings_per_share_basic_fy` | float | Basic EPS |
| `earnings_per_share_diluted_fy` | float | Diluted EPS |
| `net_income_fy` | float/int | Net income (fiscal year) |
| `total_revenue_fy` | float/int | Total revenue (fiscal year) |
| `ebitda_fy` | float/int | EBITDA (fiscal year) |
| `ebit_fy` | float/int | EBIT (fiscal year) |
| `net_margin_fy` | float | Net margin (%) |
| `operating_margin_fy` | float | Operating margin (%) |
| `debt_to_equity_fy` | float | Debt-to-equity ratio |
| `return_on_equity_fy` | float | ROE (%) |
| `return_on_assets_fy` | float | ROA (%) |
| `total_assets_fy` | float/int | Total assets |
| `total_liabilities_fy` | float/int | Total liabilities |
| `total_equity_fy` | float/int | Shareholders' equity |
| `free_cash_flow_fy` | float/int | FCF (fiscal year) |
| `cash_f_operating_activities_fy` | float/int | Operating cash flow |
| `dividend_payout_ratio_fy` | float | Dividend payout ratio (%) |

### Trailing Twelve Months (TTM) — No `_h` suffix

| Field | Type | Description |
|-------|------|-------------|
| `earnings_per_share_basic_ttm` | float | EPS (trailing 12 months, basic) |
| `earnings_per_share_diluted_ttm` | float | EPS (TTM, diluted) |
| `earnings_per_share_ttm` | float | EPS TTM (generic) |
| `net_income_ttm` | float/int | Net income TTM |
| `total_revenue_ttm` | float/int | Revenue TTM |
| `ebitda_ttm` | float/int | EBITDA TTM |
| `ebit_ttm` | float/int | EBIT TTM |
| `operating_cash_flow_ttm` | float/int | Operating cash flow TTM |
| `free_cash_flow_ttm` | float/int | Free cash flow TTM |
| `pre_tax_margin_ttm` | float | Pre-tax margin (%) |
| `operating_margin_ttm` | float | Operating margin (%) |
| `ebitda_margin_ttm` | float | EBITDA margin (%) |
| `price_earnings_ttm` | float | P/E ratio (TTM) |
| `price_free_cash_flow_ttm` | float | Price-to-FCF ratio |
| `dividend_yield_ttm` | float | Dividend yield (TTM, %) |

### Current/Real-time Snapshot

| Field | Type | Description |
|-------|------|-------------|
| `price_earnings` | float | P/E ratio (current price vs. latest annual EPS) |
| `price_earnings_current` | float | P/E (real-time, current earnings) |
| `price_book_current` | float | P/B ratio (current) |
| `price_cash_flow_current` | float | Price-to-cash-flow (current) |
| `price_sales_fy` | float | P/S ratio (fiscal year) |
| `price_revenue_ttm` | float | Price-to-revenue (TTM) |
| `price_free_cash_flow_current` | float | Price-to-FCF (current) |
| `dividend_yield_fy` | float | Dividend yield (fiscal year, %) |
| `beta_1_year` | float | Beta (1-year) |
| `beta_5_year` | float | Beta (5-year) |
| `return_on_equity_current` | float | ROE (current) |
| `return_on_assets_current` | float | ROA (current) |
| `return_on_invested_capital_current` | float | ROIC (current) |
| `debt_to_equity_current` | float | D/E ratio (current) |
| `debt_to_asset_current` | float | Debt-to-assets (current) |

---

## 7. Per-Share Metrics (Current Snapshot)

| Field | Type | Description |
|-------|------|-------------|
| `book_value_per_share_current` | float | Book value per share |
| `book_tangible_per_share_current` | float | Tangible book value per share |
| `cash_per_share_current` | float | Cash per share |
| `cash_per_share_fy` | float | Cash per share (fiscal year end) |
| `dps_common_stock_prim_issue_fq` | float | Dividends per share (FQ) |
| `dps_common_stock_prim_issue_fy` | float | Dividends per share (FY) |
| `revenue_per_share_current` | float | Revenue per share (current) |
| `revenue_per_share_fy` | float | Revenue per share (fiscal year) |
| `ebit_per_share_current` | float | EBIT per share |
| `ebitda_per_share_fq_h` | float | EBITDA per share (note: suffix is `_h` but treated as scalar) |
| `free_cash_flow_per_share_current` | float | FCF per share (current) |
| `free_cash_flow_per_share_fy` | float | FCF per share (FY) |
| `operating_cash_flow_per_share` | float | Operating cash flow per share |
| `total_debt_per_share_current` | float | Total debt per share |
| `total_debt_per_employee_fy` | float | Debt per employee |
| `capex_per_share_current` | float | Capital expenditures per share |

---

## 8. Dividend & Payment Information (Upcoming & Recent)

| Field | Type | Description | Format |
|-------|------|-------------|--------|
| `dividends_yield` | float | Current dividend yield (%) | Percent |
| `dividends_availability` | int | Dividend data availability flag | 0=none, 1=available |
| `dividend_amount_upcoming` | float | Next dividend payment amount | Currency |
| `dividend_amount_recent` | float | Most recent dividend paid | Currency |
| `dividend_payout_ratio_percent_fq` | float | Payout ratio (%) | Percent |
| `dividend_payment_date_upcoming` | int | Next payment date | Unix timestamp |
| `dividend_ex_date_h` | array | Ex-dividend dates (historical) | [Unix timestamps] |
| `payment_date_recent` | int | Most recent payment date | Unix timestamp |
| `ex_date_recent` | int | Most recent ex-dividend date | Unix timestamp |
| `amount_upcoming` | float | Amount of upcoming dividend | Currency |
| `dividends_payable_fy` | float/int | Total dividends payable (fiscal year) | Currency |
| `dividends_paid` | float/int | Dividends paid out | Currency |
| `common_dividends_cash_flow_fy` | float/int | Dividend cash outflow | Currency |

---

## 9. Earnings Information (Upcoming & Recent)

| Field | Type | Description | Format |
|-------|------|-------------|--------|
| `earnings_availability` | int | Earnings data available (flag) | 0=no, 1=yes |
| `earnings_release_date` | int | Most recent earnings release date | Unix timestamp |
| `earnings_release_calendar_date` | str | Formatted release date | "YYYY-MM-DD" |
| `earnings_release_time` | int | Release time (seconds since midnight UTC) | 0-86400 |
| `earnings_release_next_date` | int | Next earnings release date | Unix timestamp |
| `earnings_release_next_date_fq` | int | Next FQ earnings date | Unix timestamp |
| `earnings_release_next_calendar_date_fq` | str | Formatted next FQ date | "YYYY-MM-DD" |
| `earnings_release_next_time` | int | Next release time | Seconds since midnight |
| `earnings_release_trading_date_fy` | int | Earnings trading date (FY) | Unix timestamp |
| `earnings_release_next_trading_date_fy` | int | Next earnings trading date | Unix timestamp |
| `earnings_per_share_forecast_next_fy` | float | Forecasted EPS for next FY | Currency |
| `earnings_per_share_forecast_next_fq` | float | Forecasted EPS for next FQ | Currency |
| `earnings_per_share_forecast_next_fh` | float | Forecasted EPS for next FH | Currency |
| `earnings_per_share_forecast_fq` | float | General EPS forecast (FQ) | Currency |
| `earnings_per_share_forecast_fy` | float | General EPS forecast (FY) | Currency |
| `earnings_publication_type_fq_h` | array | Publication type history (array, but indexed) | ["reported", "estimated"] |

**Earnings Forecast Fields (Advanced):**
| Field | Type | Description |
|-------|------|-------------|
| `revenue_estimate_ntm` | float | Revenue estimate (next twelve months) |
| `eps_estimate_ntm` | float | EPS estimate (next twelve months) |
| `last_annual_eps` | float | Most recent annual EPS |
| `revenue_forecast_fq_h` | array | Forecasted revenue by quarter |

---

## 10. Trading Configuration & Session Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `exchange` | str | Primary trading exchange | `NASDAQ` |
| `listed_exchange` | str | Official listing exchange | `NASDAQ` |
| `subsession_id` | str | Current subsession (trading mode) | `regular`, `pre`, `post` |
| `current_session` | str | Current session status | `regular`, `premarket`, `postmarket`, `out_of_session` |
| `session-display` | str | Display name for session | "Regular" |
| `timezone` | str | Market timezone | `America/New_York` |
| `open_time` | int | Session open time (seconds since midnight) | e.g., 34200 (9:30 AM) |
| `regular_close_time` | int | Regular close time | e.g., 57600 (4:00 PM) |
| `minmov` / `minmove2` | int | Minimum price movement (tick size) | e.g., 1 (stocks) |
| `variable_tick_size` | str | Variable tick size rule | e.g., `"0.0001 1 0.01"` |
| `pricescale` | int | Divisor for integer prices | e.g., 10000 (= 4 decimal places) |
| `pointvalue` | float | Value per point (futures) | e.g., 100.0 |
| `fractional` | bool | Whether fractional shares supported | true/false |
| `is_tradable` | bool | Whether instrument is currently tradable | true/false |
| `pro_perm` | str | Permission level / tier | e.g., `"nasdaq"` |
| `pro_name` | str | Permissioning name | e.g., `"Nasdaq"` |

**Session Metadata:**
| Field | Type | Description |
|-------|------|-------------|
| `session-regular` | object | Regular session hours object |
| `session-premarket` | object | Pre-market hours object |
| `session-extended` | object | Extended (after-hours) object |
| `session-holidays` | array | Holiday dates (array of Unix timestamps) |
| `session_holidays` | object | Detailed holiday information |
| `has-adjustment` | bool | Whether data adjusted for splits/dividends |
| `allowed_adjustment` | str | Adjustment types permitted |
| `kind-delay` | int | Data delay (seconds) |
| `rt-lag` | int | Real-time data lag (milliseconds) |

---

## 11. Market Data Availability & Flags

| Field | Type | Description |
|-------|------|-------------|
| `trade_loaded` | bool | Whether trade/quote data loaded |
| `metrics_loaded` | bool | Whether fundamental metrics loaded |
| `hub_rt_loaded` | bool | Whether hub real-time data loaded |
| `financials_availability` | int | Financial data availability flag |
| `has_ipo_data` | bool | IPO data available |
| `has_ipo_details_visible` | bool | IPO details visible to user |
| `has_etf_ownership` | bool | ETF composition available |
| `has-no-volume` | bool | Symbol has no volume (indices) |
| `has-depth` | bool | Depth of market available |
| `has-adjustment` | bool | Adjustment data available |
| `feed-has-dwm` | bool | Daily/weekly/monthly bars available |
| `update_mode` | str | Data update mode | `"1"` (real-time), `"D"` (delayed) |
| `visible-plots-set` | str | Visible plots/indicators | `"ohlcv"` |

---

## 12. System & UI Metadata

| Field | Type | Description |
|-------|------|-------------|
| `popularity` | float | Popularity score (0-5 or similar) |
| `popularity_rank` | int | Popularity rank within market |
| `local_popularity` | object | Regional popularity (country → score) |
| `local_popularity_rank` | object | Regional popularity rank (country → rank) |
| `recommendation_mark` | float | Consensus recommendation | 1=strong sell, 5=strong buy |
| `recommendation_buy` | int | Number of buy recommendations |
| `recommendation_sell` | int | Number of sell recommendations |
| `recommendation_under` | int | Number of underperform ratings |
| `recommendation_over` | int | Number of outperform ratings |
| `price_target_average` | float | Average price target |
| `price_target_high` | float | Highest analyst price target |
| `price_target_average_prev` | float | Previous average price target |
| `price_target_up_num` | int | Count of raised targets (last 30d) |
| `price_target_down_num` | int | Count of lowered targets (last 30d) |
| `price_target_estimates_num` | int | Total number of price target estimates |
| `language` | str | Content language | `"en"` |
| `logo` | object | Logo metadata (id, style, url) |
| `logoid` | str | Logo identifier |
| `currency-logoid` | str | Currency logo identifier |

---

## 13. IPO & Corporate Actions

| Field | Type | Description | Format |
|-------|------|-------------|--------|
| `ipo_offer_date` | int | IPO offer date | Unix timestamp |
| `split_last_date` | int | Most recent stock split date | Unix timestamp |
| `days_to_maturity` | int | Days until maturity (bonds) | Integer |
| `fund_view_mode` | str | Fund view mode | e.g., `"base"` |
| `fund_view_modes` | str | Available fund view modes | Comma-separated |

---

## 14. Rating & Outlook (S&P, etc.)

| Field | Type | Description |
|-------|------|-------------|
| `issuer_snp_rating_st` | str | S&P short-term credit rating | `"A-1"`, `"A-2"`, `"BBB"`, etc. |
| `issuer_snp_rating_st_h` | array | S&P ST rating history (array of objects with `date`, `rating`, `outlook`) |
| `issuer_snp_rating_lt_h` | array | S&P long-term rating history |

---

## 15. Nested Objects & Complex Fields

### `broker_names` / `broker-names`
**Type:** Object (key-value mapping)  
**Structure:** `{ "broker_code": "internal_symbol", ... }`  
**Example:**
```json
{
  "alpaca": "KLAC",
  "ibkr": "270957",
  "saxobank": "KLAC:xnas",
  "moomoo": "US:KLAC"
}
```
**Usage:** Map TradingView symbols to broker-specific identifiers for order placement

---

### `rates_ttm`, `rates_fy`, `rates_mc`, `rates_current`
**Type:** Object (currency conversion rates)  
**Structure:** `{ "base_currency": rate_object, ... }`  
**Example:** Foreign exchange rates for multi-currency valuation  
**Usage:** Convert foreign financials to USD or other base currency

---

### `rates_earnings_fq`, `rates_earnings_fy`, `rates_earnings_next_fy`
**Type:** Object  
**Purpose:** Earnings-specific rate conversions  
**Usage:** Normalize earnings across different currencies/periods

---

### `options-info`
**Type:** Object  
**Structure:**
```json
{
  "families": [
    {
      "description": "AMERICAN OPTIONS",
      "exercise": "american",
      "name": "KLAC",
      "prefix": "OPRA",
      "series": [
        {
          "exp": 20260618,
          "id": "NASDAQ:KLAC;KLAC;20260618",
          "lotSize": 100,
          "root": "KLAC",
          "strikes": [290, 300, 310, ...]
        }
      ]
    }
  ]
}
```
**Depth:** 4–5 levels nested  
**Usage:** Options chain metadata (expiries, strike prices, exercise type)

---

### `figi`
**Type:** Object or string  
**Structure:** If object: `{ "SHARE_CLASS_FIGI": "...", "SECURITY_ID": "..." }`  
**Usage:** Financial Instrument Global Identifier for regulatory/data reference

---

### `logo`
**Type:** Object  
**Structure:** `{ "id": "...", "style": "...", "url": "..." }`  
**Usage:** Company logo reference for UI display

---

### `source2`
**Type:** Object  
**Content:** Provider/exchange metadata (name, id, url, country, description)

---

### `subsessions`
**Type:** Object  
**Content:** Detailed subsession rules (pre-market, regular, after-hours)

---

## 16. Per-Share Current Metrics (Bonus)

| Field | Type | Description |
|-------|------|-------------|
| `operating_cash_flow_per_share_current` | float | OCF per share |
| `operating_cash_flow_per_share_fy` | float | OCF per share (fiscal year) |
| `revenue_per_employee_fy` | float | Revenue per employee |
| `free_cash_flow_per_employee_fy` | float | FCF per employee |
| `net_income_per_employee_fy` | float | Net income per employee |
| `working_capital_per_share_fy` | float | Working capital per share |
| `working_capital_per_share_current` | float | Working capital per share (current) |

---

## 17. Balance Sheet Snapshot (Current Period)

Single-value (non-array) balance sheet fields for the most recent period:

| Field | Type | Description |
|-------|------|-------------|
| `total_assets` | float/int | Total assets (latest) |
| `total_assets_fq` | float/int | Total assets (latest FQ) |
| `total_current_assets` | float/int | Current assets |
| `total_current_assets_fq` | float/int | Current assets (FQ) |
| `total_current_liabilities_fq` | float/int | Current liabilities (FQ) |
| `total_non_current_liabilities_fq` | float/int | Non-current liabilities (FQ) |
| `total_liabilities` | float/int | Total liabilities |
| `total_liabilities_fq` | float/int | Total liabilities (FQ) |
| `total_equity_fq` | float/int | Shareholders' equity (FQ) |
| `total_equity_fy` | float/int | Shareholders' equity (FY) |
| `common_equity_total_fy` | float/int | Common equity (FY) |
| `goodwill_fq` | float/int | Goodwill (FQ) |
| `goodwill_fy` | float/int | Goodwill (FY) |
| `total_inventory_fq` | float/int | Total inventory (FQ) |
| `total_inventory_fy` | float/int | Total inventory (FY) |
| `cash_n_equivalents_fq` | float/int | Cash & equivalents (FQ) |
| `total_debt_fy` | float/int | Total debt (FY) |
| `short_term_debt_fq` | float/int | Short-term debt (FQ) |
| `long_term_debt_fy` | float/int | Long-term debt (FY) |
| `accounts_payable_fq` | float/int | Accounts payable (FQ) |
| `accounts_payable_fy` | float/int | Accounts payable (FY) |
| `paid_in_capital_fq` | float/int | Paid-in capital (FQ) |
| `paid_in_capital_fy` | float/int | Paid-in capital (FY) |
| `retained_earnings_fq` | float/int | Retained earnings (FQ) |
| `retained_earnings_fy` | float/int | Retained earnings (FY) |

---

## 18. Cash Flow Snapshot (Current Period)

| Field | Type | Description |
|-------|------|-------------|
| `cash_f_operating_activities_fy` | float/int | Operating cash flow (FY) |
| `cash_f_operating_activities_fq` | float/int | Operating cash flow (FQ) |
| `cash_f_financing_activities_fq` | float/int | Financing cash flow (FQ) |
| `cash_f_financing_activities_fy` | float/int | Financing cash flow (FY) |
| `capital_expenditures_fq` | float/int | Capex (FQ) |
| `capital_expenditures_fy` | float/int | Capex (FY) |

---

## 19. Index/Ratio Snapshots (Current, No History)

| Field | Type | Description |
|-------|------|-------------|
| `current_ratio_fq` | float | Current ratio (FQ) |
| `quick_ratio_fq` | float | Quick ratio (FQ) |
| `debt_to_asset_fq` | float | D/A ratio (FQ) |
| `return_on_invested_capital_fq` | float | ROIC (FQ) |
| `ncavps_ratio_fq` | float | Net current asset per share (FQ) |
| `tobin_q_ratio_fq` | float | Tobin's Q ratio (FQ) |
| `altman_z_score_ttm` | float | Altman Z-score (TTM) |
| `graham_numbers_fy` | float | Graham number (FY) |
| `graham_numbers_ttm` | float | Graham number (TTM) |
| `sloan_ratio_ttm` | float | Sloan ratio (TTM) |
| `zmijewski_score_fy` | float | Zmijewski score (FY) |
| `piotroski_f_score_fy` | float | Piotroski F-score (FY) |
| `asset_turnover_fy` | float | Asset turnover (FY) |
| `receivables_turnover_fy` | float | Receivables turnover (FY) |
| `inventory_turnover_fy` | float | Inventory turnover (FY) |
| `fixed_assets_turnover_fy` | float | Fixed asset turnover (FY) |

---

## Naming Conventions

### Suffix Conventions for Scalars

| Suffix | Meaning | Example |
|--------|---------|---------|
| *(no suffix)* | Current/latest real-time value | `lp`, `bid`, `ask` |
| `_current` | Current snapshot (alternative naming) | `price_earnings_current`, `return_on_equity_current` |
| `_fq` | Latest fiscal quarter (single value, not array) | `earnings_per_share_fq`, `net_income_fq` |
| `_fy` | Latest fiscal year (single value) | `earnings_per_share_fy`, `net_income_fy` |
| `_ttm` | Trailing twelve months (single value) | `earnings_per_share_ttm`, `ebitda_ttm` |
| `_fh` | Fiscal half-year | `dps_common_stock_prim_issue_fh` |
| `_mc` | Market cap aggregated | `rates_mc` |
| `_next_` | Forward-looking, next period | `earnings_per_share_forecast_next_fy` |
| `_upcoming` | Upcoming/future event | `dividend_payment_date_upcoming`, `amount_upcoming` |
| `_recent` | Most recent past event | `dividend_amount_recent`, `payment_date_recent` |

**Note:** Fields with `_h` suffix are **arrays (timeseries)** and belong in the complementary timeseries reference, not here.

---

## Data Type Mappings

| Type | Python Type | JSON Type | Range/Notes |
|------|------------|-----------|------------|
| float | `float` | `number` | Prices, ratios, percentages |
| int/float | `int` or `float` | `number` | Financial amounts, shares, timestamps |
| bool | `bool` | `boolean` | Flags, availability |
| str | `str` | `string` | Symbols, currency codes, descriptions |
| int (epoch) | `int` | `number` | Timestamps (Unix seconds) |
| object | `dict` | `object` | Nested metadata |
| array | `list` | `array` | **Use timeseries reference** |

---

## Common Field Groupings

### For Real-time Quote Monitoring
`lp`, `bid`, `ask`, `bid_size`, `ask_size`, `volume`, `ch`, `chp`, `prev_close_price`

### For Valuation Analysis
`price_earnings`, `price_book_current`, `price_sales_fy`, `market_cap_basic`, `enterprise_value_current`, `beta_1_year`

### For Fundamental Screening
`total_revenue_fy`, `net_income_fy`, `free_cash_flow_fy`, `return_on_equity_fy`, `debt_to_equity_current`, `dividend_yield`

### For Company Research
`sector`, `industry`, `founded`, `number_of_employees`, `ceo`, `web_site_url`, `business_description`, `country_code`

### For Risk Assessment
`market_cap_basic`, `beta_1_year`, `debt_to_equity_fy`, `current_ratio_fq`, `altman_z_score_ttm`, `price_52_week_high`

### For Dividend Income
`dividend_yield`, `dps_common_stock_prim_issue_fy`, `dividend_payout_ratio_fy`, `common_dividends_cash_flow_fy`

---

## Integration Notes

**Related Documentation:**
- **Timeseries Arrays:** See `TIMESERIES_NOMENCLATURE_REFERENCE.md` (for `_h` suffix fields and historical data)
- **Pattern Families:** See `TIMESERIES_PATTERNS_DETAILED.md` (for array structure analysis)
- **Field Glossary:** See `variables_definitions.md` (for brief descriptions of all fields)

**Null/Missing Data Handling:**
- Most financial snapshots may be `null` for small-cap stocks, ADRs, or non-US companies
- Divide by zero: Always check `total_shares_outstanding > 0` before computing per-share metrics
- Currency conversion: Check `currency_code` before using raw financial values

**Data Freshness:**
- Real-time fields (`lp`, `bid`, `ask`, `volume`): Updated in real-time during market hours
- Snapshot metrics (`_fq`, `_fy`): Updated at earnings/filing (quarterly/annually)
- TTM values: Updated continuously with each new bar
- Consensus ratings: Updated as analyst ratings change

---

**Document Version:** 2026-05-17  
**Applicable to:** tvdatafeed v2.0.1, TradingView WebSocket v1  
**Generated from:** KLAC_NASDAQ.json analysis + variables_extraction_summary.json
