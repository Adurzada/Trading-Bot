'''AACJjU03MB618TWIQkr8szANUsfxeU61VGtwUm1AFcZ6eMpL0YLCK0Nh'''
'''319FhLFi55TeXmwATQgsdByOUGMr+VOw7ga2tb4jDTNUr7glDhGYXgFEJOhComdEm2ZEIhTIW+Som/UyBLwq4A=='''
import time
import requests
import urllib.parse
import hashlib
import hmac
import base64
import pandas
import matplotlib

api_url = "https://api.kraken.com"
with open("keys", "r") as f:
    lines = f.read().splitlines()
    api_key = lines[0]
    api_sec = lines[1]


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
InterestAssets = ["XBT, ETH"]


def read_command(c):
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
        assetsString = ""
        for coin in InterestAssets:
            assetsString = assetsString + coin + ","
        assetsString = assetsString[:-1]
        print(assetsString)
        params['asset'] = assetsString
        values = get_public_info("Assets", params)
        print(values['result'])


'''read_command(c)
read_command("AssetInfo")'''

