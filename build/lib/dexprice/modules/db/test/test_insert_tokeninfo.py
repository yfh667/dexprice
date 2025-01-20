from dexprice.modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类
from dexprice.modules.utilis.define import Config,TokenInfo

from dexprice.modules.db.create_db import initialize_table
import dexprice.modules.db.insert_db as insert_db




# 示例使用
if __name__ == "__main__":
    manager = DexscreenApiManager()  # 实例化类

    chain_id = "ethereum"

    token = TokenInfo(
        address='0x3361f2DD00E31199F778f4b927f0Ed34C50E2a82',
        name='A Flying Cat',
        price_usd=5.004e-07,
        liquidity_usd=6600.93,
        fdv=4571.0,
        timestamp='2024-09-24 04:34:16',
        creattime='2024-08-13 16:56:59',
        pair_address='0x890210C48D46b379fd61B742CC482D4Cd0b6de46'
    )
    db_folder = '/home/yfh/Desktop/MarketSystem/Data'  # 数据库存储文件夹
    db_name = 'test.db'  # 数据库文件名
    table_name = 'token_pairs'  # 表名

    initialize_table(db_folder, db_name, table_name)

    db = insert_db.SQLiteDatabase(db_folder, db_name,chain_id)
    db.connect()


    db.insert_tokeninfo(table_name, token)

    # 关闭数据库连接
    db.close()



