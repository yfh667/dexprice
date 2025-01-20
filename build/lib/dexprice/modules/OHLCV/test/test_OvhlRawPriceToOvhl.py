import modules.OHLCV.OvhlRawPriceToOvhl as OvhlRawPriceToOvhl
from modules.utilis.define import OvhlRawPrice
import modules.db.insert_db as insert_db

if __name__ == '__main__':
    # data = [
    #     (2, 0.0007101, '2024-11-02 03:33:44'),
    #     (2, 0.0007101, '2024-11-02 03:34:46'),
    #     (2, 0.0007141, '2024-11-02 03:36:37')
    # ]

    db_folder = '/home/yfh/Desktop/MarketSystem/Data'  # 数据库存储文件夹
    db_name = 'test.db'  # 数据库文件名
    chainid = "solana"
    db = insert_db.SQLiteDatabase(db_folder, db_name,chainid)
    db.connect()
    token_new = db.readdbtoken()
    data = db.getpricedexscreen(2)
    # data = [
    #     (2, 0.0007101, '2024-11-02 03:33:44'),
    #     (2, 0.0007101, '2024-11-02 03:34:46'),
    #     (2, 0.0007141, '2024-11-02 03:36:37')
    # ]

 #   print(price_records)


# 初始化为 OvhlRawPrice 对象列表
    price_records = [OvhlRawPrice(tokenid, price, time) for tokenid, price, time in data]
    print(price_records)
    ohlc_data = OvhlRawPriceToOvhl.PriceIntoOvhl(price_records,'15min')
    for ohlc in ohlc_data:
        print(ohlc)


