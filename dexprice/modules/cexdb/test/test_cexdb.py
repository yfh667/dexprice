import  dexprice.modules.cexdb.cexdb as cexdb

import  dexprice.modules.utilis.define as define
import os
import dexprice.modules.utilis.findroot as findroot
current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = findroot.find_project_root(current_dir)
DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")


db_folder =DATA_FOLDER+ '/cex'   # 数据库存储文件夹
db_name = "mytest2"+'.db'  # 数据库文件名
db = cexdb.CexSQLiteDatabase(db_folder, db_name)

db.connect()
# 创建一个 Tokendb 实例
token = define.CexTokenInfo(
    name="ETH",            # Token name (string)
     chainid="USD",     # Chain ID (string)

)


tokens = []
tokens.append(token)
db.insert_Multidata(  tokens)
# 打印实例属性

db.close()