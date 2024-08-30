import datetime
import enum
import json
import logging
import os
import pickle
import random
import re
import shutil
import string
import time
import pandas as pd
from websocket import create_connection
import requests
import sys

logger = logging.getLogger(__name__)


class Interval(enum.Enum):
    in_1_minute = "1"
    in_3_minute = "3"
    in_5_minute = "5"
    in_15_minute = "15"
    in_30_minute = "30"
    in_45_minute = "45"
    in_1_hour = "1H"
    in_2_hour = "2H"
    in_3_hour = "3H"
    in_4_hour = "4H"
    in_daily = "1D"
    in_weekly = "1W"
    in_monthly = "1M"


class tvData:
    sign_in_url = "https://www.tradingview.com/accounts/signin/"
    ws_headers = json.dumps(
        {
            "Origin": "https://data.tradingview.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        }
    )
    signin_headers = {"Referer": "https://www.tradingview.com"}
    ws_timeout = 5

    def __init__(
        self,
        username: str = None,
        password: str = None,
        directToken: str = None
    ) -> None:
        """Create tvData object

        Args:
            username (str, optional): tradingview username. Defaults to None.
            password (str, optional): tradingview password. Defaults to None.
        """

        self.ws_debug = False
        if directToken is None:
            self.token = self.__auth(username, password)
        else: 
            self.token = directToken
        print ("Token" , self.token, directToken)

        if self.token is None:
            self.token = "unauthorized_user_token"
            logger.warning(
                "you are using nologin method, data you access may be limited"
            )

        self.ws = None
        self.session = self.__generate_session()
        self.chart_session = self.__generate_chart_session()
        # self.financials_session = self.__generate_chart_session()

    def __auth(self, username, password):

        if username is None or password is None:
            token = None

        else:
            data = {"username": username, "password": password, "remember": "off"}
            try:
                response = requests.post(
                    url=self.sign_in_url, data=data, headers=self.signin_headers
                )
                print (response.json())
                token = response.json()["user"]["auth_token"]
            except Exception as e:

                logger.error("error while signin")
                token = None

        return token

    def __create_connection(self):
        logging.debug("creating websocket connection")
        self.ws = create_connection(
            "wss://data.tradingview.com/socket.io/websocket",
            headers=self.ws_headers,
            timeout=self.ws_timeout,
        )

    @staticmethod
    def __filter_raw_message(text):
        try:
            found = re.search('"m":"(.+?)",', text).group(1)
            found2 = re.search('"p":(.+?"}"])}', text).group(1)

            return found, found2
        except AttributeError:
            logger.error("error in filter_raw_message")

    @staticmethod
    def __generate_session():
        stringLength = 12
        letters = string.ascii_lowercase
        random_string = "".join(random.choice(letters) for i in range(stringLength))
        return "qs_" + random_string

    @staticmethod
    def __generate_chart_session():
        stringLength = 12
        letters = string.ascii_lowercase
        random_string = "".join(random.choice(letters) for i in range(stringLength))
        return "cs_" + random_string

    @staticmethod
    def __prepend_header(st):
        return "~m~" + str(len(st)) + "~m~" + st

    @staticmethod
    def __construct_message(func, param_list):
        return json.dumps({"m": func, "p": param_list}, separators=(",", ":"))

    def __create_message(self, func, paramList):
        return self.__prepend_header(self.__construct_message(func, paramList))

    def __send_message(self, func, args):
        m = self.__create_message(func, args)
        if self.ws_debug:
            print(m)
        self.ws.send(m)

    @staticmethod
    def __create_timeseries_df(raw_data, symbol):
        """Returns pandas DF for timeseries
        cols =["datetime", "open", "high", "low", "close", "volume"]
        """
        try:
            out = re.search('"s":\[(.+?)\}\]', raw_data).group(1)
            x = out.split(',{"')
            data = list()
            volume_data = True

            for xi in x:
                xi = re.split("\[|:|,|\]", xi)
                ts = datetime.datetime.fromtimestamp(float(xi[4]))

                row = [ts]

                for i in range(5, 10):

                    # skip converting volume data if does not exists
                    if not volume_data and i == 9:
                        row.append(0.0)
                        continue
                    try:
                        row.append(float(xi[i]))

                    except ValueError:
                        volume_data = False
                        row.append(0.0)
                        logger.debug("no volume data")

                data.append(row)

            data = pd.DataFrame(
                data, columns=["datetime", "open", "high", "low", "close", "volume"]
            ).set_index("datetime")
            data.insert(0, "symbol", value=symbol)
            return data
        except AttributeError:
            logger.error("no data, please check the exchange and symbol")
    
    
    @staticmethod
    def __create_ohlcv_earnings_dividends (raw_data):
        """Extracts all together: timeseries, earnings dates, div dates """
        df = None
        e_df = None 
        d_df = None
        
        try:  
            # Format Raw data 
            raw_data = re.sub(r"\\\"", '', raw_data) # removes \" from string 
            raw_data = re.sub(r"\\", '', raw_data) # removes \ from string 
            raw_data = re.sub(r"~m~(.+?)~m~", ',', raw_data) #  ~m--m~ from string 
            raw_data = "["+raw_data[1:]+"]" # remove the first comma and append to a list [] 
            dataDict = json.loads(raw_data)

            # identify : timeseries, dividend series, earnings series 
            for item in dataDict : 
                try : ts = item ['p'][1]['sds_1']['s'] # ohlc array 
                except : pass 
                try: div = item['p'][1]['st2']["st"] # dividend array
                except : pass 
                try: ern = item ['p'][1]['st1']['st'] # earnings array 
                except: pass

            # Time series : ohlcv 
            t = list(map(lambda x : x['v'], ts))
            t_col = ["datetime", "open", "high", "low", "close", "volume"]
            df = pd.DataFrame(t, columns=t_col)
            df['datetime'] = pd.to_datetime(df['datetime'], unit='s')
            df = df.set_index('datetime')


            # Time series : earnings/ eps/ rev / dates  
            e = list(map(lambda x : x['v'], ern))
            t_col = ["datetime", "eps_std", "eps_est", "qy", "date", "eps_act", "rev_est_M", "rev_act_M", "sl"]
            e_df = pd.DataFrame(e, columns=t_col)
            e_df['datetime'] = pd.to_datetime(e_df['datetime'], unit='s')
            e_df['qy'] = pd.to_datetime(e_df['qy'], unit='s')
            e_df['date'] = pd.to_datetime(e_df['date'], unit='ms')
            e_df = e_df.set_index('datetime')
            # e_df.loc['2004']

            # Time series : dividend 
            d = list(map(lambda x : x['v'], div))
            t_col = ["xdate", "divamt", "ex_date", "dd", "pay_date" ]
            d_df = pd.DataFrame(d, columns=t_col)
            #  [1699626600.0, 0.239999995, 1699574400000.0, 1e+100, 1700092800000.0]
            d_df['xdate'] = pd.to_datetime(d_df['xdate'], unit='s')
            d_df['ex_date'] = pd.to_datetime(d_df['ex_date'], unit='ms')
            d_df['pay_date'] = pd.to_datetime(d_df['pay_date'], unit='ms')
            d_df = d_df.set_index('xdate')
            # d_df.loc['2015']
        
        except: 
            pass
        
        return df, e_df, d_df 

    
    
    @staticmethod
    def __create_earnings_df(raw_data):
        """Extracts Revenues and Earnings : FY and FQ"""
        try:
            out = re.search('"revenues_fq_h":\[(.+?)\]', raw_data).group(1)
            df_revenue_q = pd.read_json(out, lines=True)

            out = re.search('"earnings_fq_h":\[(.+?)\]', raw_data).group(1)
            df_earnings_q = pd.read_json(out, lines=True)

            out = re.search('"revenues_fy_h":\[(.+?)\]', raw_data).group(1)
            df_revenue_f = pd.read_json(out, lines=True)

            out = re.search('"earnings_fy_h":\[(.+?)\]', raw_data).group(1)
            df_earnings_f = pd.read_json(out, lines=True)

            return df_revenue_q, df_earnings_q, df_revenue_f, df_earnings_f
        except AttributeError:
            logger.error("no data, please check the exchange and symbol")

    @staticmethod
    def __create_financial_dict_full(raw_data):
        """Extracts all the financial data as dict"""
        try:
            raw_data = re.sub(r"\\\"", "", raw_data)  # removes \" from string
            raw_data = re.sub(r"\\", "", raw_data)  # removes \ from string
            raw_data = re.sub(r"~m~(.+?)~m~", ",", raw_data)  #  ~m--m~ from string
            # remove the first comma and append to a list []
            raw_data = "[" + raw_data[1:] + "]"
            dataDict = json.loads(raw_data)  # this is the dicts

            header = {}
            merged = {}
            for toplevelItem in dataDict:
                # print (item)
                # merged.update ( {k: v for k, v in item.items() if v})
                try:
                    merged = {
                        **merged,
                        **toplevelItem["p"][1]["v"],
                    }  # merge 2 dicts - will overwrite if same key
                except:
                    pass
                try:
                    header = {**header, **toplevelItem}
                except:
                    pass

            # len(header.keys()) , header.keys()  # count 11
            # len(merged.keys()) , merged.keys()  # count 1254
            # merged['short_name']  # AAPL

            # return {merged["short_name"]: merged}
            return merged

        except AttributeError:
            logger.error("no data, please check the exchange and symbol")

    @staticmethod
    def __format_symbol(symbol, exchange, contract: int = None):

        if ":" in symbol:
            pass
        elif contract is None:
            symbol = f"{exchange}:{symbol}"

        elif isinstance(contract, int):
            symbol = f"{exchange}:{symbol}{contract}!"

        else:
            raise ValueError("not a valid contract")

        return symbol

    def get_timeseries_earnings_dividends(
        self,
        symbol: str,
        exchange: str = "NASDAQ",
        interval: Interval = Interval.in_daily,
        n_bars: int = 10,
        fut_contract: int = None,
        extended_session: bool = False,
        debug=False,
    ) -> pd.DataFrame:
        """get financial history data

        Args:
            symbol (str): symbol name
            exchange (str, optional): exchange, not required if symbol is in format EXCHANGE:SYMBOL. Defaults to None.
            fut_contract (int, optional): None for cash, 1 for continuous current contract in front, 2 for continuous next contract in front . Defaults to None.
            html : flag to requrn html tables in tuples
            debug: flag - to return raw data from socket

        Returns:
        tuple ( tupee(DFs) , dictionary )
            tuple of DFs (df_revenue_q , df_earnings_q, df_revenue_f, df_earnings_f)
            dataframe : 4x
            and dictionary of the sanitized  dict data
        """
        symbol = self.__format_symbol(
            symbol=symbol, exchange=exchange, contract=fut_contract
        )

        interval = interval.value

        self.__create_connection()

        self.__send_message("set_auth_token", [self.token])
        self.__send_message("chart_create_session", [self.chart_session, ""])
        self.__send_message("switch_timezone", [self.chart_session, "exchange"])

        self.__send_message(
            "resolve_symbol",
            [
                self.chart_session,
                "sds_sym_1",
                '={"symbol":"' + symbol + '","adjustment":"splits","currency-id":"USD"'
                # + ('"regular"' if not extended_session else '"extended"')
                + "}",
            ],
        )
        self.__send_message(
            "create_series",
            [self.chart_session, "sds_1", "s1", "sds_sym_1", interval, n_bars, ""],
        )

        # self.__send_message(
        #     "request_more_tickmarks",
        #     [self.chart_session, "sds_1", 10],
        # )
        # self.__send_message(
        #     "request_more_data",
        #     [self.chart_session, "sds_1", 29],
        # )

        self.__send_message(
            "create_study",
            [
                self.chart_session,
                "st1",
                "st1",
                "sds_1",
                "Earnings@tv-basicstudies-240",
                {},
            ],
        )
        self.__send_message(
            "create_study",
            [
                self.chart_session,
                "st2",
                "st1",
                "sds_1",
                "Dividends@tv-basicstudies-240",
                {},
            ],
        )
        # self.__send_message(
        #     "create_study",
        #     [
        #         self.chart_session,
        #         "st2",
        #         "st1",
        #         "sds_1",
        #         "BarSetContinuousRollDates@tv-corestudies-28",
        #         '{currenttime: "now"}',
        #     ],
        # )

        raw_data = ""

        logger.debug(f"getting data for {symbol}...")
        while True:
            try:
                result = self.ws.recv()
                # raw_data = raw_data + result + "\n"
                raw_data = raw_data + result
            except Exception as e:
                print ("------- WS Timeout -------")
                logger.error(e)
                print (raw_data)
                break

            # if ("study_completed" in result) and ("series_completed" in result) :
            if (raw_data.count("study_completed") == 2) and ("series_completed" in raw_data) :
                break
        # print ("DATA >>>>> \n", raw_data)
        if debug:
            print(self.session, self.chart_session)
            return raw_data
    
        return self.__create_ohlcv_earnings_dividends(raw_data)

    

    def get_financials(
        self,
        symbol: str,
        exchange: str = "NASDAQ",
        fut_contract: int = None,
        html=False,
        debug=False,
    ) -> pd.DataFrame:
        """get financial history data

        Args:
            symbol (str): symbol name
            exchange (str, optional): exchange, not required if symbol is in format EXCHANGE:SYMBOL. Defaults to None.
            fut_contract (int, optional): None for cash, 1 for continuous current contract in front, 2 for continuous next contract in front . Defaults to None.
            html : flag to requrn html tables in tuples
            debug: flag - to return raw data from socket

        Returns:
        tuple ( tupee(DFs) , dictionary )
            tuple of DFs (df_revenue_q , df_earnings_q, df_revenue_f, df_earnings_f)
            dataframe : 4x
            and dictionary of the sanitized  dict data
        """
        symbol = self.__format_symbol(
            symbol=symbol, exchange=exchange, contract=fut_contract
        )

        # interval = interval.value

        self.__create_connection()

        self.__send_message("set_auth_token", [self.token])
        # self.__send_message("chart_create_session", [self.chart_session, ""])
        self.__send_message("quote_create_session", [self.session])

        self.__send_message(
            "quote_add_symbols",
            [
                self.session,
                '={"symbol":"'
                + symbol
                + '","adjustment":"splits","currency-id":"USD"'
                + "}",
            ],
        )
        self.__send_message(
            "quote_fast_symbols",
            [
                self.session,
                '={"symbol":"'
                + symbol
                + '","adjustment":"splits","currency-id":"USD"'
                + "}",
            ],
        )

        raw_data = ""

        logger.debug(f"getting data for {symbol}...")
        while True:
            try:
                result = self.ws.recv()
                # raw_data = raw_data + result + "\n"
                raw_data = raw_data + result
            except Exception as e:
                logger.error(e)
                break

            if "quote_completed" in result:
                break
        # print ("DATA >>>>> \n", raw_data)
        if debug:
            print(self.session)
            return raw_data

        # to extract tuple: (revenueQ, earningsQ, revenueFY, earningsFY), finDict = tv.get_financials
        if html:
            return (
                self.__create_earnings_df(raw_data),
                self.__create_financial_dict_full(raw_data),
                self.__create_html(raw_data),
            )
        else:
            return (
                self.__create_earnings_df(raw_data),
                self.__create_financial_dict_full(raw_data),
            )

    def get_timeseries(
        self,
        symbol: str,
        exchange: str = "NYSE",
        interval: Interval = Interval.in_daily,
        n_bars: int = 10,
        fut_contract: int = None,
        extended_session: bool = False,
        debug=False,
    ) -> pd.DataFrame:
        """get historical data

        Args:
            symbol (str): symbol name
            exchange (str, optional): exchange, not required if symbol is in format EXCHANGE:SYMBOL. Defaults to None.
            interval (str, optional): chart interval. Defaults to 'D'.
            n_bars (int, optional): no of bars to download, max 5000. Defaults to 10.
            fut_contract (int, optional): None for cash, 1 for continuous current contract in front, 2 for continuous next contract in front . Defaults to None.
            extended_session (bool, optional): regular session if False, extended session if True, Defaults to False.

        Returns:
            pd.Dataframe: dataframe with sohlcv as columns
        """
        symbol = self.__format_symbol(
            symbol=symbol, exchange=exchange, contract=fut_contract
        )

        interval = interval.value

        self.__create_connection()

        self.__send_message("set_auth_token", [self.token])
        self.__send_message("chart_create_session", [self.chart_session, ""])
        self.__send_message("quote_create_session", [self.session])
        self.__send_message(
            "quote_set_fields",
            [
                self.session,
                "qs_DlCLZ4f9LAdF",
                "base-currency-logoid",
                "ch",
                "chp",
                "currency-logoid",
                "currency_code",
                "currency_id",
                "base_currency_id",
                "current_session",
                "description",
                "exchange",
                "format",
                "fractional",
                "is_tradable",
                "language",
                "local_description",
                "listed_exchange",
                "logoid",
                "lp",
                "lp_time",
                "minmov",
                "minmove2",
                "original_name",
                "pricescale",
                "pro_name",
                "short_name",
                "type",
                "typespecs",
                "update_mode",
                "volume",
                "variable_tick_size",
                "value_unit_id",
                "unit_id",
                "measure",
            ],
        )

        self.__send_message(
            "quote_add_symbols",
            [
                self.session,
                symbol,
                # {"flags": ["force_permission"]}
                '={"adjustment":"splits","currency-id":"USD"}',
            ],
        )
        self.__send_message(
            "quote_fast_symbols",
            [
                self.session,
                symbol,
                '={"adjustment":"splits","currency-id":"USD"}',
            ],
        )

        self.__send_message(
            "resolve_symbol",
            [
                self.chart_session,
                "sds_sym_1",
                '={"symbol":"' + symbol + '","adjustment":"splits","currency-id":"USD"'
                # + ('"regular"' if not extended_session else '"extended"')
                + "}",
            ],
        )
        # self.__send_message(
        #     # "create_series",
        #     "request_more_data",
        #     # [self.chart_session, "s1", "s1", "symbol_1", interval, n_bars],
        #     [self.chart_session, "sds_1",],
        # )
        self.__send_message(
            # "create_series",
            "create_series",
            # [self.chart_session, "s1", "s1", "symbol_1", interval, n_bars],
            # [self.chart_session, "sds_sym_2", "s2", "symbol_1", interval, n_bars, ""],
            # [self.chart_session, "sds_2", "s2", "symbol_1", interval, n_bars, ""],
            [self.chart_session, "sds_1", "s1", "sds_sym_1", interval, n_bars, ""],
        )
        self.__send_message("switch_timezone", [self.chart_session, "exchange"])

        raw_data = ""

        logger.debug(f"getting data for {symbol}...")
        while True:
            try:
                result = self.ws.recv()
                raw_data = raw_data + result + "\n"
            except Exception as e:
                logger.error(e)
                break

            if "series_completed" in result:
                # and "quote_completed" in result
                break

        if debug:
            print(self.session, self.chart_session)
            return raw_data

        return self.__create_timeseries_df(raw_data, symbol)

    @staticmethod
    def __create_html(raw_data):

        # convert to dict
        raw_data = re.sub(r"\\\"", "", raw_data)  # removes \" from string
        raw_data = re.sub(r"\\", "", raw_data)  # removes \ from string
        raw_data = re.sub(r"~m~(.+?)~m~", ",", raw_data)  #  ~m--m~ from string
        # remove the first comma and append to a list []
        raw_data = "[" + raw_data[1:] + "]"
        dataDict = json.loads(raw_data)  # this is the dicts

        # HTML conversion - manual
        htmlText = ""
        count = 0
        for toplevelItem in dataDict:
            # print (toplevelItem)
            try:
                dd = toplevelItem["p"][1]["v"]  # a dict
                for item in dd:
                    if type(dd[item]) == dict:
                        try:
                            # print(item, dd[item])
                            htmlText += "<strong>" + item + "</strong>"
                            count += 1
                            # table = pd.DataFrame(dd[item]).to_html()
                            df = pd.DataFrame(dd[item], index=[0])  # scalar dict data
                            htmlText += df.to_html()
                            # print("table added")
                        except:
                            # print("exception #1 ! ")
                            pass
                    elif type(dd[item]) == list:
                        # # print (item, dd[item])
                        if type(dd[item][0]) == dict:
                            htmlText += "<strong>" + item + "</strong>"
                            count += 1
                            try:
                                # ? KEY financial data is here
                                htmlText += pd.DataFrame(
                                    dd[item]
                                ).to_html()  # 2D dict data
                                # print(item, "2D table added")
                            except:
                                # print("exception #2 ! ")
                                pass
                        else:
                            # # print (item, dd[item])
                            try:
                                htmlText += (
                                    "<strong>"
                                    + item
                                    + "</strong>"
                                    + "<table border='1'><tr>"
                                )
                                count += 1
                                for i in dd[item]:
                                    htmlText += "<td>" + str(i) + "</td>"
                                htmlText += "</tr></table>"
                                # print(item, "1D row added")
                            except:
                                # print("exception #3 ! ")
                                pass
                    else:
                        try:
                            htmlText += (
                                "<strong>"
                                + item
                                + "</strong> :    "
                                + str(dd[item])
                                + "</br>"
                            )
                            count += 1
                        except:
                            # print("exception #4 ! ")
                            pass
            except:
                pass

        return htmlText


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    tv = tvData()
    print(tv.get_timeseries("CRUDEOIL", "MCX", fut_contract=1))
    print(tv.get_timeseries("SPY", ""))
    print(
        tv.get_timeseries(
            "EICHERMOT",
            "NSE",
            interval=Interval.in_1_hour,
            n_bars=500,
            extended_session=False,
        )
    )
