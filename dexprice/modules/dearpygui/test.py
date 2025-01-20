import dexprice.modules.utilis.timedefine as transtime
from  dexprice.modules.utilis.define import  TokenPriceHistory
# 假设 rawdata 是 TokenPriceHistory 的列表
rawdata = [
    TokenPriceHistory(tokenid=1, open=0.0507614233705504, high=0.0569042942842257, low=0.0482630834099417, close=0.0508182150557618, time="2022-01-01 00:00:00",volume=2325599),
    TokenPriceHistory(tokenid=1, open=0.0523614233705504, high=0.0589042942842257, low=0.0502630834099417, close=0.0558182150557618, time="2022-01-02 00:00:00",volume=2325599),
    # 添加更多数据...
]

# 初始化空列表
dates = []
opens = []
highs = []
lows = []
closes = []

# 将 rawdata 转换为所需格式
for record in rawdata:
    timestamp = transtime.datetime_to_timestamp(record.time)  # 转换时间为时间戳
    dates.append(timestamp)
    opens.append(record.open)
    highs.append(record.high)
    lows.append(record.low)
    closes.append(record.close)

# 打印结果
print("dates =", dates)
print("opens =", opens)
print("highs =", highs)
print("lows =", lows)
print("closes =", closes)