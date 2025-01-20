
import modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import  modules.utilis.define as define
import modules.proxy.proxydefine as proxydefine


def main():
    addresses = ["Gv9BCH3cL4U4YV6SJKb5H5U4kF2XoJ8KvNfuDoEYmHUQ"]  # 您的地址列表
    sourcetype = define.Config.DEXS
    chain_id = "solana"




    rate =5
    capacity = 300



    #
    # startport = 50000
    # proxys = []
    # proxysport =clash.get_one_ip_proxy(startport,clash_api_url,headers)
    #
    # # 添加代理到代理池
    # for port in proxysport:
    #     socksproxy = '127.0.0.1:' + str(port)
    #     ip = testproxy.fetch_public_ip_via_http_proxy(socksproxy)
    #     if ip !=None:
    #         proxy = proxydefine.Proxy(port, ip)
    #         proxys.append(proxy)



    max_threads_per_proxy = 2
    proxy = proxydefine.Proxy(port=50001, ip='127.0.0.1')
    proxys =  []
    proxys.append(proxy)
    task_manager = dexscreen_parrel.TaskManager(addresses, sourcetype, chain_id, proxys, rate, capacity,max_threads_per_proxy)
    results, failed_tasks = task_manager.run()

    print(f"Total successful results: {len(results)}")
    print(f"Total failed tasks: {len(failed_tasks)}")

if __name__ == "__main__":
    main()
