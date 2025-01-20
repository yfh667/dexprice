
import  dexprice.modules.gateio.cexprice as gateprice
import  dexprice.modules.cexdb.cexdb as cexdb
import  time
import dexprice.modules.OHLCV.one_geck as one_geck


import  dexprice.modules.utilis.define as define
import  dexprice.modules.gateio.queuefortoken as queuefortoken
import dexprice.modules.gateio.gateio_parrel2 as gateio_parrel2
import dexprice.modules.proxy.proxymultitheread as proxymultitheread


import  dexprice.modules.utilis.define as define
import pandas as pd

import dexprice.modules.db.insert_db as insert_db

import dexprice.modules.db.multidb    as multidb

db_folder = '/home/yfh/Desktop/MarketSystem/Data/Project'   # 数据库存储文件夹
db_name = "pnut"+'.db'  # 数据库文件名
chain_id = "solana"
db = insert_db.SQLiteDatabase(db_folder, db_name,chain_id)
db.connect()

tokens = db.readdbtoken()
requestedtokenid = []
for token in tokens:
    requestedtokenid.append(token.tokenid)

db_path = db_folder+'/'+db_name
task_manager = multidb.DatabaseReadTaskManager(requestedtokenid, db_path,  chain_id,max_threads=5)
results = task_manager.run()
tokenhistorys = []
# 处理结果
for token_id, rows in results:
    tokenhistory=[]
    for row in rows:
        test = define.TokenPriceHistory(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
        tokenhistory.append(test)
    tokenhistorys.append(tokenhistory)
rawdata = tokenhistorys[0]
print(rawdata)
import importlib
import dexprice.modules.strategy.normal as normal
import dexprice.modules.strategy.monotonic as monotonic

# 对模块重新加载
importlib.reload(normal)
dates, opens, highs, lows, closes = normal.checknormalgui(rawdata)
import  dexprice.modules.dearpygui.gui as  pygui
pygui.show_chart_rectangle(dates,opens,highs,lows,closes,normal.find_monotonic)