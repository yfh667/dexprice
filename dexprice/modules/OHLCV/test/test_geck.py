
import  dexprice.modules.OHLCV.geck as geck
import time
from datetime import datetime, timezone


import time
from datetime import datetime, timedelta
def timestamp_to_datetime(timestamp, to_utc=True):
    """
    将时间戳转换为日期时间格式。

    参数:
    - timestamp: 时间戳（秒）
    - to_utc: 是否返回 UTC 时间

    返回:
    - 日期时间格式
    """
    if to_utc:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    else:
        return datetime.fromtimestamp(timestamp)

if __name__ == "__main__":
    # 示例用法
    network = "eth"
    pool_address = ['0xF965fcb75A18fb321B1Fa7F161C099Bf1BE90b70']
    timeframe = "minute"  # 可选值: day, hour, minute



    # time period to aggregate for each ohlcv (eg. /minute?aggregate=15 for 15m ohlcv)
    #
    # Available values (day): 1
    #
    # Available values (hour): 1, 4, 12
    #
    # Available values (minute): 1, 5, 15
    aggregate = "5"     # 聚合时间段


    current_timestamp = int(time.time())
   # utc_time = datetime.fromtimestamp(current_timestamp, tz=timezone.utc)
    before_timestamp = str(current_timestamp)  # 可选的时间戳参数
    print(before_timestamp)
   # print(utc_time)
   #  before_date = datetime.fromtimestamp(current_timestamp) - timedelta(days=100)
   #  before_timestamp = str(int(before_date.timestamp()))
    limit = 2
    currency = "usd"
    token = "base"
    proxy_port = 50005  # 指定代理端口

    ohlcv_data = geck.get_token_history2(network, pool_address, timeframe, aggregate, before_timestamp, limit, currency, token, proxy_port)


    for data in ohlcv_data:
        print(data.time)
    print(ohlcv_data[0])

