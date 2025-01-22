
import dexprice.modules.db.insert_db as insert_db
import dexprice.modules.allmodules.realtoken as realtoken

from dexprice.modules.utilis.define import FilterCriteria

def write_maindb(token_new,db_folder_main,db_name_main):
    criteria = FilterCriteria(
        liquidity_usd_min=10000,
        liquidity_usd_max=None,
        fdv_min=10000,
        fdv_max=None,
        pair_age_min_hours=None,
        pair_age_max_hours= None,
        txn_buy=10,
        txn_sell=10,
        volume=10000
       )
  # 添加地址到对应链的列表
    tokenreal = realtoken.extract_valid_tokens(token_new,criteria)

  #  db_folder_main = '/home/yfh/Desktop/Data/Maindb'  # 数据库存储文件夹
  #  db_name_main = "main" + '.db'  # 数据库文件名
    db_main = insert_db.SQLiteDatabase(db_folder_main, db_name_main)
    db_main.connect()
    db_main.insert_multiple_tokeninfo(tokenreal)
    db_main.close()
