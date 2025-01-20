

import dexprice.modules.proxy.proxydefine as proxydefine

import dexprice.modules.OHLCV.geck_parrel as geck_parrel
def main():
 #   addresses = ["Gv9BCH3cL4U4YV6SJKb5H5U4kF2XoJ8KvNfuDoEYmHUQ"]  # 您的地址列表
    addresses = ["FzFb2DqD8YDQNJJZNaw7T5jwheq4NmW7DeJL6HweTXkn",
                 "A4Cv8W894qRCbHkE2K9NW7Q1gdC8huH91suZb4i3g71v",
                 "6gRKHruMjdhL2pMFR4eWxqNKJywty9CEGjmXYfeK25aq",
                 "7d7eq8XndLr4JAWVAogDGJopW19qo8kVuKvCSvkkzYGE",
                 "9wRhpAGKzhdiMeZAzWga2F9u71keiDaUoatw24EYFPhY",
                 "2VUjifCjFij7ZWnju8BZ6dDTruAozLomp77qgr8mvpS6",
                 "48dtTgfgasqP2hbg2A4Qfbf6XANeRd9ZUi7em945bHAm",
                 "Fed8BgRzfh1uiMvWF3nU2XRmAyjLoHmi45Ry9H1hTyLL"]




    chain_id = "solana"


    timeframe = "day"  # 可选值: day, hour, minute
    aggregate = "1"     # 聚合时间段
    before_timestamp = "1730678400"  # 可选的时间戳参数
    limit = 2




    rate =0.5
    capacity = 30


    max_threads_per_proxy = 1
    proxy = proxydefine.Proxy(port=50008, ip='127.0.0.1')
    proxys =  []
    proxys.append(proxy)
    task_manager = geck_parrel.GeckTaskManager(addresses,  chain_id, proxys, rate, capacity, max_threads_per_proxy,timeframe, aggregate, before_timestamp, limit)
    results, failed_tasks = task_manager.run()
    print(f"Total failed tasks: {results}")
    print(f"Total successful results: {len(results)}")
    print(f"Total failed tasks: {len(failed_tasks)}")





if __name__ == "__main__":
    main()



