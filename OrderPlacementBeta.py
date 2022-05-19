#!/usr/bin/env python
# coding: utf-8

# In[30]:


import sqlalchemy
import pandas as pd
from binance.client import Client


# In[31]:


apikey = "OGyXKP0mwUvRFXahzxzdu9EqCJzgL4f5eZQqnYp5yD20rZ1nwK6AlftN4Pgh5INu"
apisec = "XChS2H1CcydVIhJdTO9jkazUNTYnT3EYBOcKlvlwcrs9iPlxQoOUL1X27BI0OTDX"
client = Client(apikey, apisec)


# In[32]:


engine = sqlalchemy.create_engine("sqlite:///BTCUSDTstream.db")


# In[33]:


df = pd.read_sql('BTCUSDT' , engine)


# In[45]:


print(df.Price)


# In[46]:


def strategy(entry, lookback, qty, open_position=False):
    while True:
        df = pd.read_sql("BTCUSDT", engine)
        lookbackperiod = df.iloc[-lookback:]
        cumret = (lookbackperiod.Price.pct_change() + 1).cumprod() - 1
        if not open_position:
            if cumret[cumret.last_valid_index()] > entry:
                order = client.create_order(symbol = "BTCUSDT", side = "BUY", type = "MARKET", quantity = qty)
                print(order)
                open_position = True
                break;
    if open_position:
        while True:
            df = pd.read_sql("BTCUSDT", engine)
            sincebuy = df.loc[df.Time > pd.to_datetime(order['transactTime'], unit = "ms")]
            if len(sincebuy) > 1:
                sincebuyret = (sincebuy.Price.pct_change() + 1).cumprod() - 1
                lastentry = sincebuyret[sincebuyret.last_valid_index()]
                if lastentry > 0.0015 or lastentry < -0.0015:
                    order = client.create_order(symbol = "BTCUSDT", side = "sell", type = "MARKET", quantity = qty)
                    print(order)
                    break;
        


# In[ ]:


strategy(0.001, 60, 0.001)


# In[ ]:




