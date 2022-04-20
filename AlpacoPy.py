
from alpaca_trade_api import REST, TimeFrame
import datetime as dt
import time
import math
seckey = ""
pubkey = ""
urlbase = ""

api = REST(key_id=pubkey, secret_key=seckey, base_url=urlbase)
sy = "SHIBUSD"


def buycheck(symbol):
    order_buy = api.submit_order(sy, qty=100000, side='buy')
    print(order_buy)


def getsma(series, periods):
    return series.rolling(periods).mean()

SF = 12
SS = 24
def getdata(symbol, time):
    bars = api.get_crypto_bars(symbol=symbol, timeframe=time).df
    bars = bars[bars.exchange == "CBSE"]
    bars['sma_fast'] = getsma(bars.close, SF)
    bars['sma_slow'] = getsma(bars.close, SS)
    return bars

print(getdata(sy, TimeFrame.Minute))

def get_position(symbol):
    positions = api.list_positions()
    for p in positions:
        if p.symbol == symbol:
            return float(p.qty)
    return 0
print(get_position("SHIBUSD"))

q = 200000

def get_pause():
    now = dt.datetime.now()
    next_min = now.replace(second=0, microsecond=0) + dt.timedelta(minutes=1)
    pause = math.ceil((next_min - now).seconds)
    print(pause)
    return pause
def buyma(f,s):
    return f > s
while True:
    bars = getdata(sy, TimeFrame.Minute)
    position = get_position(sy)
    buy = buyma(SF, SS)
    print(f'Symbol:{sy} / Should buy: {buy}')
    if (position == 0 and buy == True):
        print("Buy!")
        api.submit_order(sy, qty=q, side="buy")
    elif position>0 and buy == False:
        print("Sell")
        api.submit_order(sy,qty=q, side="sell")
    time.sleep(get_pause())
    print('-'*35)
