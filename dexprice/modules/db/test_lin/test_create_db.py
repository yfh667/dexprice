# 示例使用

import sys
import os

import dexprice.modules.utilis.findroot as findroot
import dexprice.modules.db.insert_db_linshi as insert_db
if __name__ == "__main__":
    # db_folder = '/home/yfh/Desktop/mywork/pgp2/bestdex/DexPrice/Data'  # 数据库存储文件夹
    # db_name = 'crypto_data.db'  # 数据库文件名
    # table_name = 'token_pairs'  # 表名
    #
    # initialize_table(db_folder, db_name, table_name)
    dbname = 'createnew'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = findroot.find_project_root(current_dir)
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")
    db_folder2 = DATA_FOLDER+'/Project'  # 数据库存储文件夹
    db_name2 = dbname+'.db'  # 数据库文件名



    db = insert_db.SQLiteDatabase_linshi(db_folder2, db_name2)
    db.delete_table2()
    db.connect()
