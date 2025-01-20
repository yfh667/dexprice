
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

import  modules.OHLCV.coinmarket as coinmarket  # 导入类
if __name__ == "__main__":
    chainid = "solana"



    db_folder = '/home/yfh/Desktop/mywork/pgp2/bestdex/DexPrice/Data'  # 数据库存储文件夹
    db_name = 'test.db'  # 数据库文件名
    table_name = 'token_pairs'  # 表名
    token_price_history = TokenPriceHistory(
        tokenid=1,  # 假设的 pairaddress
        open=0.0017923673797526785,
        high=0.0032208598195286723,
        low=0.0011617087366295115,
        close=0.003015783211998983,
        time="2024-09-14T00:00:00.000Z",  # "time_open" 对应的时间
        volume=1184394.0140152322
    )

    db = insert_db.SQLiteDatabase(db_folder, db_name,chainid)
    db.connect()
    db.insertpricehistory(token_price_history)
    db.close()

