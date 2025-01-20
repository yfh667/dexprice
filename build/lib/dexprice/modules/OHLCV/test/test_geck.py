
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
    network = "solana"
    pool_address = ['94hPh9VpNFqaizTHptX9GxPmfYGCtDixvE7iwqz9CtYh']
    timeframe = "day"  # 可选值: day, hour, minute
    aggregate = "1"     # 聚合时间段
    current_timestamp = int(time.time())
   # before_timestamp = str(current_timestamp)  # 可选的时间戳参数
    before_date = datetime.fromtimestamp(current_timestamp) - timedelta(days=100)
    before_timestamp = str(int(before_date.timestamp()))
    limit = 100
    currency = "usd"
    token = 'base'
    proxy_port = 50005  # 指定代理端口

    ohlcv_data = geck.get_token_history2(network, pool_address, timeframe, aggregate, before_timestamp, limit, currency, token, proxy_port)


    for data in ohlcv_data:
        print(data.time)
    print(ohlcv_data)

