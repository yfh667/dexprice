from __future__ import print_function
import gate_api
from gate_api.exceptions import ApiException, GateApiException

# 配置代理
configuration = gate_api.Configuration()
configuration.host = "https://api.gateio.ws/api/v4"
configuration.proxy = "http://127.0.0.1:7897"  # 设置代理地址

# 创建 API 客户端
api_client = gate_api.ApiClient(configuration)

# 创建现货市场 API 实例
api_instance = gate_api.SpotApi(api_client)

# 设置交易对和时间间隔
currency_pair = "BTC_USDT"
interval = "1m"

try:
    # 通过代理获取 K 线数据
    api_response = api_instance.list_candlesticks(currency_pair=currency_pair, interval=interval)
    for candlestick in api_response:
        print(f"时间: {candlestick[0]}, 开盘价: {candlestick[5]}, 收盘价: {candlestick[2]}")
except GateApiException as ex:
    print(f"Gate API Exception, label: {ex.label}, message: {ex.message}")
except ApiException as e:
    print(f"Exception when calling SpotApi->list_candlesticks: {e}")