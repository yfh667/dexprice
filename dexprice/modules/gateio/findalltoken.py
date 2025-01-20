from __future__ import print_function
import gate_api
from gate_api.exceptions import ApiException, GateApiException
import dexprice.modules.utilis.define as define
# 配置 API 客户端
configuration = gate_api.Configuration()
api_client = gate_api.ApiClient(configuration)

# 创建现货市场 API 实例
api_instance = gate_api.SpotApi(api_client)

try:
    # 获取所有交易对信息
    api_response = api_instance.list_currency_pairs()
    token = []
    for pair in api_response:
        print(f"交易对: {pair.id}, 基础币种: {pair.base}, 报价币种: {pair.quote}")
        token.append(pair.base)

   # print(token)
   ## print(len(token))
    # for pair in token:
    #     if pair == "MOBILE":
    #         print("we find")
except GateApiException as ex:
    print(f"Gate API 异常，标签: {ex.label}, 信息: {ex.message}")
except ApiException as e:
    print(f"调用 SpotApi->list_currency_pairs 时发生异常: {e}")