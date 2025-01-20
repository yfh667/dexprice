from typing import Optional, List, Tuple
from datetime import datetime, timedelta, timezone
import math
import  dexprice.modules.OHLCV.geck as geck
from typing import Optional, List, Tuple
from datetime import datetime, timedelta, timezone
import math
import dexprice.modules.OHLCV.one_geck as one_geck
import dexprice.modules.OHLCV.geck_parrel2 as geck_parrel2
pool_address = ['6rvir3c4H9cvMxtz38aG9TJPgH1sDUiGpUnupiHituVs']

# 生成开始和结束时间的时间戳
start_timestamp = one_geck.datetime_to_timestamp(2024, 9, 10, 0, 0, 0, is_utc=True)
end_timestamp = one_geck.datetime_to_timestamp(2024, 9, 22, 0, 0, 0, is_utc=True)
kline = 'minute'
aggregate = '15'
currency = "usd"
token = 'base'
proxy_port = 50005  # 指定代理端口
queue = one_geck.create_request_queue(pool_address, start_timestamp, end_timestamp, kline, aggregate)

ohlcv_data = geck.get_token_history2("solana", queue[0].pool_address, kline, aggregate, queue[0].before_timestamp, queue[0].limit, currency, token, proxy_port)

# ohlcv_data2 = geck.get_token_history2("solana", pool_address, kline, aggregate, queue[1][3], queue[1][4], currency, token, proxy_port)
# print(ohlcv_data2)
for params in queue:
    print(params)

print(ohlcv_data)
# 创建 RequestParams 实例
