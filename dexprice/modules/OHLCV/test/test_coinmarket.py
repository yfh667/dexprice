

import  modules.OHLCV.coinmarket as coinmarket  # 导入类

# def process_and_store_token_prices(data,tokenid):
#     token_prices = []
#
#     # 解析 quotes 数据
#     if 'data' in data and data['data']:
#         for quote_data in data['data'][0]['quotes']:
#             for quote_item in quote_data['quote']:
#                 # 从 quote_item 提取相关数据
#                 open_price = quote_item['open']
#                 high_price = quote_item['high']
#                 low_price = quote_item['low']
#                 close_price = quote_item['close']
#                 volume = quote_item['volume']
#                 time = quote_data['time_open']  # 使用 time_open 作为时间戳
#
#                 # 创建 TokenPriceHistory 对象
#                 token_price = TokenPriceHistory(
#                     tokenid=tokenid,
#                     open=open_price,
#                     high=high_price,
#                     low=low_price,
#                     close=close_price,
#                     time=time,
#                     volume=volume
#                 )
#
#                 # 将 TokenPriceHistory 对象添加到数组中
#                 token_prices.append(token_price)
#
#     return token_prices



if __name__ == "__main__":

    # solana,
    # params = {
    #     "contract_address": "HTmWEinSYg115BinCgHXuWAdQF8wKHEGfHH5C8nsYERJ",  # pairaddrss
    #     "network_slug": "solana",  # 网络标识符
    #     "time_period": "hourly",  # 数据的时间周期
    #     "time_start": "2024-07-28",  # 开始日期
    #     "time_end": "2024-07-30",  # 结束日期
    #     "interval": "4h",  # 数据的时间间隔
    # }

 #    params = {
 #        "contract_address": "22WrmyTj8x2TRVQen3fxxi2r4Rn6JDHWoMTpsSmn8RUd",  # 合约地址
 #        "network_slug": "solana",  # 网络标识符
 #        "time_period": "daily",  # 数据的时间周期
 #        "time_start": "2024-09-12",  # 开始日期
 #        "time_end": "2024-09-13",  # 结束日期
 #        "interval": "daily",  # 数据的时间间隔
 #    }
 #
 #
 #  #  api_key = "9a0342b8-00fa-4ef3-a6c0-89c06644f0f1"  # 替换为实际的 API 密钥
 #
 # #   data = fetch_historical_data(params, api_key)
 #
    pairaddress = "H2W2CeByodEEZG1BF4RVa7JWQosBGFmiibAxcAhNhtKA"
    chainid = "solana"
    time_start = "2024-09-10"
    time_end = "2024-09-12"
    api_key = "9a0342b8-00fa-4ef3-a6c0-89c06644f0f1"  # 替换为实际的 API 密钥
#9-10 to 9-14
    data = coinmarket.get_historical_data(pairaddress, chainid, time_start, time_end, api_key, time_period ="daily", interval="daily")
    if data:
        print(data)
    tokenid = 1
    tokenprice =  coinmarket.process_and_store_token_prices(data, tokenid)
    print(tokenprice)
    print(len(tokenprice))


