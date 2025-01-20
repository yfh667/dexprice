import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import dexprice.modules.utilis.define as define

import dexprice.modules.db.insert_db as insert_db

import dexprice.modules.OHLCV.geck_parrel as geck_parrel
import dexprice.modules.PriceMonitor.tokenflitter as tokenflitter
from dexprice.modules.utilis.define import FilterCriteria

import dexprice.modules.db.multidb as multidb

import time
import dexprice.modules.tg.tgbot as tgbot
# Define a function to try deleting the table with retry logic
import dexprice.modules.proxy.proxymultitheread as proxymultitheread


def pingwen(tokenhistorys: list[define.TokenPriceHistory]):
    #  print(tokenhistorys)
    open = tokenhistorys[0].open
    last = tokenhistorys[-1].close
    if(len(tokenhistorys)>5):
        if last > 0.8 * open:
            return True


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

    # 我们只需要5-10h寿命之内的代币即可
    criteria = FilterCriteria(
        liquidity_usd_min=1000,
        liquidity_usd_max=None,
        fdv_min=100000,
        fdv_max=None,
        pair_age_min_hours=5,
        pair_age_max_hours=10
    )
    clash_api_url = "http://127.0.0.1:9097"
    headers = {"Authorization": "Bearer 123"}
    chain_id = "solana"
    # pgp获取新的sol token代币地址存入到这个数据库内
    db_folder = '/home/yfh/Desktop/MarketSystem/Data/NewPair'  # 数据库存储文件夹
    db_name_newpairdb = 'solananewpair.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name_newpairdb, chain_id)

# 这个数据库是主要的策略数据库
    db_main_name = chain_id + '_newpairresult.db'
    db2 = insert_db.SQLiteDatabase(db_folder, db_main_name, chain_id)
    db2.connect()

#备份数据库，为了存储查到的新的代币
    db_beifen_db = 'solanabeifen.db'  # 数据库文件名
    db3 = insert_db.SQLiteDatabase(db_folder, db_beifen_db, chain_id)
    db3.connect()

    geck_rate = 0.4
    geck_capacity = 24
    timeframe = "hour"  # 可选值: day, hour, minute
    aggregate = "1"  # 聚合时间段 5min k-line
    geck_limit = 10  # 我们检查5-10h之内的，因此limit提高到了10h。
    geck_max_threads_per_proxy = 1
    dex_rate = 5
    dex_capacity = 300
    dex_max_threads_per_proxy = 3

    sourcetype = define.Config.DEXS
    while (1):
        # 1. we need get the token from the newpairdb,which is produced by pgp
        db.connect()
        tokendata = db.readdbtoken()

        success = try_delete_table_with_retry(db)
        # 我们完成读取后，需要清空db1
        if success:
            print("Proceeding to the next steps...")
        else:
            print("Exiting due to failure in deleting the table.")
            break
        # print(len(tokendata))
        db.close()
        pairaddress = []

        for token in tokendata:
            pairaddress.append(token.pair_address)

        # 2 we need check the new pair

        startport = 50000

        proxys = proxymultitheread.get_one_ip_proxy_multithread(startport, clash_api_url, headers)

        task_manager = dexscreen_parrel.TaskManager(pairaddress, sourcetype, chain_id, proxys, dex_rate, dex_capacity,
                                                    dex_max_threads_per_proxy)
        tokensinfo, failed_tasks = task_manager.run()
        tokenreal = []
        for token in tokensinfo:
            if (tokenflitter.normal_token_filter(token, criteria)):
                if (token.creattime == '1970-01-01 00:00:00'):
                    pass
                else:
                    tokenreal.append(token)

        db2.insert_multiple_tokeninfo(tokenreal)
        db3.insert_multiple_tokeninfo(tokenreal)

        # 3. we finish the read from the newpairdb,and we decide insert the token ovhl into
        # we need check the db2 pairaddress
        tokendata2 = db2.readdbtoken()
        pairaddress2 = []

        for token in tokendata2:
            pairaddress2.append(token.pair_address)

        task_manager = dexscreen_parrel.TaskManager(pairaddress2, sourcetype, chain_id, proxys, dex_rate, dex_capacity,
                                                    dex_max_threads_per_proxy)
        tokensinfo, failed_tasks = task_manager.run()
        tokenreal = []
        for token in tokensinfo:
            if (tokenflitter.normal_token_filter(token, criteria)):
                if (token.creattime == '1970-01-01 00:00:00'):
                    pass
                else:
                    tokenreal.append(token)

        realpairaddress = []

        for token in tokenreal:
            realpairaddress.append(token.pair_address)

        missing_addresses = set(pairaddress2) - set(realpairaddress)
        # 输出结果
        print("在 paireaddress 中存在但不在 realpairaddress 中的地址：")
        for address in missing_addresses:
            db2.delete_token(address)
            #print(address)
        # here we finnally refresh the token in the db

        # 4. we need insert the token into the db2

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

        # we get the new history so we better restore the results

        token_price_history_list = db2.collect_ovhl_data(results)
        # 批量插入数据
        db2.insert_multiple_price_history(token_price_history_list)

        db_path = db_folder + '/' + db_main_name

        tokens = db2.readdbtoken()
        requestedtokenid = []
        for token in tokens:
            requestedtokenid.append(token.tokenid)

        task_manager = multidb.DatabaseReadTaskManager(requestedtokenid, db_path, chain_id, max_threads=5)
        results = task_manager.run()
        tokenhistorys = []
        # 处理结果
        for token_id, rows in results:
            tokenhistory = []
            for row in rows:
                test = define.TokenPriceHistory(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                tokenhistory.append(test)
            tokenhistorys.append(tokenhistory)

        for tokenhistory in tokenhistorys:
            if (pingwen(tokenhistory)):
                tokenid = tokenhistory[0].tokenid
                tokendb = db2.read_token_withid(tokenid)

                pairaddress = tokendb.pair_address
                tgbot.sendmessage(pairaddress)
                # we need delete the token
                db2.delete_token(pairaddress)
            elif (tokenhistory[-1].high>5*tokenhistory[-1].low) and len(tokenhistory) > 2:
                tokenid = tokenhistory[0].tokenid
                tokendb = db2.read_token_withid(tokenid)

                pairaddress = tokendb.pair_address
                tgbot.sendmessage(pairaddress)
                # we need delete the token
                db2.delete_token(pairaddress)



        time.sleep(1200)
