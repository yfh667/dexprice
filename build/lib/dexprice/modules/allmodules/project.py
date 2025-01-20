import modules.db.readjson as readjson
import modules.proxy.getproxy as  getproxy
from modules.utilis.define import FilterCriteria
from functools import partial
import modules.db.insert_db as insert_db
import dexprice.modules.allmodules.writedb as writedb
import modules.PriceMonitor.tokenflitter as tokenflitter
from modules.utilis.define import Config,TokenInfo
import modules.PriceMonitor.dexscreen_priceapi as dexscreen_priceapi

import modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import modules.utilis.define as define
import  modules.utilis.define as define
import modules.proxy.proxydefine as proxydefine
import dexprice.modules.allmodules.writedb as writedb
import modules.db.insert_db as insert_db
import modules.proxy.clash_api as clash
import modules.proxy.testproxy as testproxy
def filter_ca_by_chain(result, chain_name):
    """
    从 result 中筛选出所有符合指定 chain 值的 ca。

    :param result: 包含多个字典的列表，每个字典包含 'chain' 和 'ca' 键。
    :param chain_name: 要筛选的 chain 名称（例如 'ethereum'）。
    :return: 包含所有符合条件的 ca 值的列表。
    """
    return [entry['ca'] for entry in result if entry['chain'] == chain_name]

def setproject(chainid,dbname:str,criteria: FilterCriteria,progress_callback=None):
    # criteria = FilterCriteria(
    #     liquidity_usd_min=1000,
    #     liquidity_usd_max=5000,
    #     fdv_min=1000000,
    #     fdv_max=10000000,
    #     pair_age_min_hours=5,
    #     pair_age_max_hours= None
    # )

    #  chainid = "solana"
    db_folder = '/home/yfh/Desktop/MarketSystem/Data'  # 数据库存储文件夹
    db_name = chainid+'.db'  # 数据库文件名

    db = insert_db.SQLiteDatabase(db_folder, db_name,chainid)
    db.connect()
    token_new = db.readdbtoken()
    db.close()

    pair_addresses = []

    for token in token_new:
        pair_addresses.append(token.pair_address)

    rate =5
    capacity = 300
    sourcetype = define.Config.DEXS
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


    task_manager = dexscreen_parrel.TaskManager(pair_addresses, sourcetype, chainid, proxys, rate, capacity,max_threads_per_proxy)
    tokensinfo, failed_tasks = task_manager.run()
    tokenreal  = []

    for token in tokensinfo:
        if(tokenflitter.normal_token_filter(token,  criteria)):
            if(token.creattime =='1970-01-01 00:00:00'):
                pass
            else:
                tokenreal.append(token)


    db_folder2 = '/home/yfh/Desktop/MarketSystem/Data/Project'  # 数据库存储文件夹
    db_name2 = dbname+'.db'  # 数据库文件名


    db = insert_db.SQLiteDatabase(db_folder2, db_name2,chainid)
    db.connect()
    # get the most liquid



    #print(tokensinfo)
    db.insert_multiple_tokeninfo(tokenreal)


    db.close()










