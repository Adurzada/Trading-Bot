#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd
import numpy as np
from binance import Client
import matplotlib.pyplot as plt
client = Client()


# In[37]:


def getdata(s,i='1h',lookback="400"):
    frame = pd.DataFrame(client.get_historical_klines(s,i,lookback + 'hours UTC'))
    frame = frame.iloc[:,0:6]
    frame.columns = ['Time','Open',"High",'Low','Close','Volume']
    frame.set_index('Time', inplace=True)
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame


# In[38]:


df = getdata('ETHUSDT')


# In[39]:


df['rollhigh'] = df.High.rolling(15).max()


# In[40]:


df['rolllow'] = df.Low.rolling(15).min()


# In[41]:


df['mid'] = (df.rollhigh + df.rolllow)/2
print(df)


# In[42]:


df['highapproach'] = np.where(df.Close > df.rollhigh * 0.996,1,0)


# In[43]:


df['close_a_mid'] = np.where(df.Close > df.mid,1,0)


# In[44]:


df['midcross'] = df.close_a_mid.diff() == 1


# In[45]:


in_position = False
buydates,selldates = [],[]

for i in range(len(df)):
    if not in_position:
        if df.iloc[i].midcross:
            buydates.append(df.iloc[i+1].name)
            in_position = True
    if in_position:
        if df.iloc[i].highapproach:
            selldates.append(df.iloc[i+1].name)
            in_position = False


# In[48]:



plt.figure(figsize=(20,10))
plt.plot(df[['Close',"rollhigh",'rolllow','mid']])
plt.scatter(buydates, df.loc[buydates].Open, marker="^", color = 'g', s=200)
plt.scatter(selldates, df.loc[selldates].Open, marker = "v", color='r',s=200)


# In[ ]:




