
from dexprice.modules.utilis.define import FilterCriteria

import dexprice.modules.PriceMonitor.tokenflitter as tokenflitter

import dexprice.modules.proxy.proxymultitheread as proxymultitheread

import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel

import dexprice.modules.utilis.define as define
import dexprice.modules.proxy.proxydefine as proxydefine

import dexprice.modules.db.insert_db_linshi as insert_db

import os
import dexprice.modules.utilis.findroot as findroot

def refreshmaindb():

    # we need refresh the whole db
    criteria = FilterCriteria(
        liquidity_usd_min=1000,
        liquidity_usd_max=None,
        fdv_min=1000,
        fdv_max=None,
        pair_age_min_hours=None,
        pair_age_max_hours= None
    )

    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = findroot.find_project_root(current_dir)
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

    db_folder = DATA_FOLDER

    db_name =   'all.db'  # 数据库文件名

    db = insert_db.SQLiteDatabase_linshi(db_folder, db_name)
    db.connect()
    token_new = db.readdbtoken()


    pair_addresses = []

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
    tokenreal = []
    # # 示例：打印每个链名及其对应的地址列表
    for chain, pairaddresses in chain_addresses.items():


        print(f"we check Chain: {chain} ")


        rate = 5
        capacity = 300

        chainid  = chain

        sourcetype = define.Config.DEXS
        max_threads_per_proxy = 2
        clash_api_url = "http://127.0.0.1:9097"
        headers = {"Authorization": "Bearer 123"}
        startport = 50000
        proxys = proxymultitheread.get_one_ip_proxy_multithread(startport, clash_api_url, headers)

        task_manager = dexscreen_parrel.TaskManager(pairaddresses, sourcetype, chainid, proxys, rate, capacity,
                                                    max_threads_per_proxy,'refresh '+chainid)
        tokensinfo, failed_tasks = task_manager.run()

        for token in tokensinfo:
            if (tokenflitter.normal_token_filter(token, criteria)):
                if (token.creattime == '1970-01-01 00:00:00'):
                    pass
                else:
                    tokenreal.append(token)


    realpairaddress = []
    for token in tokenreal:
        realpairaddress.append(token.pair_address)
   # print(realpairaddress)
    missing_addresses = set(pairaddresses) - set(realpairaddress)
    # 输出结果
    print("在 paireaddress 中存在但不在 realpairaddress 中的地址：")
    for address in missing_addresses:
        db.delete_token(address)
        print(address)


    db.close()










