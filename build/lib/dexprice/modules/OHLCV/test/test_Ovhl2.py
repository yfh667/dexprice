import modules.OHLCV.OvhlRawPriceToOvhl as OvhlRawPriceToOvhl
from modules.utilis.define import OvhlRawPrice
import modules.db.insert_db as insert_db

if __name__ == '__main__':
    db_folder = '/home/yfh/Desktop/MarketSystem/Data'  # 数据库存储文件夹
    db_name = 'test2.db'  # 数据库文件名
    chainid = "solana"
    db = insert_db.SQLiteDatabase(db_folder, db_name,chainid)
    db.connect()
    token_new = db.readdbtoken()
    #print(token_new)
    # we turn the dexscreen data to ovhl
    OvhlRawPriceToOvhl.process_and_store_price_data(token_new, db, interval='15min')



#