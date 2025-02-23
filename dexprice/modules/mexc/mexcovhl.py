import requests
import json
import time
import time
import dexprice.modules.utilis.timedefine as timedefine
import dexprice.modules.mexc.mexc_queue as mexc_queue
import dexprice.modules.utilis.define as define
def get_kline_data(symbol, interval="Min15", start=None, end=None,port=7890):
   # url = f"https://contract.mexc.com/api/v1/contract/kline/{symbol}"
    url = f"https://contract.mexc.com/api/v1/contract/kline/{symbol}"

    params = {"interval": interval}

    if start:
        params["start"] = start
    if end:
        params["end"] = end
    httpurl = "http://127.0.0.1:"+str(port)

    proxies = {
        "http": httpurl,
        "https": httpurl
    }

    # 生成完整 URL 并打印
    full_url = requests.Request('GET', url, params=params).prepare().url


    response = requests.get(url, params=params,proxies=proxies)

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data["data"]
        else:
            print("API Response Error:", data)
            print(f"the token is {symbol}")
    else:
        print("HTTP Request Failed with Status Code:", response.status_code)

    return None


def mexc_token_history(ohlcv_data, pool_address):
    historydatas = []
    if(ohlcv_data):
        for entry in ohlcv_data['data']['attributes']['ohlcv_list']:
            pass
           # historydata =  define.OvhlFromCex(pool_address[0],entry[1],entry[2],entry[3],entry[4],timestamp_to_datetime(entry[0]),entry[5])
            # print(entry)
            #historydatas.append(historydata)
    return historydatas



def determine_initial_timesta(symbol,port=7890):
    interval = "Month1"
    start = None  # 允许为空
    # end is the now time
   # end = 1738308461  # 允许为空
    end = None
   # end = int(time.time())
    kline_data = get_kline_data(symbol, interval, start, end,port)
    time = kline_data['time']
    if (len(time) <= 2000):
        start = time[0]
        #here we find the start month
        #and we need find the start time
        end = timedefine.addtime(start)
        interval = 'Day1'
        kline_data = get_kline_data(symbol, interval, start, end,port)
        real_start = kline_data['time'][0]
        time  = timedefine.timestamp_to_datetime(real_start)
        return time
    else:
        print(" to old we  delete")
        return None


def mexc_token_history_basic(ohlcv_data, symbol):
    historydatas = []
    if(ohlcv_data):
        timelen = len(ohlcv_data.get('time'))

        for i in range(timelen):
            timedata = ohlcv_data.get('time')[i]
            open = ohlcv_data.get('open')[i]
            high = ohlcv_data.get('high')[i]
            low = ohlcv_data.get('low')[i]
            close = ohlcv_data.get('close')[i]
            volume = ohlcv_data.get('vol')[i]
            amount = ohlcv_data.get('amount')[i]
            historydata =  define.OvhlFromCex(symbol,open,high,low,close,timedefine.timestamp_to_datetime(timedata),volume,amount)

            historydatas.append(historydata)
    return historydatas


def mexc_token_history(symbol, interval="Min15", start=None, end=None,port=7890 ):
    kline_data = get_kline_data(symbol, interval, start, end,port)
    historydatas = mexc_token_history_basic(kline_data, symbol)
    return historydatas


def mexc_token_history_queue(  queue: mexc_queue.mexcqueue,port=7890 ):
    symbol = queue.symbol
    kline = queue.kline
    aggregate = queue.aggregate
    starttime = queue.starttime
    endtime = queue.endtime
    interval  = kline+aggregate
    kline_data = get_kline_data(symbol, interval, starttime, endtime,port)
    historydatas = mexc_token_history_basic(kline_data, symbol)
    return historydatas
# kline_data = get_kline_data('BTC_USDT', 'Min60', 1740020707, 1740196980,7890)
#
# print(kline_data)