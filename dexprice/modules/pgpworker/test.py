
from dexprice.modules.utilis.define import FilterCriteria
import dexprice.modules.proxy.proxymultitheread as proxymultitheread
import dexprice.modules.OHLCV.geck_parrel as geck_parrel
import dexprice.modules.utilis.define as define
import dexprice.modules.db.insert_db as insert_db
import time
import dexprice.modules.db.multidb as multidb
import dexprice.modules.tg.tgbot as tgbot
import dexprice.modules.strategy.basefunction as  basefunction
import threading
import dexprice.modules.allmodules.realtoken as realtoken
import dexprice.modules.allmodules.refreshmaindb as dexrefreshmaindb
import dexprice.modules.allmodules.geckpricehistory as geckpricehistory
Proxyport =7890
def try_delete_table_with_retry(db, retries=3, delay=5):
    for attempt in range(retries):
        try:
            db.delete_table2()
            print("Table deleted successfully.")
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Could not delete table.")
                return False

def read_from_newpair():
    db_folder = '/home/yfh/Desktop/Data/NewPair'  # 数据库存储文件夹
    db_name = "newpair" + '.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    token_new = db.readdbtoken()
    db.close()
    # read and we need delete the token in the newpairdb
    success = try_delete_table_with_retry(db)
    if(success):
        print("Table successfully deleted.")
    return token_new

def write_maindb(token_new):
    criteria = FilterCriteria(
        liquidity_usd_min=10000,
        liquidity_usd_max=None,
        fdv_min=10000,
        fdv_max=None,
        pair_age_min_hours=None,
        pair_age_max_hours= None,
        txn_buy=10,
        txn_sell=10,
        volume=10000
       )
  # 添加地址到对应链的列表
    tokenreal = realtoken.extract_valid_tokens(token_new,criteria)

    db_folder_main = '/home/yfh/Desktop/Data/Maindb'  # 数据库存储文件夹
    db_name_main = "main" + '.db'  # 数据库文件名
    db_main = insert_db.SQLiteDatabase(db_folder_main, db_name_main)
    db_main.connect()
    db_main.insert_multiple_tokeninfo(tokenreal)
    db_main.close()


def refreshmaindb():
    # we need refresh the whole db
    criteria = FilterCriteria(
        liquidity_usd_min=10000,
        liquidity_usd_max=None,
        fdv_min=10000,
        fdv_max=None,
        pair_age_min_hours=None,
        pair_age_max_hours= None,
        txn_buy=10,
        txn_sell=10,
        volume=10000
       )

    db_folder = '/home/yfh/Desktop/Data/Maindb'  # 数据库存储文件夹
    db_name =   'main.db'  # 数据库文件名
    dexrefreshmaindb.refresh_database(db_name, db_folder, criteria)
    tgbot.sendmessage_chatid("@jingou22","refresh token",Proxyport)


def strategy():
    db_folder = '/home/yfh/Desktop/Data/Maindb'  # 数据库存储文件夹
    db_name =   'main.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    tokens = db.readdbtoken()
    ## 读取token的历史数据，进行处理
    db_path = db_folder + '/'  + 'main.db'
    requestedtokenid = []
    for token in tokens:
        requestedtokenid.append(token.tokenid)

    task_manager = multidb.DatabaseReadTaskManager(requestedtokenid, db_path, max_threads=5)
    results = task_manager.run()
    tokenhistorys = []
    # 处理结果
    for token_id, rows in results:
        tokenhistory = []
        for row in rows:
            test = define.TokenPriceHistory(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            tokenhistory.append(test)
        tokenhistorys.append(tokenhistory)
    find_address = []
    for tokenhistory in tokenhistorys:
        if (len(tokenhistory) > 1):
            tokenhistory = basefunction.sort_by_time(tokenhistory)
            if tokenhistory[-1].close > 0.8 * tokenhistory[0].open:
                for i in range(1, len(tokenhistory)):
                    token = tokenhistory[i]
                    if (token.high > 5 * token.low):
                        # 我么需要判断是涨还是跌
                        if (token.close > token.open):
                            tokenid = tokenhistory[0].tokenid
                            tokendb = db.read_token_withid(tokenid)
                            pairaddress = tokendb.pair_address
                            tgbot.sendmessage(pairaddress, Proxyport)
                            db.delete_token(pairaddress)
                            find_address.append(pairaddress)

    # 输出前的去重操作。
    unique_find_address = list(set(find_address))
    for address in unique_find_address:
        print(address)
    db.close()

# get the ovhl data and inset to the maindb
def gettheovhl():
    db_folder = '/home/yfh/Desktop/Data/Maindb'  # 数据库存储文件夹
    db_name =   'main.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    timeframe = "hour"  # 可选值: day, hour, minute
    aggregate = "1"  # 聚合时间段 5min k-line
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

def refresh():
    while True:
        print("\nrefresh 10-minute cycle...")
        refreshmaindb()
        time.sleep(300)  # 5min

def ten_min_cycle():
    while True:
        print("\nStarting 10-minute cycle...")
        tokennew = read_from_newpair()
        write_maindb(tokennew)
        time.sleep(600)  # 10分钟

def thirty_min_cycle():
    while True:
        print("\nStarting 30-minute cycle...")
        gettheovhl()
        strategy()
        time.sleep(1800)  # 30分钟

if __name__ == "__main__":
    # 使用多线程分别运行 10 分钟和 30 分钟的任务
    ten_min_thread = threading.Thread(target=ten_min_cycle)
    refresh_thread = threading.Thread(target=refresh)
    thirty_min_thread = threading.Thread(target=thirty_min_cycle)

    ten_min_thread.start()
    thirty_min_thread.start()
    refresh_thread.start()


    ten_min_thread.join()
    thirty_min_thread.join()
    refresh_thread.join()

