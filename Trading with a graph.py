#!/usr/bin/env python
# coding: utf-8

# In[153]:


import time
import requests
import urllib.parse
import hashlib
import hmac
import base64
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# In[162]:


api_url = ""
api_key = ""
api_sec = ""


def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


def kraken_request(url_path, data, api_key, api_sec):
    headers = {"API-Key": api_key, "API-Sign": get_kraken_signature(url_path, data, api_sec)}
    resp = requests.post((api_url + url_path), headers=headers, data=data)
    return resp


def get_info(domain, params):
    resp = kraken_request(("/0/private/" + domain), params, api_key, api_sec)
    return resp.json()


def get_public_info(domain, params):
    resp = kraken_request(("/0/public/" + domain), params, api_key, api_sec)
    return resp.json()


c = "OpenOrders"
InterestAssets = ["XBT", "ETH"]

def read_command(c, interval):
    params = {
        "nonce": str(int(1000 * time.time()))
    }
    if c == "Balance":
        values = get_info("Balance", params)['result']
        for coin in values:
            if float(values[coin]) > 0:
                print(coin + "  -  " + values[coin])
    elif c == "TradeBalance":
        values = get_info(c,params)['result']
        print(values)
    elif c == "OpenOrders":
        values = get_info(c,params)['result']
        descrs = []
        for value in values['open']:
            print(values['open'][value]['descr'])
            descrs.append(values['open'][value]['descr'])
        return descrs
    elif c == "AssetInfo":
        '''
        assetsString = ""
        for coin in InterestAssets:
            assetsString = assetsString + coin + ","
        assetsString = assetsString[:-1]
        print(assetsString)
        params['asset'] = assetsString
        values = get_public_info("Assets", params)
        print(values)
        return values
        '''
        queryDomains = []
        for coin in InterestAssets:
            queryDomains.append("OHLC?pair=" + coin + "USD")
            
        OHLCvals = {}
        '''
        for i in range(0,len(InterestAssets)):
            print(queryDomains[i])
            OHLCvals[InterestAssets[i]] =  "OHLC?pair=" + coin + "USD"
        '''
        params['asset'] = InterestAssets
        #
        #
        #Setting interval
        #
        #
        params['interval'] = interval
        for coin in InterestAssets:
            chubby = get_public_info(("OHLC?pair=" + coin + "USD"), params)
            OHLCvals[coin] = chubby['result']
            
        return OHLCvals
AssetInfo = "AssetInfo"
currentAssets = read_command(AssetInfo, 1)
#print(currentAssets['XBT']['XXBTZUSD']).df
df = pd.DataFrame(currentAssets["XBT"]["XXBTZUSD"])
df.columns = ["Time","O","H","L","C","P","V","X"]
print(df)


# In[163]:


O = []
C = []
H = []
L = []
V = []
Vwa = []

from datetime import datetime, timedelta


def toTimeThis(mili):
    x = str(datetime.today()).split("-")
    day = x[2][0:2]
    z = [int(x[0]),int(x[1]),int((x[2][0:2]))]
    epoch = datetime(z[0], z[1], z[2])
    cookie_microseconds_since_epoch = mili
    cookie_datetime = epoch + timedelta(microseconds=cookie_microseconds_since_epoch)
    str(cookie_datetime)
    return cookie_datetime


for numbers in currentAssets["XBT"]["XXBTZUSD"]:
    O.append(float(numbers[1]))
   # Time.append(toTimeThis(numbers[0]))
    C.append(float(numbers[4]))
    H.append(float(numbers[2]))
    L.append(float(numbers[3]))
    V.append(float(numbers[6]))
    Vwa.append(float(numbers[5]))
dff = pd.DataFrame({"Open":O,"Close":C,"High":H,"L":L,"V":V,"WA":Vwa})
dff["Open"] = dff["Open"].apply(np.ceil)
print(dff.columns)
for col in dff.columns:
    #print(col)
    try:
        dff[col] = dff[col].apply(np.ceil)
        dff[col] = dff[col].apply(int)
    except:
        continue
    


# In[164]:


print(dff)


# In[165]:


xAxis = dff.index
yAxis = dff["Open"]
plt.plot(xAxis,yAxis)
plt.title("BTC / USD")
plt.show()


# In[143]:


print(dff["Open"])


# In[ ]:


'''
sfp
matic
1inch
crv
alice
'''


