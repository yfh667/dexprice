import dexprice.modules.allmodules.geckpricehistory as geckpricehistory
import dexprice.modules.db.insert_db as insert_db
import dexprice.modules.utilis.define as define

import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import dexprice.modules.utilis.define as define
import  dexprice.modules.utilis.define as define
import dexprice.modules.proxy.proxydefine as proxydefine
import dexprice.modules.allmodules.writedb as writedb
import dexprice.modules.db.insert_db as insert_db
import dexprice.modules.db.multidb as multidb
import dexprice.modules.strategy.strategy1 as strategy1
import dexprice.modules.proxy.clash_api as clash
import dexprice.modules.proxy.testproxy as testproxy
import dexprice.modules.OHLCV.geck_parrel as geck_parrel
import time
import time
from datetime import datetime, timedelta
if __name__ == "__main__":
    chain_id = "solana"
    db_folder = '/home/yfh/Desktop/MarketSystem/Data/Project'   # 数据库存储文件夹
    db_name = "10days"+'.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name,chain_id)
    db.connect()
    tokens = db.readdbtoken()
    requestedtokenid = []
    for token in tokens:
        requestedtokenid.append(token.tokenid)

    db_path = db_folder+'/'+db_name
    task_manager = multidb.DatabaseReadTaskManager(requestedtokenid,  db_path,chain_id, max_threads=6)
    results = task_manager.run()
    tokenhistorys = []
    # 处理结果
    for token_id, rows in results:
        tokenhistory=[]
        for row in rows:
            test = define.TokenPriceHistory(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            tokenhistory.append(test)
        tokenhistorys.append(tokenhistory)


    for history in tokenhistorys:
        if(strategy1.find_no_less_time(history)):

            token = db.read_token_withid(history[0].tokenid)
            print(f"we find  {token.pair_address}")



    db.close()
