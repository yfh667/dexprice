import dexprice.modules.allmodules.geckpricehistory as geckpricehistory
import dexprice.modules.db.insert_db as insert_db
import dexprice.modules.utilis.define as define

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
import dexprice.modules.db.postsql as postsql

## use postql, we could neleget it
if __name__ == "__main__":

    chain_id = "solana"
    db_folder = '/home/yfh/Desktop/MarketSystem/Data/Project'   # 数据库存储文件夹
    db_name = "10days"+'.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name,chain_id)
    db.connect()
    tokens = db.readdbtoken()
    paireaddress = []
    for token in tokens:
        paireaddress.append(token.pair_address)


    # first we need refresh the table
    rate =5
    capacity = 300
    sourcetype = define.Config.DEXS
    max_threads_per_proxy = 3
    clash_api_url = "http://127.0.0.1:9097"
    headers = {"Authorization": "Bearer 123"}

    startport = 50000
    proxys = []
    proxysport =clash.get_one_ip_proxy(startport,clash_api_url,headers)

    # 添加代理到代理池
    for port in proxysport:
        socksproxy = '127.0.0.1:' + str(port)
        ip = testproxy.fetch_public_ip_via_http_proxy(socksproxy)
        if ip !=None:
            proxy = proxydefine.Proxy(port, ip)
            proxys.append(proxy)


    task_manager = dexscreen_parrel.TaskManager(paireaddress, sourcetype, chain_id, proxys, rate, capacity,max_threads_per_proxy)
    tokensinfo, failed_tasks = task_manager.run()

    realpairaddress =[]
    for token in tokensinfo:
        realpairaddress.append(token.pair_address)
    missing_addresses = set(paireaddress) - set(realpairaddress)

    # 输出结果
    print("在 paireaddress 中存在但不在 realpairaddress 中的地址：")
    for address in missing_addresses:
        db.delete_token(address)
        print(address)


    db.close()

    timeframe = "hour"  # 可选值: day, hour, minute
    aggregate = "1"     # 聚合时间段
    current_timestamp = int(time.time())
    limit = 100

    db_config = {
        'host': 'localhost',
        'port': 5432,
        'dbname': 'solana10days',
        'user': 'yfh',
        'password': 'yfh'
    }

    db = postsql.PostgreSQLDatabase(db_config, chain_id)
    before_timestamp = str(current_timestamp)  # 当前时间的时间戳

    #geckpricehistory.inserthistorywithgeck_db(db,realpairaddress,chain_id,proxys,timeframe,aggregate,before_timestamp,limit)
    geckpricehistory.inserthistorywithgeck_db2(db, realpairaddress, chain_id, proxys, timeframe, aggregate, 240, limit)
    db.close()
