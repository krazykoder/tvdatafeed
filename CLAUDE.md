# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**tvdatafeed** is a Python library for downloading historical market data (OHLCV, financials, earnings, dividends) from TradingView via WebSocket. Version 2.0.0 is a complete rewrite — no Selenium, WebSocket-based only. Not backward compatible with v1.x.

## Installation & Setup

```bash
# From source
pip install -r requirements.txt
python setup.py install

# From GitHub
pip install --upgrade --no-cache-dir git+https://github.com/krazykoder/tvdatafeed.git
```

## Running & Testing

There is no formal test suite. Use these for validation:

```bash
# Validate raw WebSocket data parsing (reads .ws files in debug/)
python debug/test_parser.py

# Download fresh raw WebSocket samples for AAPL/AMD/etc.
python debug/download_raw_data.py

# Interactive examples (Jupyter)
jupyter notebook tv.ipynb
```

## Architecture

### Core Module: `tvDatafeed/main.py`

Single class `tvData` handles everything:

1. **Authentication** (`__auth`) — POSTs to TradingView signin, extracts JWT. Supports direct token via `directToken=` param. Falls back to `"unauthorized_user_token"` for anonymous use.

2. **WebSocket protocol** — Connects to `wss://data.tradingview.com/socket.io/websocket`. Messages use `~m~{length}~m~{json}` framing. Key send sequence: `set_auth_token` → `chart_create_session` / `quote_create_session` → `resolve_symbol` → `create_series` / `create_study`.

3. **Public data methods:**
   - `get_timeseries(symbol, exchange, interval, n_bars, ...)` → `pd.DataFrame` (OHLCV, datetime index)
   - `get_financials(symbol, exchange, ...)` → `(4 DataFrames, financial_dict)` — 1000+ fields
   - `get_timeseries_earnings_dividends(...)` → `(ohlcv_df, earnings_df, dividends_df)`

4. **Parsing** — Raw WebSocket text is parsed with regex + JSON. Key patterns:
   - Time series: regex `"s":\[(.+?)\}\]` on raw response
   - Earnings/dividends: strip escape chars, replace `~m~...~m~` headers with commas, parse as JSON array, extract from `item['p'][1]['sds_1']`, `['st1']`, `['st2']`
   - Financials: regex extraction of `revenues_fq_h`, `earnings_fq_h`, etc.

### Symbol Formatting

`__format_symbol(symbol, exchange, contract)`:
- Pass `"EXCHANGE:SYMBOL"` directly (skips formatting)
- Cash: `"EXCHANGE:SYMBOL"`
- Futures: `"EXCHANGE:SYMBOL{n}!"` (e.g. `"NSE:NIFTY1!"`)
- Pass empty string `''` for exchange to use TradingView's default

### `Interval` Enum

Values: `in_1_minute` through `in_monthly`. Maps to TradingView strings (`"1"`, `"1H"`, `"1D"`, etc.).

## Key Files

| File | Purpose |
|---|---|
| `tvDatafeed/main.py` | All logic — auth, WebSocket, parsing, public API |
| `tvDatafeed/__init__.py` | Exports `tvData`, `Interval` |
| `tvDatafeed/fields.md` | Full list of 1000+ financial field keys |
| `debug/test_parser.py` | Parser validation against saved `.ws` files |
| `debug/download_raw_data.py` | Saves live WebSocket responses as `.ws` files |
| `debug/*.ws` | Raw WebSocket samples (AAPL, AMD, AVGO, KLAC, MU) |
| `fiddle_socket.py` / `tv.ipynb` | Usage examples and manual testing |

## Common Pitfalls

- **Indices (e.g. IXIC) have no volume** — the parser handles this with a fallback; preserve that logic when modifying `__create_timeseries_df`.
- **WebSocket timeout is 5s** — `ws_timeout` attribute; increase if getting incomplete data on slow connections.
- **Max 5000 bars per request** — TradingView server limit for `get_timeseries`; `n_bars` above this is silently capped.
- **Regex parsing is fragile** — changes to TradingView's response format will break parsing. The `debug/` tools exist specifically to diagnose this.
