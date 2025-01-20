
import modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import modules.utilis.define as define
import  modules.utilis.define as define
import modules.proxy.proxydefine as proxydefine
import dexprice.modules.allmodules.writedb as writedb
import modules.db.insert_db as insert_db
import modules.proxy.clash_api as clash
import modules.proxy.testproxy as testproxy
def main():
#    addresses = ["Gv9BCH3cL4U4YV6SJKb5H5U4kF2XoJ8KvNfuDoEYmHUQ"]  # 您的地址列表
  #  sourcetype = define.Config.DEXS
    chain_id = "solana"
    db_folder = '/home/yfh/Desktop/MarketSystem/Data'  # 数据库存储文件夹
    db_name = chain_id+'.db'  # 数据库文件名

    db = insert_db.SQLiteDatabase(db_folder, db_name,chain_id)
    db.connect()
    token_new = db.readdbtoken()
    db.close()

    pairaddress = []

    for token in token_new:
        pairaddress.append(token.address)



    rate =2.5
    capacity = 150
    sourcetype = define.Config.DEXCA
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


    task_manager = dexscreen_parrel.TaskManager(pairaddress, sourcetype, chain_id, proxys, rate, capacity,max_threads_per_proxy)
    results, failed_tasks = task_manager.run()
    print(results[0])
    print(f"Total successful results: {len(results)}")
    print(f"Total failed tasks: {len(failed_tasks)}")


if __name__ == "__main__":
    main()
