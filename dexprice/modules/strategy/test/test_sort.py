import dexprice.modules.strategy.basefunction as basefunction

from dexprice.modules.utilis.define import FilterCriteria

import dexprice.modules.PriceMonitor.tokenflitter as tokenflitter

import dexprice.modules.proxy.proxymultitheread as proxymultitheread

import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel

import dexprice.modules.utilis.define as define
import dexprice.modules.proxy.proxydefine as proxydefine

#import dexprice.modules.db.insert_db as insert_db
import dexprice.modules.db.insert_db as insert_db

import dexprice.modules.proxy.clash_api as clash
import dexprice.modules.proxy.testproxy as testproxy
import os
import dexprice.modules.utilis.findroot as findroot
import time
import dexprice.modules.db.multidb as multidb
import dexprice.modules.tg.tgbot as tgbot
db_folder = '/home/yfh/Desktop/Data/Maindb'  # 数据库存储文件夹

db_name = 'main.db'  # 数据库文件名

db = insert_db.SQLiteDatabase(db_folder, db_name)
db.connect()
tokens = db.readdbtoken()

## 读取token的历史数据，进行处理
db_path = db_folder + '/' + 'main.db'
requestedtokenid = []
for token in tokens:
    requestedtokenid.append(token.tokenid)
db.delete_token(address)

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
        if tokenhistory[-1].close > 0.8 * tokenhistory[0].open:
            for i in range(1, len(tokenhistory)):
                #     for token in tokenhistory:
                token = tokenhistory[i]
                if (token.high > 5 * token.low):
                    # 我么需要判断是涨还是跌
                    if (token.close > token.open):
                        tokenid = tokenhistory[0].tokenid
                        tokendb = db.read_token_withid(tokenid)
                        pairaddress = tokendb.pair_address

                        find_address.append(pairaddress)
                #  print(pairaddress)

# 输出前的去重操作。
unique_find_address = list(set(find_address))
for address in unique_find_address:
    print(address)
db.close()
