
import websocket
from websocket import create_connection
import time
import threading
import json
import re 
import requests


# SOCKET = "wss://data.tradingview.com/socket.io/websocket"
SOCKET = "wss://data.tradingview.com/socket.io/websocket?from=chart%2FK6x3E8ws%2Ftype=chart"
timeout = 5
headers = {
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    # "Cache-Control": "no-cache",
    "Connection": "Upgrade",
    "Host": "data.tradingview.com",
    "Origin": "https://www.tradingview.com",
    # "Pragma": "no-cache",
    # "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
    # "Sec-WebSocket-Key": "Qf9IDRKqcgNBrNs7X4FK9w==",
    # "Sec-WebSocket-Version": 13,
    "Upgrade": "websocket",
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0"
}

ws = None
import string, random 
def __create_connection():
    print("creating websocket connection")
    ws = create_connection(
        "wss://data.tradingview.com/socket.io/websocket",
        headers=headers,
        timeout=timeout,
    )
    return ws
def __generate_session():
    stringLength = 12
    letters = string.ascii_lowercase
    random_string = "".join(random.choice(letters) for i in range(stringLength))
    return "qs_" + random_string
def __generate_chart_session():
    stringLength = 12
    letters = string.ascii_lowercase
    random_string = "".join(random.choice(letters) for i in range(stringLength))
    return "cs_" + random_string
def __prepend_header(st):
    return "~m~" + str(len(st)) + "~m~" + st
def __construct_message(func, param_list):
    return json.dumps({"m": func, "p": param_list}, separators=(",", ":"))
def __create_message(func, paramList):
    return __prepend_header(__construct_message(func, paramList))
def __send_message(func, args):
    m = __create_message(func, args)
    # if ws_debug:
    print(m)
    ws.send(m)


# Getting the WS data 

symbol: str = "SPY"
exchange: str = "NASDAQ"
interval: str = "1D"
n_bars: int = 100
fut_contract: int = None
extended_session: bool = False
debug=False

username = "rookiecurie"
password = "OPhjfd7jdt$_sddDdx"
data = {"username": username, "password": password, "remember": "on"}
sign_in_url = "https://www.tradingview.com/accounts/signin/"
try:
    response = requests.post(
        url=sign_in_url, data=data, headers=self.signin_headers
    )
    print (response.json())
    token = response.json()["user"]["auth_token"]
except Exception as e:
    print("error while signin")
    token = None

print ("Auth Token : ", token)
# tv = tvData (username, password) # works 
token = tv.token # get token
# token="unauthorized_user_token"

ws = None
session = __generate_session()
chart_session = __generate_chart_session()

# initialize connection and 
ws = __create_connection()
__send_message("set_auth_token", [token])

__send_message("chart_create_session", [chart_session, ""])
__send_message("switch_timezone", [chart_session, "exchange"])
__send_message(
    "resolve_symbol",
    [
        chart_session,
        "sds_sym_1",
        '={"symbol":"' + symbol + '","adjustment":"splits","currency-id":"USD"'
        # + ('"regular"' if not extended_session else '"extended"')
        + "}",
    ],
)
__send_message(
    "create_series",
    [chart_session, "sds_1", "s1", "sds_sym_1", interval, n_bars, ""],
)

# __send_message
r = {  "m": "create_study", 
        "p": [ 
        chart_session,
        "st1",
        "st1",
        "sds_1",
        "Script@tv-scripting-101!", 
        # json.dumps( 
        {"text": "bmI9Ks46_46gN8zUfgFGkqBgwXG+81g==_9P5Svbf02sdKFCBA0XcEAIE105BbvlXIhu/gJJtq2dnC+fTx1qkaJ9YF0g9uL1A0wbLS0/gP6Jlp9rXkUFnPl5krxWvyHC0RBZnVz8l4k5Noauyavlzgci0nD73q8Vyg6TFqwXIjtyzFOlksJ5ebzffZXsCNc02gcSN04LETuPmZ3wPA1zOEEct4EMnXpGsvdWHtgv1d+d4ncRO6c8/Mq3kddBrgUxozvo/Vpbs3G+WOJG2pKZWLFxrwUgEFH+KS0wmtlnJfq1tV0aN09jg/ilEmr4Rf/33eCky9B8OqXC737LP7m1t7nZYXgQU4TkoG8CU6oynWPQA6lzJKknjbfCXtBlhe72iaPjjRvC8obB98R0oHqIdqyGl6vj/6qQRFW99q7/1z5Ebeyue6UnUnR+8dSKJocdYJsgbAWLwTVDdz90SPi6kLHaLkoPwymAcHNNnDdZSAYmu0mnmV2ewU184BnPXEg+/uo7nBXtclwMkuBGg22TNKi3u7ZCp0kO/4zZqgEBW/efSgoNZx4aKcvYzsDouz/EHtGvdiSu+b8HgG2QICBSo2Qg2NdU4iYiz0VwV5mrVnhoA6yMev7/ZCENUpeSdiDAl0EYSInlLjCLTmbQKW0i3vsEqMishKqVDXrbbrC8Fc49TD9zjVbtxr33Ml1J3yIyBNusSJC7KbN+liNH0H44GOanyUkof8smIhYSoufuRaxdw7uY117PwVwxr8BGITTdgaoyovpBVxNssEeu87zeGVMj80Wlv7AD1LxmeGrtpETJQIM4U2ox8aCeSUnHKM/wJtvldj+3CmQtwF3Vc0d9j7ThhCw8BqlGX8BILITq7KTuhOPJccDJeDoMzLzU/DWROSBafrgIcastjrt41A28Os8FvhVKkkrrmlglsGQIcf5fUudTXL5mQemO3XU/dJSrQ/i7PTLKJTq3Phxuij9n58KWpnqm8uXK4kTkbqcsxHSS4HMq/pkQeY4wy+z9n7v/YMfz8FGmO28zCtX6cWgLQ2E1qA5kmgca1rwzVI3l1Ga6HXK2hU3VQ3X1jz3DLE0XBf9D0hqQCxfhQz4kwUCcQEBApv52IAXYV8bSvqrPpIF8L9cSlUaHN0B7b4fOaegkCB0+xhvalMTUvzm4yQQkea6fTzvDcu31nD5pqwYYMBekQ2V9QzdNQyCeZ+4HQiFzVwcNajO9ENftNt7qmBz3kmbLwlrEaOaq/l",
        "pineId": "USER;a36f8317c1ed4fa691838837a1af4aae",
        "pineVersion": "16.0",
        "pineFeatures": {
            "v": '{"indicator":1,"plot":1,"ta":1,"math":1}',
            "f": True,
            "t": "text"
        },
        "in_0": {
            "v": 9,
            "f": True,
            "t": "integer"
        },
        "in_1": {
            "v": 50,
            "f": True,
            "t": "integer"
        },
        "in_2": {
            "v": "",
            "f": True,
            "t": "resolution"
        },
        "__profile": {
            "v": False,
            "f": True,
            "t": "bool"
        }
    }      
    # )
    ]
}
# json.dumps(r, separators=(",", ":"))

ws.send(
    __prepend_header(json.dumps(r, separators=(",", ":")))
)

# __send_message(
#     "create_study",
#     [
#         chart_session,
#         "st2",
#         "st1",
#         "sds_1",
#         "BarSetContinuousRollDates@tv-corestudies-28",
#         '{currenttime: "now"}',
#     ],
# )

# initialize placeholders 
ws_raw_data = ""
result = ws.recv()
while True:
    try:
        result = ws.recv()
        ws_raw_data = ws_raw_data + result
    except Exception as e:
        print ("------- WS Timeout -------")
        print (ws_raw_data)
        break
    # if (ws_raw_data.count("study_completed") == 2) and ("series_completed" in ws_raw_data) :
    # if ("series_completed" in ws_raw_data) :
    # if ("study_completed" in ws_raw_data) :
    if ("series_completed" in ws_raw_data and "study_completed" in ws_raw_data) :
        break

raw_data = ws_raw_data

# Format Raw data 
raw_data = re.sub(r"\\\"", '', raw_data) # removes \" from string 
raw_data = re.sub(r"\\", '', raw_data) # removes \ from string 
raw_data = re.sub(r"~m~(.+?)~m~", ',', raw_data) #  ~m--m~ from string 
raw_data = "["+raw_data[1:]+"]" # remove the first comma and append to a list [] 
dataDict = json.loads(raw_data)

# identify : timeseries OHLCV 
import pandas as pd
df = None 
for item in dataDict : 
    try : 
        ts = item ['p'][1]['sds_1']['s'] # ohlc array 
        
        # Time series : ohlcv 
        t = list(map(lambda x : x['v'], ts))
        has_volume = len(t[0]) == 6
        t_col = ["datetime", "open", "high", "low", "close", "volume"] if has_volume else ["datetime", "open", "high", "low", "close"]  # NO VOLUME DATA CASE HANDLING
        
        df = pd.DataFrame(t, columns=t_col)
        df['datetime'] = pd.to_datetime(df['datetime'], unit='s')
        df = df.set_index('datetime')             
        if not has_volume :  df["volume"] = 0.0 # NO VOLUME DATA CASE HANDLING                    
    except : pass 

df  # final dataframe - OHLCV 






def on_open(ws):
    print('opened connection')
    # def run(*args):
    #     for i in range(30):
    #         time.sleep(1)
    #         ws.send("Hello %d" % i)
    #     time.sleep(1)
    #     ws.close()
    #     print("thread terminating...")
    # threading.start_new_thread(run, ())
    time.sleep(2)
    ws.send('~m~524~m~{"m":"set_auth_token","p":["eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJ1c2VyX2lkIjo5OTIxMjA1LCJleHAiOjE2MDM2NzgyMDcsImlhdCI6MTYwMzY2MzgwNywicGxhbiI6IiIsImV4dF9ob3VycyI6MSwicGVybSI6IiIsInN0dWR5X3Blcm0iOiJQVUI7eXNueXc5aUVOY0dTeEhJQk9pNGJUUDFIczJreVg2Y1EsUFVCO0ZQRlJnWU5FOTZiZEI3MXBBZ1RSUGdIa3dLWGswZnJXIiwibWF4X3N0dWRpZXMiOjMsIm1heF9mdW5kYW1lbnRhbHMiOjB9.LTCdVfkkquhStte9UU_xWiVJE-ZBIoShUrPQP6vywh1ep3S894qEpk3h509utD5vmz8vgAzcJRZKy3eKPMY-bh81gg76WRjwdjJ2RM2YnoQ7tAhKF0wK78-JFg_3BfcTmude1ypJu_7I5NJgeF8RqM78ymJ6OTiKzgu84ZrMRr4"]}')
    ws.send('~m~54~m~{"m":"set_auth_token","p":["unauthorized_user_token"]}')
    ws.send('~m~55~m~{"m":"chart_create_session","p":["cs_zEcm9GqyQdK0",""]}')
    ws.send('~m~52~m~{"m":"quote_create_session","p":["qs_x72fChUYomPp"]}')
    ws.send('~m~344~m~{"m":"quote_set_fields","p":["qs_x72fChUYomPp","ch","chp","current_session","description","local_description","language","exchange","fractional","is_tradable","lp","lp_time","minmov","minmove2","original_name","pricescale","pro_name","short_name","type","update_mode","volume","currency_code","logoid","currency-logoid","base-currency-logoid"]}')

    ws.send('~m~98~m~{"m":"quote_add_symbols","p":["qs_x72fChUYomPp","SPY",{"flags":["force_permission"]}]}')
    ws.send('~m~98~m~{"m":"quote_fast_symbols","p":["qs_x72fChUYomPp","SPY",]}')



def on_close(ws):
    print('closed connection')


def on_message(ws, message):
    # p = message.split('~', -1)[4]
    # data = json.loads(p)
    # print(data)
    print(f'received message :: {message}')
    if 'lp' in message:
        print (p)
        # p = message.split('~', -1)[4]
        # data = json.loads(p)
        # # print(data)
        # timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        # symbol = data['p'][1]['n']
        # ltp = data['p'][1]['v']['lp']
        # volume = data['p'][1]['v']['volume']
        # if symbol.upper() == "SPY":
        #     print(f'tick :: {timestamp} :: {symbol} :: {ltp} :: {volume}')

# if __name__ == "__main__":
websocket.enableTrace(False)
ws = websocket.WebSocketApp(
    SOCKET, on_message=on_message, on_open=on_open, on_close=on_close)
wst = threading.Thread(target=ws.run_forever)
wst.daemon = True
wst.start()

conn_timeout = 60
while not ws.sock.connected and conn_timeout:
    time.sleep(1)
    conn_timeout -= 1

while ws.sock is not None:
    time.sleep(10)