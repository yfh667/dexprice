
import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import  dexprice.modules.utilis.define as define

import dexprice.modules.db.insert_db as insert_db

import time

import dexprice.modules.proxy.proxymultitheread as proxymultitheread
import dexprice.modules.tg.tgbot as tgbot
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

    clash_api_url = "http://127.0.0.1:9097"
    headers = {"Authorization": "Bearer 123"}
    chain_id = "solana"
    db_folder = '/home/yfh/Desktop/MarketSystem/Data/Project'   # 数据库存储文件夹
    db_name_newpairdb = 'relaobi.db'  # 数据库文件名

    db = insert_db.SQLiteDatabase(db_folder, db_name_newpairdb,chain_id)
    db.connect()
    tokens = db.readdbtoken()

    pairaddress =[]
    for token in tokens:
        pairaddress.append(token.pair_address)




    dex_rate =5
    dex_capacity = 300
    dex_max_threads_per_proxy = 3
    startport = 50000
    sourcetype = define.Config.DEXS


    proxys = proxymultitheread.get_one_ip_proxy_multithread(startport, clash_api_url, headers)

    task_manager = dexscreen_parrel.TaskManager(pairaddress, sourcetype, chain_id, proxys, dex_rate, dex_capacity,dex_max_threads_per_proxy)
    tokensinfo, failed_tasks = task_manager.run()


        # 假设 tokensinfo 是从 task_manager.run() 返回的结果
    initial_prices = {token.address: token.price_usd for token in tokensinfo}

    # 打印生成的字典
   # print(address_price_dict)
    while(1):
        # first we need refresh the table

        tokens = db.readdbtoken()

        pairaddress =[]
        for token in tokens:
            pairaddress.append(token.pair_address)

        time.sleep(60)

        proxys = proxymultitheread.get_one_ip_proxy_multithread(startport, clash_api_url, headers)

        task_manager = dexscreen_parrel.TaskManager(pairaddress, sourcetype, chain_id, proxys, dex_rate, dex_capacity,dex_max_threads_per_proxy)
        tokensinfo, failed_tasks = task_manager.run()

            # 遍历新获得的 tokensinfo 并与初始价格字典对比
        for token in tokensinfo:
            if token.address in initial_prices:
                initial_price = initial_prices[token.address]
                # we try to fenbie
                if(token.fdv<100000):
                    # 防止初始价格为 0 的情况
                    if initial_price > 0 and (token.price_usd / initial_price) > 6:
                        print(f"YES: Token {token.name} ({token.address}) price increased by more than 500%! "
                              f"Initial: {initial_price}, Current: {token.price_usd}")
                        tgbot.sendmessagewithtoken(token.address,"@jingou22")
                        db.delete_token(token.pair_address)
                else:
                    if initial_price > 0 and (token.price_usd / initial_price) > 3:
                            print(f"YES: Token {token.name} ({token.address}) price increased by more than 500%! "
                                  f"Initial: {initial_price}, Current: {token.price_usd}")
                            tgbot.sendmessagewithtoken(token.address,"@jingou22")
                            db.delete_token(token.pair_address)






