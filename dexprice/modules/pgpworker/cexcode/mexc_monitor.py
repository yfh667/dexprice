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
def getnew():
    symbol = getalltoken.getalltoken()
    tokens = []
    for symbol in symbol:
        token_parts = symbol.split('_')
        name = token_parts[0]
        chaind = token_parts[1]
        token = define.CexTokenInfo(
            name=name,  # Token name (string)
            chainid=chaind,  # Chain ID (string)

        )
        tokens.append(token)
    return tokens
def find_added_and_deleted_tokens(tokenlocal, tokennew):
    # Find added tokens
    tokenlocalname = []
    for token in tokenlocal:
        tokenlocalname.append(token.name)
    tokennewname = []
    for token in tokennew:
        tokennewname.append(token.name)


    added_tokens = [token for token in tokennewname if token not in tokenlocalname]

    # Find deleted tokens
    deleted_tokens = [token for token in tokenlocalname if token not in tokennewname]



    return added_tokens, deleted_tokens
def tokendbtotokeninfo(tokendb):
    tokens = []
    for token in tokendb:
        tokeninfo = define.CexTokenInfo(
            name=token.name, chainid=token.chainid,

        )
        tokens.append(tokeninfo)
    return tokens
def readtoken(db_folder,db_name):
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # PROJECT_ROOT = findroot.find_project_root(current_dir)
    # DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")
    #
    # db_folder = DATA_FOLDER + '/cex'  # 数据库存储文件夹
    # db_name = "cexmain" + '.db'  # 数据库文件名
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
        tokenlocal = tokendbtotokeninfo(readtoken(db_folder,db_name))
        tokennew = getnew()
        added_tokens, deleted_tokens = find_added_and_deleted_tokens(tokenlocal, tokennew)
        # 1. we need find the added token
        # it is the add_tokens
        added_tokens = list(set(added_tokens))
        # we need insert the add_tokens in the db
        token_infos = []
        for token in added_tokens:
            token_info = define.CexTokenInfo(
               name =  token,
                chainid='USDT',
            )
            token_infos.append(token_info)
        db.insert_Multidata(token_infos)
        mexctg.mexctg2( "@jingou24", token_infos)

        deleted_tokens = list(set(deleted_tokens))
        token_infos = []
        for token in deleted_tokens:
            token_info = define.CexTokenInfo(
               name =  token,
                chainid='USDT',
            )
            token_infos.append(token_info)
        mexctg.mexctg2( "@jingou25", token_infos)

        for token in deleted_tokens:
            delete_token_name = token
            db.delete_token(delete_token_name)

        print(f"added_tokens is {added_tokens}")
        print(f"deleted_tokens is {deleted_tokens}")


        db.close()

        time.sleep(3600)  # 10分钟
if __name__ == '__main__':


    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = findroot.find_project_root(current_dir)
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

    db_folder = DATA_FOLDER + '/cex'  # 数据库存储文件夹
    db_name = "cexmain" + '.db'  # 数据库文件名
    


    ten_min_cycle(db_folder,db_name)

    #ten_min_thread.join()

  #   for i in range(1):
  #      # tokenlocal = readtoken()
  #
  #
  #   # we need find the delete token
  #       #it is the deleted tokens
  #
  #
  # #  db.insert_Multidata(tokens)
  #   # 打印实例属性

