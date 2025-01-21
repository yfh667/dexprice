
from dexprice.modules.utilis.define import FilterCriteria

import dexprice.modules.PriceMonitor.tokenflitter as tokenflitter

import dexprice.modules.proxy.proxymultitheread as proxymultitheread

import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel

import dexprice.modules.utilis.define as define
import dexprice.modules.proxy.proxydefine as proxydefine

#import dexprice.modules.db.insert_db as insert_db
import dexprice.modules.db.insert_db as insert_db

import dexprice.modules.proxy.clash_api as clash
import dexprice.modules.proxy.testproxy as testproxy
import os
import dexprice.modules.utilis.findroot as findroot
def filter_ca_by_chain(result, chain_name):
    """
    从 result 中筛选出所有符合指定 chain 值的 ca。

    :param result: 包含多个字典的列表，每个字典包含 'chain' 和 'ca' 键。
    :param chain_name: 要筛选的 chain 名称（例如 'ethereum'）。
    :return: 包含所有符合条件的 ca 值的列表。
    """
    return [entry['ca'] for entry in result if entry['chain'] == chain_name]





def setproject_linshi(dbname:str,criteria: FilterCriteria,progress_callback=None):
    criteria = FilterCriteria(
        liquidity_usd_min=1000,
        liquidity_usd_max=5000,
        fdv_min=1000000,
        fdv_max=10000000,
        pair_age_min_hours=5,
        pair_age_max_hours= None
       )


    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = findroot.find_project_root(current_dir)
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

    db_folder = DATA_FOLDER

    db_name = 'all.db'  # 数据库文件名
#here
  #  db = insert_db.SQLiteDatabase(db_folder, db_name,chainid)
    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    token_new = db.readdbtoken()


    # here we get all the token them from bsc base   ethereum solana,so we need split the into the group

    # 初始化字典，用链名作为键，地址列表作为值
    chain_addresses = {
        'solana': [],
        'base': [],
        'ethereum': [],
        'bsc': []
    }

    # 遍历 token_new，根据链名将地址加入对应的列表
    for token in token_new:
        # 确保 token.chainid 是链名，并存在于字典的键中
        if token.chainid in chain_addresses:
            chain_addresses[token.chainid].append(token.pair_address)  # 添加地址到对应链的列表
   # all the token that satisfied the request
    tokenreal = []
    # # 示例：打印每个链名及其对应的地址列表
    for chain, pairaddresses in chain_addresses.items():

        print(f"we check Chain: {chain} ")

        rate = 5
        capacity = 300

        chainid = chain

        sourcetype = define.Config.DEXS
        max_threads_per_proxy = 2
        clash_api_url = "http://127.0.0.1:9097"
        headers = {"Authorization": "Bearer 123"}

        startport = 50000

        proxys = proxymultitheread.get_one_ip_proxy_multithread(startport, clash_api_url, headers)

        task_manager = dexscreen_parrel.TaskManager(pairaddresses, sourcetype, chainid, proxys, rate, capacity,
                                                    max_threads_per_proxy, 'get  ' + chainid)
        tokensinfo, failed_tasks = task_manager.run()

        for token in tokensinfo:
            if (tokenflitter.normal_token_filter(token, criteria)):
                if (token.creattime == '1970-01-01 00:00:00'):
                    pass
                else:
                    tokenreal.append(token)



    db.close()

    db_folder2 = DATA_FOLDER+'/Project'
    db_name2 = dbname+'.db'  # 数据库文件名


    db = insert_db.SQLiteDatabase(db_folder2, db_name2)
    db.connect()

    db.insert_multiple_tokeninfo(tokenreal)


    db.close()












