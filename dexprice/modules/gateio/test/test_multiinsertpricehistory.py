import  dexprice.modules.gateio.cexprice as gateprice
import  dexprice.modules.cexdb.cexdb as cexdb
import  time
import dexprice.modules.OHLCV.one_geck as one_geck

import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import dexprice.modules.utilis.define as define
import  dexprice.modules.utilis.define as define
import dexprice.modules.proxy.proxydefine as proxydefine
import dexprice.modules.allmodules.writedb as writedb
import dexprice.modules.db.insert_db as insert_db
import dexprice.modules.proxy.clash_api as clash
import dexprice.modules.proxy.testproxy as testproxy
import dexprice.modules.OHLCV.geck_parrel as geck_parrel
import time
import time
from datetime import datetime, timedelta
import dexprice.modules.proxy.proxymultitheread as proxymultitheread
import  dexprice.modules.gateio.gateio_parrel as gateio_parrel

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






    timeframe = "d"  # 可选值: day, hour, minute
    aggregate = "1"     # 聚合时间段
    current_timestamp = int(time.time())
    limit = 10

    rate =0.5
    capacity = 30

    clash_api_url = "http://127.0.0.1:9097"
    headers = {"Authorization": "Bearer 123"}

    startport = 50000


    proxys = proxymultitheread.get_one_ip_proxy_multithread(startport, clash_api_url, headers)

    max_threads_per_proxy = 1

    for i in range(1):
        if i == 0:
            before_timestamp = str(current_timestamp)  # 当前时间的时间戳
        elif i == 1:
            # 计算 100 天前的时间戳
            before_date = datetime.fromtimestamp(current_timestamp) - timedelta(days=100)
            before_timestamp = str(int(before_date.timestamp()))
        else:
            # 如果有更多的情况，可以继续添加
            pass

        print(f"Iteration {i}, before_timestamp: {before_timestamp}")

        task_manager = gateio_parrel.GateTaskManager(
            current,
            proxys,
            rate,
            capacity,
            max_threads_per_proxy,
            timeframe,
            aggregate,
            before_timestamp,
            limit
        )
        results, failed_tasks = task_manager.run()
        # 收集数据
        token_price_history_list = db.collect_ovhl_data(results)
        # 批量插入数据
        db.insert_multiple_price_history(token_price_history_list)




    db.close()