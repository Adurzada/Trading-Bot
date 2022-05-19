#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager
apikey = "OGyXKP0mwUvRFXahzxzdu9EqCJzgL4f5eZQqnYp5yD20rZ1nwK6AlftN4Pgh5INu"
apisec = "XChS2H1CcydVIhJdTO9jkazUNTYnT3EYBOcKlvlwcrs9iPlxQoOUL1X27BI0OTDX"
client = Client(apikey,apisec)
bsm = BinanceSocketManager(client)
socket = bsm.trade_socket("BTCUSDT")


# In[12]:


def createFrame(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:,['s','E','p']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit = 'ms')
    return df


# In[13]:


engine = sqlalchemy.create_engine("sqlite:///BTCUSDTstream.db")


# In[14]:


while True:
    await socket.__aenter__()
    msg = await socket.recv()
    frame = createFrame(msg)
    frame.to_sql('BTCUSDT', engine, if_exists = "append", index = False)
    print(frame)


# In[ ]:




