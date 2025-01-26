

import dexprice.modules.utilis.define as define
import dexprice.modules.db.insert_db as insert_db
import time
import dexprice.modules.db.multidb as multidb
import dexprice.modules.tg.tgbot as tgbot
import dexprice.modules.strategy.basefunction as  basefunction

import  dexprice.modules.pgpworker.senddb as senddb

def strategy(db_folder,db_name,send_dbname,Proxyport,sendflag=1):
 #   db_folder = '/home/yfh/Desktop/Data/Maindb'  # 数据库存储文件夹
  #  db_name =   'main.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    tokens = db.readdbtoken()
    ## 读取token的历史数据，进行处理
    db_path = db_folder + '/'  + 'main.db'
    requestedtokenid = []
    for token in tokens:
        requestedtokenid.append(token.tokenid)

    task_manager = multidb.DatabaseReadTaskManager(requestedtokenid, db_path, max_threads=5)
    results = task_manager.run()
    tokenhistorys = []
    # 处理结果
    for token_id, rows in results:
        tokenhistory = []
        for row in rows:
            test = define.TokenPriceHistory(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            tokenhistory.append(test)
        tokenhistorys.append(tokenhistory)
    find_address = []

    for tokenhistory in tokenhistorys:
        if (len(tokenhistory) > 1):
            tokenhistory = basefunction.sort_by_time(tokenhistory)

            if tokenhistory[-1].close > 0.8 * tokenhistory[0].open:
                ##here it is strategy
                tokenid = tokenhistory[0].tokenid
                tokendb = db.read_token_withid(tokenid)
                pairaddress = tokendb.pair_address
                strategyflag = 0

# here is the strategy
                for i in range(1, len(tokenhistory)):
                    token = tokenhistory[i]
                    if (token.high > 5 * token.low):
                        # 我么需要判断是涨还是跌
                        if (token.close > token.open):
# we find the token ,wo we need set the flag of the token
                            strategyflag = 1
                            break

                if(strategyflag == 1):
                    if (sendflag):
                        tgbot.sendmessage(pairaddress, Proxyport)

                    #  if(not senddb.havesend(db_folder,send_dbname,caaddress)):
                    # here we need insert the token that haven't sent to the send db
                    # in order to no duplicate in the send db
                    senddb.insertsenddb(db_folder, send_dbname, tokendb)
                    db.delete_token(pairaddress)
                    find_address.append(pairaddress)

    # 输出前的去重操作。
    unique_find_address = list(set(find_address))
    for address in unique_find_address:
        print(address)
    db.close()

