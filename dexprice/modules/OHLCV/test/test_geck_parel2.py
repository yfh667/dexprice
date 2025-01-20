from typing import Optional, List, Tuple
from datetime import datetime, timedelta, timezone
import math
import  dexprice.modules.OHLCV.geck as geck
from typing import Optional, List, Tuple
from datetime import datetime, timedelta, timezone
import math
import dexprice.modules.proxy.proxydefine as proxydefine
import dexprice.modules.proxy.clash_api as clash
import dexprice.modules.OHLCV.one_geck as one_geck
import dexprice.modules.OHLCV.geck_parrel2 as geck_parrel2
import dexprice.modules.proxy.testproxy as testproxy
pool_address = ['6rvir3c4H9cvMxtz38aG9TJPgH1sDUiGpUnupiHituVs']

# 生成开始和结束时间的时间戳
start_timestamp = one_geck.datetime_to_timestamp(2024, 9, 10, 0, 0, 0, is_utc=True)
end_timestamp = one_geck.datetime_to_timestamp(2024, 9, 22, 0, 0, 0, is_utc=True)
kline = 'minute'
aggregate = '15'
currency = "usd"
token = 'base'

queue = one_geck.create_request_queue(pool_address, start_timestamp, end_timestamp, kline, aggregate)





# print(queue)
# print(queue[0].pool_addresses)
#
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

rate =0.5
capacity = 30
chain_id = 'solana'

max_threads_per_proxy = 1
#  proxy = proxydefine.Proxy(port=50008, ip='127.0.0.1')
# proxys =  []
# proxys.append(proxy)
task_manager = geck_parrel2.GeckTaskManager2(queue,  chain_id, proxys, rate, capacity, max_threads_per_proxy)
results, failed_tasks = task_manager.run()
for result in results:
    print(result)