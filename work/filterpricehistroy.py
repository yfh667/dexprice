
import dexprice.modules.db.multidb   as multidb
import dexprice.modules.utilis.define as define
import dexprice.modules.PriceMonitor.tokenflitter as tokenflitter
import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import dexprice.modules.utilis.define as define
import dexprice.modules.proxy.proxydefine as proxydefine
import dexprice.modules.db.insert_db as insert_db
import dexprice.modules.proxy.clash_api as clash
import dexprice.modules.proxy.testproxy as testproxy
# 假设您的数dexprice.据库路径为 'your_database.db'
import dexprice.modules.strategy.strategy1 as strategy1

if __name__ == "__main__":
    criteria = define.FilterCriteria(
        liquidity_usd_min=1000,
        liquidity_usd_max=None,
        fdv_min=100000,
        fdv_max=10000000,
        pair_age_min_hours=720,
        pair_age_max_hours= None
    )
    db_folder = '/home/yfh/Desktop/MarketSystem/Data/Project'  # 数据库存储文件夹
    db_name = "solana_100kover"+'.db'  # 数据库文件名
    chainid = 'solana'
    db = insert_db.SQLiteDatabase(db_folder, db_name,chainid)
    db.connect()
    token_new = db.readdbtoken()


    pair_addresses = []

    for token in token_new:
        pair_addresses.append(token.pair_address)

    rate =5
    capacity = 300
    sourcetype = define.Config.DEXS
    max_threads_per_proxy = 2
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


    task_manager = dexscreen_parrel.TaskManager(pair_addresses, sourcetype, chainid, proxys, rate, capacity,max_threads_per_proxy)
    tokensinfo, failed_tasks = task_manager.run()

    requestedtokenid = []

    for token in tokensinfo:
        if(tokenflitter.normal_token_filter(token,  criteria)):
            requestedtokenid.append(db.FindParetokenid( token.pair_address))


    db_path = db_folder+'/'+db_name
    task_manager = multidb.DatabaseReadTaskManager(requestedtokenid,  db_path,chainid, max_threads=8)
    results = task_manager.run()
    tokenhistorys = []
    # 处理结果
    for token_id, rows in results:
        tokenhistory=[]
        for row in rows:
            test = define.TokenPriceHistory(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
            tokenhistory.append(test)
        tokenhistorys.append(tokenhistory)

# find_bullish_pattern(ovhldata: list[define.TokenPriceHistory]):
    for history in tokenhistorys:
        if(strategy1.find_bullish_pattern(history)):
            print(history[0].tokenid)
    print("we sourt")
    strategy1.simple(tokenhistorys[0])

    db.close()