from dexprice.modules.utilis.define import Config,TokenInfo

import dexprice.modules.db.insert_db_linshi as insert_db

import os
import  dexprice.modules.utilis.findroot as findroot


# 示例使用
if __name__ == "__main__":



    token = TokenInfo(
        chainid='solana',
        address='0x3361f2DD00E31199F778f4b927f0Ed34C50E2a82',
        name='A Flying Cat',
        price_usd=5.004e-07,
        liquidity_usd=6600.93,
        fdv=4571.0,
        timestamp='2024-09-24 04:34:16',
        creattime='2024-08-13 16:56:59',
        pair_address='0x890210C48D46b379fd61B742CC482D4Cd0b6de46'
    )

    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = findroot.find_project_root(current_dir)
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

    db_folder = DATA_FOLDER +'/Project'# 数据库存储文件夹
    db_name = 'test32.db'  # 数据库文件名
    table_name = 'token_pairs'  # 表名



    db = insert_db.SQLiteDatabase_linshi(db_folder, db_name)



    db.connect()


    db.insert_tokeninfo(table_name, token)

    # 关闭数据库连接
    db.close()



