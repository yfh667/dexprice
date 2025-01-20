
import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import dexprice.modules.utilis.define as define
import  dexprice.modules.utilis.define as define
import dexprice.modules.proxy.proxydefine as proxydefine
import dexprice.modules.allmodules.writedb as writedb
import dexprice.modules.db.insert_db as insert_db
import dexprice.modules.proxy.clash_api as clash
import dexprice.modules.proxy.testproxy as testproxy
import dexprice.modules.OHLCV.geck_parrel as geck_parrel
import time
import time
from datetime import datetime, timedelta
import dexprice.modules.proxy.proxymultitheread as proxymultitheread

import dexprice.modules.db.multidb   as multidb
import dexprice.modules.strategy.normal as normal

def main():



    chain_id = "base"
    db_folder = '/home/yfh/Desktop/MarketSystem/Data/Project'   # 数据库存储文件夹
    db_name = "basetoken"+'.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name,chain_id)
    db.connect()
    tokens = db.readdbtoken()
    token_ids = []
    for token in tokens:
        token_ids.append( token.tokenid)

    # 假设您的数据库路径为 'your_database.db'
    db_path =  db_folder+'/'+db_name
    # 需要读取的 token_id 列表




    task_manager = multidb.DatabaseReadTaskManager(token_ids,  db_path,chain_id, max_threads=6)
    results = task_manager.run()
    tokenhistorys = []
    # 处理结果
    for token_id, rows in results:
        tokenhistory=[]
        for row in rows:
            test = define.TokenPriceHistory(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            tokenhistory.append(test)
        tokenhistorys.append(tokenhistory)

    for tokenhistory in tokenhistorys:
        if(len(tokenhistory)>1):
            if normal.checknormal(tokenhistory):

                tokendb = db.read_token_withid(tokenhistory[0].tokenid)
                if(tokendb):
                 print(f"the id is { tokendb.pair_address}")

    db.close()


if __name__ == "__main__":
    main()



