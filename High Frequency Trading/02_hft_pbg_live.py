import ccxt.pro as ccxtpro
from asyncio import run
import requests
import configparser
from multiprocessing import Process, Value

config = configparser.ConfigParser()
config.read('config.ini')
api_key=config.get("HITBTC", "api_key")
api_secret=config.get("HITBTC", "api_secret")
curl=config.get('HITBTC', 'curl')


def book(orderbook):
    bids = orderbook['bids'][0]
    asks = orderbook['asks'][0]
    bid = round(bids[0], decimals)
    ask = round(asks[0], decimals)
    spread = ask - bid
    spread_tick = int(round(spread / tick, 0))
    available_tick = spread_tick - 1
    return bid, ask, available_tick


async def portafoglio(portafoglio_base, portafoglio_target):
    while True:
        try:
            balance = await ccPro.fetch_balance()
            totale_b = balance[base]['total']
            totale_t = balance[target]['total']
            portafoglio_base.value = totale_b
            portafoglio_target.value = totale_t
            print(f'portafoglio_base: {totale_b}, portafoglio_target: {totale_t}')
        except Exception as ex:
            print(ex)


async def order(portafoglio_base, portafoglio_target):
    def delete_order(id):
        url = f"https://api.hitbtc.com/api/3/spot/order/{id}"
        headers = {'Authorization': f'Basic {curl}'}
        requests.request("DELETE", url, headers=headers, data={})
    
    def aggressivity(bid, ask, bagg, aagg):
        buy_price = bid + bagg * (ask - bid)
        sell_price = ask - aagg * (ask - bid)
        buy_price = round(buy_price, decimals)
        sell_price = round(sell_price, decimals)
        return buy_price, sell_price


    old_available_tick = 0
    while True:
        try:
            try:
                orderbook = await ccPro.watch_order_book(symbol, 50)
                bid, ask, available_tick = book(orderbook)

                if old_available_tick != available_tick:
                    print('Recalculated orders')
                    orders = await ccPro.fetch_open_orders(symbol)
                    for ord in orders:
                        delete_order(ord['id'])
                    
                    if available_tick == 0:
                        buy_price, sell_price = aggressivity(bid, ask, 0, 0)
                    elif available_tick == 1:
                        buy_price, sell_price = aggressivity(bid, ask, 0, 0.33)
                    elif available_tick == 2:
                        buy_price, sell_price = aggressivity(bid, ask, 0.2, 0.33)
                    elif available_tick == 3:
                        buy_price, sell_price = aggressivity(bid, ask, 0.2, 0.2)
                    else:
                        buy_price, sell_price = aggressivity(bid, ask, 0.4, 0.4)
                    print(available_tick, bid, ask, buy_price, sell_price)
                    try:
                        await ccPro.create_limit_buy_order(symbol=symbol, amount=portafoglio_base.value*0.999 / buy_price, price=buy_price)
                    except Exception as ex:
                        pass

                    try:
                        await ccPro.create_limit_sell_order(symbol=symbol, amount=portafoglio_target.value, price=sell_price)
                    except Exception as ex:
                        pass
                
                    orderbook = await ccPro.watch_order_book(symbol, 50)
                    bid, ask, available_tick = book(orderbook)

            except Exception as ex:
                print(ex)

        except Exception as ex:
            print(ex)


def runThread(thread, b, t, bid, ask, pos, ava):
    if thread == 'portafoglio':
        run(portafoglio(b, t))
    elif thread == 'order':
        run(order(b, t))


exchange = 'hitbtc'
symbol = "btc/usdt".upper()
tick = 0.01
decimals = 2

target = symbol.split('/')[0]
base = symbol.split('/')[1]
ccPro = getattr(ccxtpro, exchange)({'apiKey': api_key,'secret': api_secret})


if __name__ == '__main__':
    portafoglio_base = Value('f', 0)
    portafoglio_target = Value('f', 0)
    bid = Value('f', 0)
    ask = Value('f', 0)
    available_tick = Value('f', 0)

    portafoglioThread = Process(target=runThread, args=('portafoglio',portafoglio_base,portafoglio_target,None,None,None,None))
    portafoglioThread.start()

    orderThread = Process(target=runThread, args=('order',portafoglio_base,portafoglio_target,bid,ask,None,available_tick,))
    orderThread.start()

    portafoglioThread.join()
    orderThread.join()
