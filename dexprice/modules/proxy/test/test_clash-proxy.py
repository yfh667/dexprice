
import modules.proxy.proxydefine as proxydefine
import threading
import modules.proxy.clash_api as clash
import modules.proxy.getproxy as getproxy
import modules.proxy.testproxy as testproxy
import time
# 示例使用
if __name__ == "__main__":
    # 假设您有一个 Clash API，可以获取所有代理的信息
    # 由于我们没有实际的 Clash API，这里将模拟代理列表



    # 设置要检查的端口范围
    clash_api_url = "http://127.0.0.1:9097"
    headers = {"Authorization": "Bearer 123"}
    proxies = clash.get_all_proxies(clash_api_url,headers)

    proxynumber = clash.get_proxy_number(proxies)
    available_ports = getproxy.check_open_ports(50000, proxynumber)

   # print("可用端口:", available_ports)

    # 模拟获取代理数量
   # proxynumber = 5  # 假设有 5 个代理
    startport = 50000

    # 创建 ProxyPool 实例
    rate = 2.5  # 每秒允许的请求数
    capacity = 150  # 令牌桶的容量
    max_threads_per_proxy = 3  # 每个代理的最大并发线程数
    proxy_pool = proxydefine.ProxyPool(rate, capacity, max_threads_per_proxy)

    # 添加代理到代理池
    for i in range(proxynumber):
        port = startport + i
        proxy = '127.0.0.1:' + str(port)
        ip = testproxy.fetch_public_ip_via_http_proxy(proxy)
      #  ip = "127.0.0.1"  # 假设所有代理的 IP 都是本地地址
        proxy = proxydefine.Proxy(proxy, ip)
        proxy_pool.add_proxy(proxy)

    # 打印代理池状态
    print(proxy_pool)
    #
    # # 模拟使用代理池
    # def worker_task(proxy_pool: proxydefine.ProxyPool, task_id: int):
    #     proxy, limiter, semaphore = proxy_pool.acquire_proxy()
    #     if proxy:
    #         try:
    #             # 模拟速率限制
    #             if limiter.consume("api_call", 1):
    #                 print(f"Task {task_id} is using proxy {proxy.port}")
    #                 time.sleep(1)  # 模拟请求耗时
    #             else:
    #                 print(f"Task {task_id} is rate limited on proxy {proxy.port}")
    #         finally:
    #             proxy_pool.release_proxy(proxy.port, semaphore)
    #     else:
    #         print(f"Task {task_id} could not acquire a proxy")
    #
    # # 启动一些线程来模拟任务
    # threads = []
    # for i in range(10):
    #     t = threading.Thread(target=worker_task, args=(proxy_pool, i))
    #     threads.append(t)
    #     t.start()
    #
    # # 等待所有线程完成
    # for t in threads:
    #     t.join()
    #
    # # 打印代理池状态
    # print(proxy_pool)
