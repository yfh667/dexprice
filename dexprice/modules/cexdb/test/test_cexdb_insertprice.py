import  dexprice.modules.cexdb.cexdb as cexdb

import  dexprice.modules.utilis.define as define
db_folder = '/home/yfh/Desktop/MarketSystem/Data/Project'   # 数据库存储文件夹
db_name = "mytest2"+'.db'  # 数据库文件名
db = cexdb.CexSQLiteDatabase(db_folder, db_name)

db.connect()
ovhl_data = [
    define.OvhlFromCex(
        name="ETH",
        open=0.002831,
        high=0.003496,
        low=0.00274,
        close=0.00274,
        time="2024-12-05 00:00:00",
        volume=593483.30000000
    )
]
token_price_history_list = db.collect_ovhl_data(ovhl_data)
db.insert_multiple_price_history(token_price_history_list)
# 打印实例属性

db.close()