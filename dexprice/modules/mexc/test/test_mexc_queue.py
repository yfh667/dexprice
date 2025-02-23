from datetime import datetime, timezone
from datetime import datetime, timedelta, timezone
import math
import dexprice.modules.OHLCV.one_geck as one_geck
import dexprice.modules.mexc.mexc_queue as mexc_queue
symbol= 'BTC_USDT'
# 生成开始和结束时间的时间戳
start_timestamp = one_geck.datetime_to_timestamp(2025, 2, 20, 0, 0, 0, is_utc=True)
end_timestamp = one_geck.datetime_to_timestamp(2025, 2, 20, 3, 0, 0, is_utc=True)

kline = 'Min'
aggregate = '60'


queue = mexc_queue.mexc_create_request_queue(symbol, start_timestamp, end_timestamp, kline, aggregate)
print(queue)