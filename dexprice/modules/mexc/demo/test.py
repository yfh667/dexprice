import dexprice.modules.mexc.getalltoken as getalltoken
import dexprice.modules.cexdb.cexdb as cexdb

import dexprice.modules.utilis.define as define
import os
import dexprice.modules.utilis.findroot as findroot
import dexprice.modules.mexc.initial_timesta as initial_timesta
import dexprice.modules.mexc.initial_timesta_parall as initial_timesta_parall
import dexprice.modules.proxy.proxymultitheread as proxymultitheread
import dexprice.modules.utilis.timedefine as timedefine
from dexprice.three import creattime
import dexprice.modules.OHLCV.one_geck as one_geck
import dexprice.modules.mexc.mexc_queue as mexc_queue
import dexprice.modules.mexc.mexcovhl_parall as mexcovhl_parall

import dexprice.modules.cexdb.multidb    as multidb
# 假设您的数据库路径为 'your_database.db'
#db_path = '/home/yfh/Desktop/MarketSystem/Data/Project/test4.db'
import dexprice.modules.strategy.basefunction as basefunction
current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = findroot.find_project_root(current_dir)
DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

db_folder = DATA_FOLDER + '/cex'  # 数据库存储文件夹
db_mubiao_name = "myspot" + '.db'

db_path = db_folder+"/"+db_mubiao_name

# 需要读取的 token_id 列表
#token_ids = [19 ]

db = cexdb.CexSQLiteDatabase(db_folder, db_mubiao_name)

db.connect()


tokens =db.readdbtoken()

token_ids = []
for token in tokens:
    token_ids.append(token.tokenid)

task_manager = multidb.CexDatabaseReadTaskManager(token_ids, db_path,  max_threads=5)
results = task_manager.run()

# 处理结果
tokenhistorys = []
for token_id, rows in results:
        tokenhistory = []
        for row in rows:
            test = define.CexTokenPriceHistory(row[1], row[2], row[3], row[4], row[5], row[6], row[7],row[8])
            tokenhistory.append(test)
        tokenhistorys.append(tokenhistory)

# print(tokenhistorys)
for tokenhistory in tokenhistorys:

    tokenhistory = basefunction.sort_by_time(tokenhistory)
    last = tokenhistory[ - 1]
    first = tokenhistory[0]
    if(first.close<last.close):
        if(last.amount>200000):
         tokenid = tokenhistory[0].tokenid
         token = db.read_token_withid(tokenid)
         tokenname = token.name
         print(f"we find{tokenname}")

    # dates, opens, highs, lows, closes = normal.checknormalgui(tokenhistory)
    # if (star1.monotonic_intervals(dates, opens, highs, lows, closes)):
    #     #   print( f"we find{tokenhistory[0].tokenid}")
    #     if (db.read_token_withid(tokenhistory[0].tokenid)):
    #         print(f"we find  {db.read_token_withid(tokenhistory[0].tokenid).pair_address}")
    #
    #
    # else:
    #     pass
