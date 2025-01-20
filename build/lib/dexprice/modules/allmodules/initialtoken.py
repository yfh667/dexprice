import modules.db.readjson as readjson
import modules.proxy.getproxy as  getproxy
from modules.utilis.define import Config,TokenInfo
import modules.db.insert_db as insert_db
import dexprice.modules.allmodules.writedb as writedb
import modules.PriceMonitor.tokenflitter as tokenflitter
import  math
import modules.proxy.testproxy as testproxy
import random
import modules.utilis.define as define
import modules.proxy.clash_api as clash

import modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import modules.utilis.define as define
import  modules.utilis.define as define
import modules.proxy.proxydefine as proxydefine
import dexprice.modules.allmodules.writedb as writedb
import modules.db.insert_db as insert_db
import modules.proxy.clash_api as clash
import modules.proxy.testproxy as testproxy
def remove_duplicates(pairaddress):
    # 去除列表中的重复元素
    return list(set(pairaddress))


def filter_ca_by_chain(result, chain_name):
    """
    从 result 中筛选出所有符合指定 chain 值的 ca。

    :param result: 包含多个字典的列表，每个字典包含 'chain' 和 'ca' 键。
    :param chain_name: 要筛选的 chain 名称（例如 'ethereum'）。
    :return: 包含所有符合条件的 ca 值的列表。
    """
    return [entry['ca'] for entry in result if entry['chain'] == chain_name]


def initialtoken(file,chainid,progress_callback=None):
    # we get the token from the jsonfile

 #   results =  readjson.process_all_json_files2(file)

    #gettokenca

    results =  readjson.gettokenca(file)
    # we get the pairaddress
    pairaddress =  filter_ca_by_chain(results, chainid)
    #this we will get [  '0x11f63834f8daa7c5daea802579abdfd9456b30a8', '0x11f63834f8daa7c5daea802579abdfd9456b30a8', ]
   #
    if progress_callback:
        print("Starting progress tracking...")

    start_port = 30001
    numner = 22
    available_ports = getproxy.check_open_ports(start_port, numner)


    tokensinfo = writedb.pairaddress_info(Config.DEXS,chainid,pairaddress,len(available_ports)*3,available_ports,5,300,tokenflitter.liquid_token_filter,progress_callback)
    #return tokensinfo

    db_folder = '/home/yfh/Desktop/MarketSystem/Data'  # 数据库存储文件夹
    db_name = chainid+'.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name,chainid)
    db.connect()
    db.insert_multiple_tokeninfo(tokensinfo)
    #
    #
    #
    #
    #
    #
    #
    #
    db.close()


def initialtoken2(file,chainid,progress_callback=None):
    results =  readjson.gettokenCAaddress(file,chainid)
    CApairaddress =  filter_ca_by_chain(results, chainid)
    unique_CApairaddress = remove_duplicates(CApairaddress)

    if progress_callback:
        print("Starting progress tracking...")

    max_batch_size = 5000
    chain_id = 'solana'

    total_addresses = len(unique_CApairaddress)
    num_batches = math.ceil(total_addresses / max_batch_size)

    clash_api_url = "http://127.0.0.1:9097"
    headers = {"Authorization": "Bearer 123"}

    db_folder = '/home/yfh/Desktop/MarketSystem/Data'  # 数据库存储文件夹
    db_name = chainid+'.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name,chainid)
    db.connect()
    for i in range(num_batches):
        start = i * max_batch_size
        end = min(start + max_batch_size, total_addresses)
        batch = unique_CApairaddress[start:end]

        rate =2.5
        capacity = 150
        sourcetype = define.Config.DEXCA
        max_threads_per_proxy = 2


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


        task_manager = dexscreen_parrel.TaskManager(batch, sourcetype, chain_id, proxys, rate, capacity,max_threads_per_proxy)
        tokensinfo, failed_tasks = task_manager.run()


        db.insert_multiple_tokeninfo(tokensinfo)

    db.close()
