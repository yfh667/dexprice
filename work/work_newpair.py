
import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import  dexprice.modules.utilis.define as define
import dexprice.modules.proxy.proxydefine as proxydefine
import dexprice.modules.db.insert_db as insert_db
import dexprice.modules.proxy.clash_api as clash
import dexprice.modules.proxy.testproxy as testproxy
import dexprice.modules.OHLCV.geck_parrel as geck_parrel
import dexprice.modules.PriceMonitor.tokenflitter as tokenflitter
from dexprice.modules.utilis.define import FilterCriteria
import dexprice.modules.db.multidb as multidb
import time


# Define a function to try deleting the table with retry logic
def try_delete_table_with_retry(db, retries=3, delay=5):
    for attempt in range(retries):
        try:
            db.delete_table2()
            print("Table deleted successfully.")
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Could not delete table.")
                return False

if __name__ == "__main__":
    criteria = FilterCriteria(
        liquidity_usd_min=1000,
        liquidity_usd_max=None,
        fdv_min=None,
        fdv_max=None,
        pair_age_min_hours=None,
        pair_age_max_hours= None
    )
    clash_api_url = "http://127.0.0.1:9097"
    headers = {"Authorization": "Bearer 123"}
    chain_id = "solana"
    db_folder = '/home/yfh/Desktop/MarketSystem/Data/NewPair'   # 数据库存储文件夹
    db_name_newpairdb = 'solananewpair.db'  # 数据库文件名

    db = insert_db.SQLiteDatabase(db_folder, db_name_newpairdb,chain_id)


    db_main_name = chain_id+'_newpairresult.db'
    db2 = insert_db.SQLiteDatabase(db_folder, db_main_name,chain_id)
    db2.connect()
    geck_rate =0.5
    geck_capacity = 30
    timeframe = "minute"  # 可选值: day, hour, minute
    aggregate = "5"     # 聚合时间段 5min k-line
    geck_limit = 100
    geck_max_threads_per_proxy = 1
    dex_rate =5
    dex_capacity = 300
    dex_max_threads_per_proxy = 3

    sourcetype = define.Config.DEXS
    while(1):
        #1. we need get the token from the newpairdb,which is used by pgp
        db.connect()
        tokendata = db.readdbtoken()

        success = try_delete_table_with_retry(db)
        if success:
            print("Proceeding to the next steps...")
        else:
            print("Exiting due to failure in deleting the table.")
            break
        # print(len(tokendata))
        db.close()
        pairaddress  = []

        for token in tokendata:
            pairaddress.append(token.pair_address)

        # first we need refresh the table




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


        task_manager = dexscreen_parrel.TaskManager(pairaddress, sourcetype, chain_id, proxys, dex_rate, dex_capacity,dex_max_threads_per_proxy)
        tokensinfo, failed_tasks = task_manager.run()
        tokenreal = []
        for token in tokensinfo:
            if(tokenflitter.normal_token_filter(token,  criteria)):
                if(token.creattime =='1970-01-01 00:00:00'):
                    pass
                else:
                    tokenreal.append(token)

        db2.insert_multiple_tokeninfo(tokenreal)


        #2. we finish the read from the newpairdb,and we decide insert the token ovhl into
        # we need check the db2 pairaddress
        tokendata2 = db2.readdbtoken()
        pairaddress2  = []

        for token in tokendata2:
            pairaddress2.append(token.pair_address)

        task_manager = dexscreen_parrel.TaskManager(pairaddress2, sourcetype, chain_id, proxys, dex_rate, dex_capacity,dex_max_threads_per_proxy)
        tokensinfo, failed_tasks = task_manager.run()
        tokenreal = []
        for token in tokensinfo:
            if(tokenflitter.normal_token_filter(token,  criteria)):
                if(token.creattime =='1970-01-01 00:00:00'):
                    pass
                else:
                    tokenreal.append(token)

        realpairaddress =[]

        for token in tokenreal:
            realpairaddress.append(token.pair_address)

        missing_addresses = set(pairaddress2) - set(realpairaddress)
        # 输出结果
        print("在 paireaddress 中存在但不在 realpairaddress 中的地址：")
        for address in missing_addresses:
            db2.delete_token(address)
            print(address)
        # here we finnally refresh the token in the db

        #3. we need insert the token into the db2


        pairaddress = realpairaddress
        current_timestamp = int(time.time())
        before_timestamp = str(current_timestamp)  # 当前时间的时间戳


        task_manager = geck_parrel.GeckTaskManager(
            pairaddress,
            chain_id,
            proxys,
            geck_rate,
            geck_capacity,
            geck_max_threads_per_proxy,
            timeframe,
            aggregate,
            before_timestamp,
            geck_limit
        )
        results, failed_tasks = task_manager.run()
    # 收集数据
        token_price_history_list = db2.collect_ovhl_data(results)
        # 批量插入数据
        db2.insert_multiple_price_history(token_price_history_list)



        # here we finally finish the priceinsert
        # we begin our  strategy

        # token_price_history_list = db2.
        # 假设您的数据库路径为 'your_database.db'

 #       db_path = '/home/yfh/Desktop/MarketSystem/Data/Project/solana_100kover.db'
        db_path = db_folder+'/'+db_main_name
        # 需要读取的 token_id 列表CREATE TABLE sqlite_sequence(name,seq);
        # INSERT INTO "main"."sqlite_sequence" VALUES('token_pairs','54');
        tokendata2 = db2.readdbtoken()
        token_ids = []
        for token in tokendata2:
            token_ids.append(token.tokenid)
        #token_ids = [1,8,9,90]

        task_manager = multidb.DatabaseReadTaskManager(token_ids, db_path,chain_id, max_threads=5)
        results = task_manager.run()

        # 处理结果
        # for token_id, rows in results:
        #     print(f"Token ID: {token_id}, Rows: {rows}")
        tokenhistorys = []
# 处理结果
        for token_id, rows in results:
            tokenhistory=[]
            for row in rows:
                test = define.TokenPriceHistory(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                tokenhistory.append(test)
            tokenhistorys.append(tokenhistory)

        # for history in tokenhistorys:
        #     if(strategy1.find_bullish_pattern(history)):
        #         print(history[0].tokenid)

        time.sleep(5)

        
