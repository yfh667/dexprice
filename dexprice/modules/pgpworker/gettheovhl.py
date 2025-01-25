

import dexprice.modules.proxy.proxymultitheread as proxymultitheread

import dexprice.modules.db.insert_db as insert_db
import time

import dexprice.modules.allmodules.geckpricehistory as geckpricehistory



def gettheovhl(db_folder, db_name):

    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    timeframe = "minute"  # 可选值: day, hour, minute
    aggregate = "5"  # 聚合时间段 5min k-line
    geck_limit = 30  # 我们检查5-10h之内的，因此limit提高到了10h。
    tokendata = db.readdbtoken()

    # 初始化字典，用链名作为键，地址列表作为值
    chain_addresses = {
        'solana': [],
        'base': [],
        'ethereum': [],
        'bsc': []
    }

    # 遍历 token_new，根据链名将地址加入对应的列表
    for token in tokendata:
        # 确保 token.chainid 是链名，并存在于字典的键中
        if token.chainid in chain_addresses:
            chain_addresses[token.chainid].append(token.pair_address)  # 添加地址到对应链的列表
    current_timestamp = int(time.time())
    before_timestamp = str(current_timestamp)  # 当前时间的时间戳

    clash_api_url = "http://127.0.0.1:9097"
    headers = {"Authorization": "Bearer 123"}

    startport = 50000
    proxys = proxymultitheread.get_one_ip_proxy_multithread(startport, clash_api_url, headers)

    for chain, pairaddresses in chain_addresses.items():
        print(f"we check Chain: {chain} ")
        if chain == "ethereum":
            chainid = 'eth'
        else:
            chainid = chain
        geckpricehistory.inserthistorywithgeck_db(db, pairaddresses, chainid, proxys, timeframe, aggregate,
                                                  before_timestamp, geck_limit)

    db.close()