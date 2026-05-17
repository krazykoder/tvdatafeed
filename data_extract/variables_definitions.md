# Variables extraction — metrics & timeseries definitions

Generated: 2026-05-17

**Metrics & Parameters**
- `trade_loaded`: boolean — indicates whether trade/quote data was successfully loaded for the symbol.
- `ask`: float — current best ask price.
- `bid`: float — current best bid price.
- `ask_size`: float|int — size/quantity available at the ask price.
- `bid_size`: float|int — size/quantity available at the bid price.
- `lp`: float — last traded (last price) for the symbol.
- `lp_time`: int (epoch seconds) — timestamp of the last trade (use `lp_time` when present).
- `lp_ms` / `t_ms`: int (milliseconds) — millisecond-resolution timestamp for message/frame.
- `t` / `timestamp`: int (epoch seconds) — frame-level timestamp.
- `ch`: float — absolute change in price (usually `lp - prev_close`).
- `chp`: float — percent change in price relative to previous close.
- `volume`: int — cumulative trade volume (usually for the current session/day).
- `price_52_week_high` / `price_52_week_low`: float — 52-week high/low prices.
- `open_price` / `high_price` / `low_price` / `regular_close`: float — common price-level metadata.
- `market_cap_calc` / `market_cap_basic`: float/int — market capitalization estimates.
- `enterprise_value_current`: float/int — current enterprise value estimate.
- `currency_code` / `currency_id`: str — trading currency (e.g., "USD").
- `is_tradable`: bool — whether the symbol is tradable on the exchange.
- `pricescale`: int — divisor to apply to integer price fields: true_price = raw / `pricescale`.
- `minmov` / `minmove2`: int — minimum price movement increment (tick size metadata).
- `pointvalue`: float — multiplier for contract/point value (futures/derivatives).
- `visible-plots-set` / `visible_plots_set`: str — which plots are visible (e.g., `ohlcv`).
- `has_adjustment` / `allowed_adjustment`: bool/str — whether historical adjustments (splits/dividends) are available and allowed types.
- `earnings_per_share_basic_ttm`, `earnings_per_share_fq`: float — EPS (trailing twelve months / most recent fiscal quarter).
- `dividends_yield` / `dividends_availability`: float/int — dividend yield and availability flag.
- `total_revenue`, `net_income`, `ebit`, `ebitda`: numeric — corporate financial aggregates.
- `first_bar_time_1d`, `first_bar_time_1m`, `first_bar_time_1s`: int — earliest bar timestamp available for different resolutions.
- `session-display` / `session` / `subsessions`: session trading hours metadata.

**Nested objects (examples)**
- `source2`: object — provider/exchange metadata (name, id, url, country, description).
- `logo`: object — logo metadata (id, style, url).
- `rates_ttm`, `rates_fy`, `rates_mc`: object — currency / rate conversion info.

**Timeseries datasets — time variable + data variables**
General note: TradingView messages provide both frame-level timestamps and bar-level timestamps. Bars are typically arrays where the first element is the timestamp and remaining elements are price/volume fields.

- Time fields (common)
  - `t` : int — frame message time (seconds since epoch).
  - `t_ms`: int — frame message time in milliseconds.
  - `lp_time`: int — last trade time (seconds since epoch).
  - Bar timestamp: `bar[0]` — epoch seconds for that bar (use `t_ms` or `bar[0] * 1000` if millisecond precision required).

- Typical OHLCV bar format (per-bar array):
  - `bar[0]` — timestamp (epoch seconds)
  - `bar[1]` — open price
  - `bar[2]` — high price
  - `bar[3]` — low price
  - `bar[4]` — close price
  - `bar[5]` — volume

  (Note: some series omit fields or use slightly different ordering; always validate with the `series_loading`/`series_completed` messages and `visible_plots_set`.)

- Data variables commonly found in timeseries messages
  - `open` / `o` — open price for the bar (may be in-array or named in some JSON variants).
  - `high` / `h` — high price for the bar.
  - `low` / `l` — low price for the bar.
  - `close` / `c` — close price for the bar.
  - `volume` / `v` — trade volume for the bar.
  - `trade_count` / `n` — number of trades (rare / optional).

**Scaling and interpretation rules**
- When `pricescale` is present, integer price fields must be divided by `pricescale` to get human-readable prices. Example: actual_price = raw_price / pricescale.
- Timestamps are typically in seconds; prefer `t_ms` when available for millisecond accuracy.
- `lp` and `lp_time` provide a convenient single-point last-trade price/time if full bars are not present.

**Suggested minimum extraction list**
- Scalar metrics: `lp`, `lp_time`, `bid`, `ask`, `bid_size`, `ask_size`, `volume`, `ch`, `chp`, `market_cap_calc`, `market_cap_basic`, `currency_code`, `is_tradable`, `pricescale`.
- Timeseries fields to extract per-bar: `timestamp` (bar[0]), `open`, `high`, `low`, `close`, `volume`.

If you want, I can also generate a machine-readable JSON mapping (field → definition) or expand this to include every field found in `debug/variables_extraction_summary.json`.
