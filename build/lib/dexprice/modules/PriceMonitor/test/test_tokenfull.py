
from modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类

from modules.utilis.define import Config,TokenInfo,Tokendb


import  modules.OHLCV.coinmarket as coinmarket  # 导入类


import  modules.utilis.time as time  # 导入类

from modules.db.create_db import initialize_table
import modules.db.insert_db as insert_db

from modules.PriceMonitor.multi_geck_dexscreen_api import Get_DEX_From_GECK  # 导入类
from modules.db.readjson import extract_chain_and_ca,read_json_file,gettokenca
from modules.PriceMonitor.tokenflitter import liquid_token_filter,fdv_token_filter



# def get_token_price_history(token_db_entry, chain_id, days_in_past, api_key):
#     """
#     获取给定 token 的价格历史数据并返回处理后的结果
#     :param token_db_entry: Tokendb 类的实例，包含 token 的数据库信息
#     :param chain_id: 区块链 ID
#     :param days_in_past: 获取多少天前的历史数据
#     :param api_key: 用于调用 API 的密钥
#     :return: 处理后的 token 价格数据
#     """
#     pair_address = token_db_entry.pair_address
#
#     # 获取时间区间
#     start_date = time.get_past_utc_date(days_in_past)
#     end_date = time.get_current_utc_date()
#
#     print(f"Time range: {start_date} to {end_date}")
#
#     # 如果 token 的创建时间比 start_date 更早，调整 start_date 为创建时间
#     if time.compare_utc_dates(start_date, token_db_entry.creattime):
#         start_date = token_db_entry.creattime
#
#     # 调用 coinmarket API 获取历史数据
#     historical_data = coinmarket.get_historical_data(
#         pair_address, chain_id, start_date, end_date, api_key, time_period="daily", interval="daily"
#     )
#
#     # 使用 token ID 处理和存储 token 的价格数据
#     token_id = token_db_entry.tokenid
#     token_price_history = coinmarket.process_and_store_token_prices(historical_data, token_id)
#
#     return token_price_history
from tqdm import tqdm  # 导入 tqdm
# 示例使用
if __name__ == "__main__":

    api_key = "9a0342b8-00fa-4ef3-a6c0-89c06644f0f1"  # 替换为实际的 API 密钥

    manager = DexscreenApiManager()  # 实例化类
    #ethereum
    chain_id = "solana"
    pair_addresses = ["1", "5hiAEegopPSpRZxmYdoJSgAc4d9T2kxN4XtFPrRJ7xjZ", " 8UC6pXr236qGcGVA6oYL8ZioJGVC5YBFHUK7ez95e1Z1 ", "1"]  # 示例地址








    #2. we need call dex api to get the tokeninfo
    num_threads = 3
    proxy_ports = [30002, 30001,30003]

    rate = 5  # 每秒生成的令牌数
    capacity = 300  # 令牌桶的最大容量
    # 调用类的方法，使用 Config.GECK 替代硬编码的 GECK
    results = manager.multi_get_token_dexscreen(Config.DEXS, pair_addresses, chain_id, num_threads, proxy_ports,5,300)
    #  print("All results:", results)
    # 使用列表解析展开嵌套列表
    flattened_results = [token for sublist in results for token in sublist]

    #3.we need set the scale for fdv liquid etc.

    tokens=[]

    for results1 in flattened_results:
        if liquid_token_filter(results1) and fdv_token_filter(results1):
            print(results1)
            tokens.append(results1)
        else:
            pass
    #print(tokens)

    #4.we write to the db









    db_folder = '/home/yfh/Desktop/mywork/pgp2/bestdex/DexPrice/Data'  # 数据库存储文件夹
    db_name = 'test.db'  # 数据库文件名




    db = insert_db.SQLiteDatabase(db_folder, db_name,chain_id)
    db.connect()


    db.insert_multiple_tokeninfo(tokens)
    token_new = db.readdbtoken()
    print(token_new)
   # print(token_new[0])
   #  tokenprice = coinmarket.get_multi_token_price_history(token_new,chain_id,2,api_key)
   #  print(tokenprice)
   #  for token in tokenprice:
   #    db.insertpricehistory(token)

    for tokes in tqdm(token_new, desc="Fetching token price history", unit="token"):
        tokenprice = coinmarket.get_token_price_history(tokes, chain_id, 6, api_key)
        print(tokenprice)
        for price in tokenprice:
          db.insertpricehistory(price)
    # 关闭数据库连接
    db.close()



