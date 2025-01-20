import schedule
import modules.OHLCV.OvhlRawPriceToOvhl as OvhlRawPriceToOvhl

import time
from dexprice.modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager
from modules.utilis.define import Config, TokenInfo, Tokendb
import modules.OHLCV.coinmarket as coinmarket
import modules.utilis.time as mytime
from modules.db.create_db import initialize_table
import modules.db.insert_db as insert_db
import modules.tg.tgbot as tgbot
from modules.PriceMonitor.multi_geck_dexscreen_api import Get_DEX_From_GECK
from modules.PriceMonitor.tokenflitter import liquid_token_filter, fdv_token_filter
from tqdm import tqdm

def fetch_and_store_data():
    results = manager.multi_get_token_dexscreen(Config.DEXS, pair_addresses, chain_id, num_threads, proxy_ports, rate, capacity)
    flattened_results = [token for sublist in results for token in sublist]
    db.insertMultipricedexscreen(flattened_results)
    print("Price data stored.")

def process_ohlc_data():
    # 获取数据库中的最新 token 数据
    token_new = db.readdbtoken()
    OvhlRawPriceToOvhl.process_and_store_price_data(token_new, db, interval)
    print(f"Processed OHLC data for interval: {interval}")

if __name__ == "__main__":
    chain_id = "solana"
    db_folder = '/home/yfh/Desktop/MarketSystem/Data'
    db_name = 'test2.db'
    db = insert_db.SQLiteDatabase(db_folder, db_name, chain_id)
    db.connect()

    manager = DexscreenApiManager()
    token_new = db.readdbtoken()
    pair_addresses = [token.pair_address for token in token_new]
    num_threads = 1
    proxy_ports = [30001]
    rate = 5
    capacity = 300
    interval = '15min'

    # 设置定期任务，每隔 10 秒获取价格数据并存入数据库
    schedule.every(10).seconds.do(fetch_and_store_data)

    # 设置定期任务，按照 interval 时间间隔转换并存储 OHLC 数据
    schedule.every(15).minutes.do(process_ohlc_data)

    while True:
        # 执行计划的任务
        schedule.run_pending()
        time.sleep(1)  # 减少 CPU 占用率
