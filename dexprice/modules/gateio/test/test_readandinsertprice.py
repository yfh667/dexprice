import  dexprice.modules.gateio.cexprice as gateprice
import  dexprice.modules.cexdb.cexdb as cexdb

import dexprice.modules.OHLCV.one_geck as one_geck
if __name__ == "__main__":


    db_folder = '/home/yfh/Desktop/MarketSystem/Data/Project'   # 数据库存储文件夹
    db_name = "test3"+'.db'  # 数据库文件名
    db = cexdb.CexSQLiteDatabase(db_folder, db_name)

    db.connect()
    # 创建一个 Tokendb 实例
    tokens = db.readdbtoken()
    # 打印实例属性



    current = []
    for token in tokens:
        current.append(token.name)
    ovhl_dataS = []
    for current in current:


        currency_pair = current+"_USDT"
        interval = "1d"  # 日线
        limit = 2       # 数据点数量
        end_timestamp = one_geck.datetime_to_timestamp(2024, 12, 7, 0, 0, 0, is_utc=True)

        proxy_port = 50057  # 本地代理端口

        # result = gateprice.get_cex_ohlcv_data(currency_pair, interval, limit, end_timestamp, proxy_port=proxy_port)

        ovhl_data =  gateprice.get_token_history2(currency_pair, interval, limit, end_timestamp, proxy_port=proxy_port)
        ovhl_dataS.extend(ovhl_data)

    token_price_history_list = db.collect_ovhl_data(ovhl_dataS)
    db.insert_multiple_price_history(token_price_history_list)


    db.close()