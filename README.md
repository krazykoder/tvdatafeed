# **TvDatafeed**
### Updated 08/07/2024 by `krazykoder` from [fork-tvdatafeed](https://github.com/stefanomorni/fork-tvdatafeed)

A simple TradingView historical Data Downloader. Tvdatafeed allows downloading upto 5000 bars on any of the supported timeframe.

## Installation

This module is installed via pip:

Installing from github repo

```sh
pip install --upgrade --no-cache-dir git+https://github.com/krazykoder/tvdatafeed.git
```

---

## About release 2.0.0

Version 2.0.0 is a major release and is not backward compatible. make sure you update your code accordingly. Thanks to [stefanomorni](https://github.com/stefanomorni) for contributing and removing selenium dependancy.

## Usage

Import the packages and initialize with your tradingview username and password.

```python
from tvDatafeed import TvDatafeed, Interval

username = 'YourTradingViewUsername'
password = 'YourTradingViewPassword'

tv = TvDatafeed(username, password)
```

You may use without logging in, but in some cases tradingview may limit the symbols and some symbols might not be available.

To use it without logging in

```python
tv = TvDatafeed()
```

when using without login, following warning will be shown `you are using nologin method, data you access may be limited`

---

## Getting Data

To download the data use `tv.get_hist` method.

It accepts following arguments and returns pandas dataframe

```python
(symbol: str, exchange: str = 'NSE', interval: Interval = Interval.in_daily, n_bars: int = 10, fut_contract: int | None = None, extended_session: bool = False) -> DataFrame)
```

for example-

```python

# indices - leave exchange '' blank
tv.get_hist('NDQ','', interval=Interval.in_daily,n_bars=5000) # Nasdaq index 
tv.get_hist('DJI','', interval=Interval.in_daily,n_bars=10000) # DOW index
tv.get_hist('DJA','', interval=Interval.in_daily,n_bars=5000) # DOW AVERAGE
tv.get_hist('SPX','', interval=Interval.in_daily,n_bars=5000) # SPY index
tv.get_hist('SPY','', interval=Interval.in_daily,n_bars=5000) # etf fund 
tv.get_hist('VOO','', interval=Interval.in_daily,n_bars=5000) 
tv.get_hist('TQQQ','', interval=Interval.in_daily,n_bars=10000)
tv.get_hist('GLD','', interval=Interval.in_daily,n_bars=10000) # GOLD 

# ETF, EQUITY, STOCKS
tv.get_hist('SPY','AMEX', interval=Interval.in_daily,n_bars=5000)
tv.get_hist('SPXL','AMEX', interval=Interval.in_daily,n_bars=5000)
tv.get_hist(symbol='AMD',exchange='NASDAQ',interval=Interval.in_daily,n_bars=10000)
tv.get_hist(symbol='QQQ',exchange='NASDAQ',interval=Interval.in_1_hour,n_bars=10000)
tv.get_hist(symbol='QQQ',exchange='NASDAQ',interval=Interval.in_30_minute,n_bars=10000)

# FUTURES - leave exchange '' blank for US futures 
tv.get_hist(symbol='ES1!',exchange='',interval=Interval.in_1_hour,n_bars=1000) #SPY FUTURE
tv.get_hist(symbol='ES2!',exchange='',interval=Interval.in_1_hour,n_bars=1000) #SPY FUTURE
tv.get_hist(symbol='USOIL',exchange='',interval=Interval.in_daily,n_bars=1000) #USOIL FUTURE

tv.get_hist(symbol='NIFTY',exchange='NSE',interval=Interval.in_1_hour,n_bars=1000,fut_contract=1)

# crudeoil
crudeoil_data = tv.get_hist(symbol='CRUDEOIL',exchange='MCX',interval=Interval.in_1_hour,n_bars=5000,fut_contract=1)

# extended market hours
tv.get_hist(symbol="SPY",exchange="AMEX",interval=Interval.in_1_hour,n_bars=500, extended_session=True)
tv.get_hist(symbol="NDQ",exchange="",interval=Interval.in_1_hour,n_bars=500, extended_session=True)

```

---
## Supported Time Intervals

Following timeframes intervals are supported-

`Interval.in_1_minute`
`Interval.in_3_minute`
`Interval.in_5_minute`
`Interval.in_15_minute`
`Interval.in_30_minute`
`Interval.in_45_minute`
`Interval.in_1_hour`
`Interval.in_2_hour`
`Interval.in_3_hour`
`Interval.in_4_hour`
`Interval.in_daily`
`Interval.in_weekly`
`Interval.in_monthly`

---

