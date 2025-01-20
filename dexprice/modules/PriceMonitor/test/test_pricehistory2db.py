
import sys
import os


from modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类

from modules.utilis.define import Config,TokenInfo



from modules.db.create_db import initialize_table
import modules.db.insert_db as insert_db

from modules.PriceMonitor.multi_geck_dexscreen_api import Get_DEX_From_GECK  # 导入类
from modules.db.readjson import extract_chain_and_ca,read_json_file,gettokenca
from modules.PriceMonitor.tokenflitter import liquid_token_filter,fdv_token_filter


from modules.OHLCV.coinmarket import fetch_historical_data  # 导入类

import  modules.OHLCV.coinmarket as coinmarket  # 导入类


import sys
import os


from modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类

from modules.utilis.define import Config,TokenInfo,TokenPriceHistory



from modules.db.create_db import initialize_table
import modules.db.insert_db as insert_db

from modules.PriceMonitor.multi_geck_dexscreen_api import Get_DEX_From_GECK  # 导入类
from modules.db.readjson import extract_chain_and_ca,read_json_file,gettokenca
from modules.PriceMonitor.tokenflitter import liquid_token_filter,fdv_token_filter


from modules.OHLCV.coinmarket import fetch_historical_data  # 导入类

import  modules.OHLCV.coinmarket as coinmarket  # 导入类



if __name__ == "__main__":


    pairaddress = "22WrmyTj8x2TRVQen3fxxi2r4Rn6JDHWoMTpsSmn8RUd"
    chainid = "solana"
    time_start = "2024-09-12"
    time_end = "2024-09-13"
    api_key = "9a0342b8-00fa-4ef3-a6c0-89c06644f0f1"  # 替换为实际的 API 密钥

    data = coinmarket.get_historical_data(pairaddress, chainid, time_start, time_end, api_key, time_period ="daily", interval="daily")
    if data:
        print(data)
    tokenid = 1
    tokenprice =  coinmarket.process_and_store_token_prices(data, tokenid)
    # print(tokenprice)




    db_folder = '/home/yfh/Desktop/mywork/pgp2/bestdex/DexPrice/Data'  # 数据库存储文件夹
    db_name = 'test.db'  # 数据库文件名


    db = insert_db.SQLiteDatabase(db_folder, db_name,chainid)
    db.connect()
    for token in tokenprice:
         db.insertpricehistory(token)
    db.close()
