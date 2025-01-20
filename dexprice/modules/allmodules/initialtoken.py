import dexprice.modules.db.readjson as readjson

import  math

import dexprice.modules.proxy.proxymultitheread as proxymultitheread

import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import  dexprice.modules.utilis.define as define
import dexprice.modules.proxy.proxydefine as proxydefine
#import dexprice.modules.db.insert_db as insert_db
import dexprice.modules.db.insert_db as insert_db
def remove_duplicates(pairaddress):
    # 去除列表中的重复元素
    return list(set(pairaddress))
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

#
#
#
# def initialtoken2(file,chainid,progress_callback=None):
#     results =  readjson.gettokenCAaddress(file,chainid)
#     CApairaddress =  filter_ca_by_chain(results, chainid)
#     unique_CApairaddress = remove_duplicates(CApairaddress)
#
#     if progress_callback:
#         print("Starting progress tracking...")
#
#     max_batch_size = 5000
#     #chain_id = 'solana'
#
#     total_addresses = len(unique_CApairaddress)
#     num_batches = math.ceil(total_addresses / max_batch_size)
#
#     clash_api_url = "http://127.0.0.1:9097"
#     headers = {"Authorization": "Bearer 123"}
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     PROJECT_ROOT = findroot.find_project_root(current_dir)
#     DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")
#
#     db_folder = DATA_FOLDER  # 数据库存储文件夹
#     db_name = chainid+'.db'  # 数据库文件名
#     db = insert_db.SQLiteDatabase_linshi(db_folder, db_name)
#     db.connect()
#     for i in range(num_batches):
#         start = i * max_batch_size
#         end = min(start + max_batch_size, total_addresses)
#         batch = unique_CApairaddress[start:end]
#
#         rate =5
#         capacity = 300
#         sourcetype = define.Config.DEXCA
#         max_threads_per_proxy = 2
#
#
#         startport = 50000
#
#         proxys = proxymultitheread.get_one_ip_proxy_multithread(startport, clash_api_url, headers)
#
#         task_manager = dexscreen_parrel.TaskManager(batch, sourcetype, '', proxys, rate, capacity,max_threads_per_proxy,'initial')
#         tokensinfo, failed_tasks = task_manager.run()
#         print(tokensinfo)
#         print("we have get the following tasks:")
#
#         db.insert_multiple_tokeninfo(tokensinfo)
#
#     db.close()




def initialtoken3(file,progress_callback=None):
    results =  readjson.gettokenCAaddress_linshi(file)
    CApairaddress = results
    unique_CApairaddress = remove_duplicates(CApairaddress)

    if progress_callback:
        print("Starting progress tracking...")

    max_batch_size = 5000
    #chain_id = 'solana'

    total_addresses = len(unique_CApairaddress)
    num_batches = math.ceil(total_addresses / max_batch_size)

    clash_api_url = "http://127.0.0.1:9097"
    headers = {"Authorization": "Bearer 123"}
    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = findroot.find_project_root(current_dir)
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

    db_folder = DATA_FOLDER  # 数据库存储文件夹
    db_name = 'all.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    for i in range(num_batches):
        start = i * max_batch_size
        end = min(start + max_batch_size, total_addresses)
        batch = unique_CApairaddress[start:end]

        rate =5
        capacity = 300
        sourcetype = define.Config.DEXCA
        max_threads_per_proxy = 2


        startport = 50000

        proxys = proxymultitheread.get_one_ip_proxy_multithread(startport, clash_api_url, headers)

        task_manager = dexscreen_parrel.TaskManager(batch, sourcetype, '', proxys, rate, capacity,max_threads_per_proxy,'initial')
        tokensinfo, failed_tasks = task_manager.run()
        print(tokensinfo)
        print("we have get the following tasks:")

        db.insert_multiple_tokeninfo(tokensinfo)
    #we have add all the token into the db,but we need refresh the db


    db.close()
