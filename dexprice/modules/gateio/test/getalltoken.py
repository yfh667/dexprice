from __future__ import print_function
import dexprice.modules.cexdb.cexdb as  cexdb
import dexprice.modules.gateio.findalltoken as findtoken

import gate_api
from gate_api.exceptions import ApiException, GateApiException
import dexprice.modules.utilis.define as define

if __name__ == "__main__":
    # 配置 API 客户端
    configuration = gate_api.Configuration()
    api_client = gate_api.ApiClient(configuration)

    # 创建现货市场 API 实例
    api_instance = gate_api.SpotApi(api_client)
    # 获取所有交易对信息
    api_response = api_instance.list_currency_pairs()
    tokens = []
    try:
        # 获取所有交易对信息
        api_response = api_instance.list_currency_pairs()
        tokens = []
        for pair in api_response:
            print(f"交易对: {pair.id}, 基础币种: {pair.base}, 报价币种: {pair.quote}")
            if(pair.quote =='USDT'):
                token = define.CexTokenInfo(pair.base,'USDT')
                # token = define.CexTokenInfo(
                #     name="ETH",            # Token name (string)
                #     chainid="USD",     # Chain ID (string)
                #
                #
                # )
                tokens.append(token)
        if len(tokens) > 0:
            db_folder = '/home/yfh/Desktop/MarketSystem/Data/Project'   # 数据库存储文件夹
            db_name = "gateid"+'.db'  # 数据库文件名
            db = cexdb.CexSQLiteDatabase(db_folder, db_name)

            db.connect()
            db.insert_Multidata(   tokens)
            db.close()

    # print(token)
    ## print(len(token))
    # for pair in token:
    #     if pair == "MOBILE":
    #         print("we find")
    except GateApiException as ex:
        print(f"Gate API 异常，标签: {ex.label}, 信息: {ex.message}")
    except ApiException as e:
        print(f"调用 SpotApi->list_currency_pairs 时发生异常: {e}")
