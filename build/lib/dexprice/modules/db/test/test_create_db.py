# 示例使用

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from create_db import initialize_table
import modules.db.insert_db as insert_db
if __name__ == "__main__":
    # db_folder = '/home/yfh/Desktop/mywork/pgp2/bestdex/DexPrice/Data'  # 数据库存储文件夹
    # db_name = 'crypto_data.db'  # 数据库文件名
    # table_name = 'token_pairs'  # 表名
    #
    # initialize_table(db_folder, db_name, table_name)
    dbname = 'test'
    chainid ='slana'
    db_folder2 = '/home/yfh/Desktop/MarketSystem/Data/Project'  # 数据库存储文件夹
    db_name2 = dbname+'.db'  # 数据库文件名



    db = insert_db.SQLiteDatabase(db_folder2, db_name2,chainid)
    db.delete_table2()
    db.connect()
