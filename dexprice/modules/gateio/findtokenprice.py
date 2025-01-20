from __future__ import print_function
import gate_api
from gate_api.exceptions import ApiException, GateApiException

# 配置 API 客户端
configuration = gate_api.Configuration()
api_client = gate_api.ApiClient(configuration)

# 创建现货市场 API 实例
api_instance = gate_api.SpotApi(api_client)

# 指定交易对和时间间隔
currency_pair = "SOL_USDT"  # 交易对
interval = "1d"  # 时间间隔（1m, 5m, 15m, 30m, 1h, 4h, 1d 等）

try:
    # 获取K线数据
    api_response = api_instance.list_candlesticks(currency_pair=currency_pair, interval=interval)
    for candle in api_response:
        print(f"时间: {candle[0]}, 开盘价: {candle[5]}, 收盘价: {candle[2]}, 最低价: {candle[4]}, 最高价: {candle[3]}, 成交量: {candle[1]}")
except GateApiException as ex:
    print(f"Gate API 异常，标签: {ex.label}, 信息: {ex.message}")
except ApiException as e:
    print(f"调用 SpotApi->list_candlesticks 时发生异常: {e}")