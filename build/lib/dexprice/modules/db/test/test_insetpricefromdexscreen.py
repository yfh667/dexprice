
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
    token_info = TokenInfo(
        address="9SbDeAhHt1TjPNwhg8de88jhstymAn4A4KPDzdJvpump",
        name="OPENAI MASCOT",
        price_usd=0.0007145,
        liquidity_usd=131992.33,
        fdv=714560.0,
        timestamp="2024-11-02 03:31:41",
        pair_address="6GKPhrJ9sRS6obiXhq66rgfSPS6vtUJxZCMnuuBX581w",
        creattime="2024-10-31 18:33:01"
    )

    tokens =[]
    tokens.append(token_info)
    db = insert_db.SQLiteDatabase(db_folder, db_name,chainid)
    db.connect()
    db.insert_multiple_tokeninfo(tokens)
    token_new = db.readdbtoken()
    pair_addresses = []
    for token in token_new:
        pair_addresses.append(token.pair_address)
    print(pair_addresses)
    manager = DexscreenApiManager()  # 实例化类
    num_threads = 1

    proxy_ports = [30002]

    rate = 5  # 每秒生成的令牌数
    capacity = 300  # 令牌桶的最大容量

    results = manager.multi_get_token_dexscreen(Config.DEXS, pair_addresses, chainid, num_threads, proxy_ports,rate,capacity)
    flattened_results = [token for sublist in results for token in sublist]
    print(flattened_results)
    db.insertMultipricedexscreen(flattened_results)



