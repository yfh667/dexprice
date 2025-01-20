# Database configuration dictionary
from dexprice.modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类
from dexprice.modules.utilis.define import Config,TokenInfo
import  dexprice.modules.utilis.define as define
from dexprice.modules.db.create_db import initialize_table
import dexprice.modules.db.insert_db as insert_db
import dexprice.modules.allmodules.geckpricehistory as geckpricehistory
import dexprice.modules.db.postsql as postsql
db_config = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'solana10days',
    'user': 'yfh',
    'password': 'yfh'
}

# Initialize the PostgreSQLDatabase instance
chainid = 'solana'
db = postsql.PostgreSQLDatabase(db_config, chainid)
token = TokenInfo(
    address='0x3361f2DD00E31199F778f4b927f0Ed34C50E2a82',
    name='A Flying Cat',
    price_usd=5.004e-07,
    liquidity_usd=6600.93,
    fdv=4571.0,
    timestamp='2024-09-24 04:34:16',
    creattime='2024-08-13 16:56:59',
    pair_address='0x890210C48D46b379fd61B742CC482D4Cd0b6de46'
)
token_price_history = define.OvhlFromDex(
    pairaddress='0x890210C48D46b379fd61B742CC482D4Cd0b6de46',  # 假设的 pairaddress
    open=0.0017923673797526785,
    high=0.0032208598195286723,
    low=0.0011617087366295115,
    close=0.003015783211998983,
    time="2024-09-14T00:00:00.000Z",  # "time_open" 对应的时间
    volume=1184394.0140152322
)

tokens = []
tokens.append(token)

# Connect to the database
db.connect()
# db.insert_multiple_tokeninfo(tokens)
# t = db.readdbtoken()
token_price_historys = []
token_price_historys.append(token_price_history)



token_price_history_list = db.collect_ovhl_data(token_price_historys)
# 批量插入数据
db.insert_multiple_price_history(token_price_history_list)


# Now you can use db to call the methods like insert_data, insertpricehistory, etc.

# Don't forget to close the connection when done
db.close()
