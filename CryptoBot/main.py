from csv import excel
import os
import sys
import time
from xml.sax.handler import DTDHandler
import pandas as pd
import datetime as dt
import requests
from binance.client import Client
from binance import ThreadedWebsocketManager

api_key = os.environ['api_key']
api_secret = os.environ['api_secret']
token_telegram = os.environ['token_telegram']
telegram_chat_id = os.environ['telegram_chat_id']
client = Client(api_key, api_secret)
file = "alerting.txt"

def send(text):
    token = token_telegram
    params = {'chat_id': telegram_chat_id, 'text': text, 'parse_mode': 'HTML', 'disable_web_page_preview': True}
    resp = requests.post(
        'https://api.telegram.org/bot{}/sendMessage'.format(token), params)
    resp.raise_for_status()


def alert(file):
    argvs = ""
    with open(file, 'r') as f:
        argvs = f.read().split("\n")
    for raw in argvs:
        asset = raw.split(" ")[0]
        asset_value = float(raw.split(" ")[1])
        operation = raw.split(" ")[2]
        current_price = float(client.get_symbol_ticker(symbol=asset)["price"])
        if operation == "up" and current_price > asset_value:
            txt = "ALERT {0} up {1}".format(asset, asset_value)
            send(txt)
            print(txt)
        if operation == "down" and current_price < asset_value:
            txt = "ALERT {0} down {1}".format(asset, asset_value)
            print(txt)
            send(txt)


    print("Finished")


def kline(tf, symbol, start, end):
    bars = client.get_historical_klines(symbol, tf, str(start), str(end), limit=1000)
    for line in bars:
        del line[5:]
    df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
    df.set_index('date', inplace=True)
    df.index = pd.to_datetime(df.index, unit='ms').tz_localize('UTC').tz_convert('Europe/Rome')

    df['date'] = df.index
    df['symbol'] = symbol
    df['close'] = df.close.astype(float)
    df['open'] = df.open.astype(float)
    df['high'] = df.high.astype(float)
    df['low'] = df.low.astype(float)
    return df


def get_assets(socket, interval='1d'):
    assets = []
    for asset in client.get_account()["balances"]:
        if socket:
            assets.append("{0}{1}{2}".format(asset["asset"].lower(), "usdt@kline_", interval))
            assets.append("{0}{1}".format(asset["asset"], "USDT"))
    return assets


def vol(delta, perc):
    assets = get_assets(socket=False)
    for asset in assets:
        try:
            end = dt.datetime.now()
            start = end - dt.timedelta(days=300)
            df = kline('1d', asset, start, end)
            max = df.iloc[-delta]['high']
            min = df.iloc[-delta]['low']
            
            vol = round((max - min) / min * 100, 2)

            if vol > perc:
                print(assets)
        except Exception as ex:
            skip = "invalid symbol"
            if skip not in str(ex):
                print(ex)


def check_single_candle(interval, perc):
    old = []
    try:

        def handle_socket_message(msg):
            try:
                candle = dt.datetime.fromtimestamp(msg['data']['k']['t']/1000).replace(second=0, microsecond=0)
                asset = msg['data']['s']
                close = float(msg['data']['k']['c'])
                open = float(msg['data']['k']['o'])
                vol = round((close - open) / open * 100, 2)
                finished = msg['data']['k']['x']
                
                if finished:
                    if vol >= perc:
                        print("ALERT {0} > {1}".format(asset, perc))
            except:
                old.append("error")

        streams = get_assets(socket=True, interval=interval)
        twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
        twm.start()
        socket = twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)
        while True:
            if "error" in old:
                twm.stop_socket(socket)
                time.sleep(2)

                old = []
                socket = twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)
            time.sleep(0.1)
            
    except Exception as ex:
        print(ex)

