
import dexprice.modules.strategy.deadcoin as deadcoin
import importlib
importlib.reload(deadcoin)


import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import  dexprice.modules.utilis.define as define

import dexprice.modules.db.insert_db as insert_db


import dexprice.modules.db.multidb as multidb

import dexprice.modules.proxy.proxymultitheread as proxymultitheread
## use postql, we could neleget it
if __name__ == "__main__":

    chain_id = "solana"
    db_folder = '/home/yfh/Desktop/MarketSystem/Data/Project'   # 数据库存储文件夹
    db_name = "laobi"+'.db'  # 数据库文件名
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

    laobiaddress = []
    for history in tokenhistorys:
        if(len(history) > 0):
            if(deadcoin.deadallday(history)):

                token = db.read_token_withid(history[0].tokenid)
                laobiaddress.append(token.pair_address)
                print(f"we find  {token.pair_address}")
    chain_id = "solana"
    db_folder = '/home/yfh/Desktop/MarketSystem/Data/Project'   # 数据库存储文件夹
    db_name = "relaobi"+'.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name,chain_id)
    db.connect()
    startport = 50000
    clash_api_url = "http://127.0.0.1:9097"
    headers = {"Authorization": "Bearer 123"}
    proxys = proxymultitheread.get_one_ip_proxy_multithread(startport, clash_api_url, headers)
    dex_rate =5
    dex_capacity = 300
    dex_max_threads_per_proxy = 3
    task_manager = dexscreen_parrel.TaskManager(laobiaddress, define.Config.DEXS, chain_id, proxys, dex_rate, dex_capacity,dex_max_threads_per_proxy)
    tokensinfo, failed_tasks = task_manager.run()
    # tokenreal = []
    # for token in tokensinfo:
    #     if(tokenflitter.normal_token_filter(token,  criteria)):
    #         if(token.creattime =='1970-01-01 00:00:00'):
    #             pass
    #         else:
    #             tokenreal.append(token)

    db.insert_multiple_tokeninfo(tokensinfo)
