
import sys
import os


from modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类

from modules.utilis.define import Config,TokenInfo


from modules.utilis.define import Config,TokenInfo,TokenPriceHistory

from modules.db.create_db import initialize_table
import modules.db.insert_db as insert_db

from modules.PriceMonitor.multi_geck_dexscreen_api import Get_DEX_From_GECK  # 导入类
from modules.PriceMonitor.tokenflitter import liquid_token_filter,fdv_token_filter


from modules.OHLCV.coinmarket import fetch_historical_data  # 导入类

if __name__ == "__main__":
    chainid = "solana"



    db_folder = '/home/yfh/Desktop/MarketSystem/Data'  # 数据库存储文件夹
    db_name = 'test.db'  # 数据库文件名

    db = insert_db.SQLiteDatabase(db_folder, db_name,chainid)
    db.connect()

    token_new = db.readdbtoken()
    pair_addresses = []
    for token in token_new:
        pair_addresses.append(token.pair_address)
    print(pair_addresses)
    price_records = db.getpricedexscreen(2)
    print(price_records)

    db.close()






