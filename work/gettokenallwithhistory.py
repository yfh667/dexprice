
from modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类

from modules.utilis.define import Config,TokenInfo
from tqdm import tqdm  # 导入 tqdm



from modules.db.create_db import initialize_table
import modules.db.insert_db as insert_db

from modules.PriceMonitor.multi_geck_dexscreen_api import Get_DEX_From_GECK  # 导入类
from modules.db.readjson import extract_chain_and_ca,read_json_file,gettokenca
from modules.PriceMonitor.tokenflitter import liquid_token_filter,fdv_token_filter

import modules.db.readjson as readjson


import  modules.OHLCV.coinmarket as coinmarket  # 导入类
# 示例使用
if __name__ == "__main__":

    api_key = "9a0342b8-00fa-4ef3-a6c0-89c06644f0f1"  # 替换为实际的 API 密钥
#     manager = DexscreenApiManager()  # 实例化类
#     #ethereum
    chain_id = "solana"



    db_folder = '/home/yfh/Desktop/mywork/pgp2/bestdex/DexPrice/Data'  # 数据库存储文件夹
    db_name = 'solana_db.db'  # 数据库文件名




    db = insert_db.SQLiteDatabase(db_folder, db_name,chain_id)
    db.connect()


#    db.insert_multiple_tokeninfo(  tokens)
    token_new = db.readdbtoken()
    print(token_new)

    for tokes in tqdm(token_new, desc="Fetching token price history", unit="token"):
        tokenprice = coinmarket.get_token_price_history(tokes, chain_id, 6, api_key)
       # print(tokenprice)
        for price in tokenprice:
            db.insertpricehistory(price)

    # 关闭数据库连接
    db.close()




