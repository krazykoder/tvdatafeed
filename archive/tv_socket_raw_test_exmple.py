
import websocket
import time
import threading
import json

SOCKET = "wss://data.tradingview.com/socket.io/websocket"

headers = {
    "Accept-Encoding": "gzip, deflate, br",
    # "Accept-Language": "en-US,en;q=0.9",
    # "Cache-Control": "no-cache",
    # "Connection": "Upgrade",
    "Host": "data.tradingview.com",
    "Origin": "https://www.tradingview.com",
    # "Pragma": "no-cache",
    # "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
    # "Sec-WebSocket-Key": "Qf9IDRKqcgNBrNs7X4FK9w==",
    # "Sec-WebSocket-Version": 13,
    # "Upgrade": "websocket",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
}


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
    # ws.send('~m~524~m~{"m":"set_auth_token","p":["eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJ1c2VyX2lkIjo5OTIxMjA1LCJleHAiOjE2MDM2NzgyMDcsImlhdCI6MTYwMzY2MzgwNywicGxhbiI6IiIsImV4dF9ob3VycyI6MSwicGVybSI6IiIsInN0dWR5X3Blcm0iOiJQVUI7eXNueXc5aUVOY0dTeEhJQk9pNGJUUDFIczJreVg2Y1EsUFVCO0ZQRlJnWU5FOTZiZEI3MXBBZ1RSUGdIa3dLWGswZnJXIiwibWF4X3N0dWRpZXMiOjMsIm1heF9mdW5kYW1lbnRhbHMiOjB9.LTCdVfkkquhStte9UU_xWiVJE-ZBIoShUrPQP6vywh1ep3S894qEpk3h509utD5vmz8vgAzcJRZKy3eKPMY-bh81gg76WRjwdjJ2RM2YnoQ7tAhKF0wK78-JFg_3BfcTmude1ypJu_7I5NJgeF8RqM78ymJ6OTiKzgu84ZrMRr4"]}')
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