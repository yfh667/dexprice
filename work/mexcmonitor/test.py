import dexprice.modules.mexc.getalltoken as getalltoken
import dexprice.modules.cexdb.cexdb as cexdb
import dexprice.modules.tg.tgbot as tgbot
import dexprice.modules.tg.mexctg as mexctg
import dexprice.modules.utilis.define as define
import dexprice.modules.utilis.define as define
import os
import dexprice.modules.utilis.findroot as findroot
import time
import threading
import dexprice.modules.mexc.getalltoken as getalltoken
import dexprice.modules.cexdb.cexdb as cexdb

import dexprice.modules.utilis.define as define
import os
import dexprice.modules.utilis.findroot as findroot
import dexprice.modules.mexc.initial_timesta as initial_timesta
import dexprice.modules.mexc.initial_timesta_parall as initial_timesta_parall
import dexprice.modules.proxy.proxymultitheread as proxymultitheread


def find_added_and_deleted_tokens(tokenlocal, tokennew):
    # Find added tokens
    tokenlocalname = []
    for token in tokenlocal:
        tokenlocalname.append(token.name)
    tokennewname = []

    for token in tokennew:
        name = token.name
        tokennewname.append(name)

    if(not len(tokennewname)):
        return [],[]
    # 将 tokenlocalname 转为 set，避免每次循环都遍历整个列表
    tokenlocalname_set = set(tokenlocalname)

    added_tokens = []
    for token in tokennew:
        if token.name.endswith('USDT'):
            if token.name not in tokenlocalname_set:
                added_tokens.append(token)





    return added_tokens
def tokendbtotokeninfo(tokendb):
    tokens = []
    for token in tokendb:
        tokeninfo = define.CexTokenInfo(
            name=token.name,
            chainid=token.chainid,
            creattime=token.creattime,

        )
        tokens.append(tokeninfo)
    return tokens
def readtoken(db_name,db_folder):
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # PROJECT_ROOT = findroot.find_project_root(current_dir)
    # DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")
    #
    # db_folder = DATA_FOLDER + '/cex'  # 数据库存储文件夹
  #  db_name = "cexmain" + '.db'  # 数据库文件名
    db = cexdb.CexSQLiteDatabase(db_folder, db_name)

    db.connect()
    # 创建一个 Tokendb 实例
    tokens = db.readdbtoken()
    db.close()
    return tokens

def ten_min_cycle(db_folder,db_name):
    while True:
        db = cexdb.CexSQLiteDatabase(db_folder, db_name)

        db.connect()
        tokenlocal = tokendbtotokeninfo(readtoken(db_name,db_folder))

        symbol = getalltoken.getalltoken()
        # symbol  = ['BTC','SOL']
        tokens = []

        rate = 0.3
        capacity = 20
        max_threads_per_proxy = 1
        clash_api_url = "http://127.0.0.1:9097"
        headers = {"Authorization": "Bearer 123"}

        startport = 50000

        proxys = proxymultitheread.get_one_ip_proxy_multithread(startport, clash_api_url, headers)

        task_manager = initial_timesta_parall.MexcTaskManager(
            symbol,
            proxys,
            rate,
            capacity,
            max_threads_per_proxy,

        )
        tokennew, failed_tasks = task_manager.run()

        added_tokens = find_added_and_deleted_tokens(tokenlocal, tokennew)
        if(not len(added_tokens)):
            time.sleep(600)  # 10分钟
            continue
        # 1. we need find the added token
        # it is the add_tokens
       # added_tokens = list(set(added_tokens))


        # we need insert the add_tokens in the db
        token_infos = []

        for token in added_tokens:
            token_info = define.CexTokenInfo(
               name =  token.name,
                chainid='USDT',
                creattime=token.creattime,
            )
            token_infos.append(token_info)
        db.insert_Multidata(token_infos)
        mexctg.mexctg2( "@jingou24", token_infos)



        print(f"added_tokens is {added_tokens}")


        db.close()

        time.sleep(600)  # 10分钟
if __name__ == '__main__':


    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = findroot.find_project_root(current_dir)
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

    db_folder = DATA_FOLDER + '/cex'  # 数据库存储文件夹
    db_name = "send_cexmain" + '.db'  # 数据库文件名



    ten_min_cycle(db_folder,db_name)


