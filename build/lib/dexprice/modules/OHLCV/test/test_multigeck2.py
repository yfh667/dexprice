
import modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import modules.utilis.define as define
import  modules.utilis.define as define
import modules.proxy.proxydefine as proxydefine
import dexprice.modules.allmodules.writedb as writedb
import modules.db.insert_db as insert_db
import modules.proxy.clash_api as clash
import modules.proxy.testproxy as testproxy
import modules.OHLCV.geck_parrel as geck_parrel
def main():
    addresses = ["6USpEBbN94DUYLUi4a2wo3AZDCyozon1PLGYu27jzPkX"]  # 您的地址列表

    # addresses = ["FzFb2DqD8YDQNJJZNaw7T5jwheq4NmW7DeJL6HweTXkn",
    #              "A4Cv8W894qRCbHkE2K9NW7Q1gdC8huH91suZb4i3g71v",
    #              "6gRKHruMjdhL2pMFR4eWxqNKJywty9CEGjmXYfeK25aq",
    #              "7d7eq8XndLr4JAWVAogDGJopW19qo8kVuKvCSvkkzYGE",
    #              "9wRhpAGKzhdiMeZAzWga2F9u71keiDaUoatw24EYFPhY",
    #              "2VUjifCjFij7ZWnju8BZ6dDTruAozLomp77qgr8mvpS6",
    #              "48dtTgfgasqP2hbg2A4Qfbf6XANeRd9ZUi7em945bHAm",
    #              "6USpEBbN94DUYLUi4a2wo3AZDCyozon1PLGYu27jzPkX"]


    chain_id = "solana"
    db_folder = '/home/yfh/Desktop/MarketSystem/Data/Project'  # 数据库存储文件夹
    db_name = "testgck"+'.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name,"solana")
    db.connect()

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


    task_manager = dexscreen_parrel.TaskManager(addresses, sourcetype, chain_id, proxys, rate, capacity,max_threads_per_proxy)
    tokensinfo, failed_tasks = task_manager.run()
    db.insert_multiple_tokeninfo(tokensinfo)









    timeframe = "day"  # 可选值: day, hour, minute
    aggregate = "1"     # 聚合时间段
    before_timestamp = "1730678400"  # 可选的时间戳参数
    limit = 100




    rate =0.5
    capacity = 30


    max_threads_per_proxy = 1
  #  proxy = proxydefine.Proxy(port=50008, ip='127.0.0.1')
    # proxys =  []
    # proxys.append(proxy)
    task_manager = geck_parrel.GeckTaskManager(addresses,  chain_id, proxys, rate, capacity, max_threads_per_proxy,timeframe, aggregate, before_timestamp, limit)
    results, failed_tasks = task_manager.run()
    for ovhldata in results:
        db.insert_OvhlFromDex(ovhldata)
    print(f"Total failed tasks: {failed_tasks}")
    print(f"Total successful results: {len(results)}")
    print(f"Total failed tasks: {len(failed_tasks)}")
    db.close()


if __name__ == "__main__":
    main()



