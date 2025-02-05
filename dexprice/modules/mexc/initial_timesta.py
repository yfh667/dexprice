import requests
import json
import time
import time
import dexprice.modules.utilis.timedefine as timedefine
def get_kline_data(symbol, interval="Min15", start=None, end=None,port=7890):
    url = f"https://contract.mexc.com/api/v1/contract/kline/index_price/{symbol}"
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
  #  print(f"Request URL: {full_url}")

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

