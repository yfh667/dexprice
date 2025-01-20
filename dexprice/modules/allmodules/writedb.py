
from dexprice.modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类

from dexprice.modules.utilis.define import Config,TokenInfo

from tqdm import tqdm
import threading
import math

import dexprice.modules.db.insert_db as insert_db

import  dexprice.modules.db.readjson as readjson
def pairaddressdb(chain_id,pair_addresses,num_threads,proxy_ports,rate,capacity,db_folder,db_name,process_fn):
    manager = DexscreenApiManager()  # 实例化类


    results = manager.multi_get_token_dexscreen(Config.DEXS, pair_addresses, chain_id, num_threads, proxy_ports,rate,capacity)

    flattened_results = [token for sublist in results for token in sublist]

    #3.we need set the scale for fdv liquid etc.

    tokens=[]
    for results1 in flattened_results:
        if process_fn(results1) :
            print(results1)
            tokens.append(results1)
        else:
            pass
    db = insert_db.SQLiteDatabase(db_folder, db_name,chain_id)
    db.connect()
    db.insert_multiple_tokeninfo(tokens)
    # 关闭数据库连接
    db.close()

def pairaddress_info(sourcetype:int,chain_id,pair_addresses,num_threads,proxy_ports,rate,capacity,process_fn=None,progress_callback=None):
    manager = DexscreenApiManager()  # 实例化类

   # print(pair_addresses)
    results = manager.multi_get_token_dexscreen(sourcetype,pair_addresses, chain_id, num_threads, proxy_ports,rate,capacity,progress_callback)
   # print(results)
    flattened_results = [token for sublist in results for token in sublist]
  #  print(flattened_results)
    # here we need filier the token
    if process_fn:

        tokens=[]

        for results1 in flattened_results:
            if process_fn(results1) :

                tokens.append(results1)
            else:
             #   print(results1)
                pass


        return tokens
    else:
        return flattened_results


def jsontodb_one(chain_id,file_path,num_threads,proxy_ports,rate,capacity,db_folder,db_name):

    json_data = read_json_file(file_path)
    # 从 JSON 数据中提取所有链和合约地址
    jsonresults = gettokenca(json_data)


    pair_addresses = [item['ca'] for item in jsonresults if item['chainid'] == chain_id]
    pairaddressdb(chain_id,pair_addresses,num_threads,proxy_ports,rate,capacity,db_folder,db_name)

def jsontodb_multi(chain_id,file_path,num_threads,proxy_ports,rate,capacity,db_folder,db_name,process_fn):
    directory ='/home/yfh/Desktop/beifen/test/'
    jsonresults =readjson.process_all_json_files(directory)
    # json_data = read_json_file(file_path)
    # # 从 JSON 数据中提取所有链和合约地址
    # jsonresults = gettokenca(json_data)
    print(jsonresults)
    pair_addresses = [item['ca'] for item in jsonresults if item['chain'] == chain_id]
    pairaddressdb(chain_id,pair_addresses,num_threads,proxy_ports,rate,capacity,db_folder,db_name,process_fn)


def jsontodb_multi2(chain_id,file_path,num_threads,proxy_ports,rate,capacity,db_folder,db_name,process_fn):
    # directory ='/home/yfh/Desktop/beifen/test/'
    # jsonresults =readjson.process_all_json_files(directory)
    # json_data = read_json_file(file_path)
    # # 从 JSON 数据中提取所有链和合约地址
    # jsonresults = gettokenca(json_data)
   # file_path ='/home/yfh/Desktop/beifen/test/allforeth.json'
    results =  readjson.gettokenca(file_path)
    #print(jsonresults)
    pair_addresses = [item['ca'] for item in results if item['chain'] == chain_id]
    pairaddressdb(chain_id,pair_addresses,num_threads,proxy_ports,rate,capacity,db_folder,db_name,process_fn)