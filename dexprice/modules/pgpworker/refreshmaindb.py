
import dexprice.modules.allmodules.refreshmaindb as dexrefreshmaindb
from dexprice.modules.utilis.define import FilterCriteria
import dexprice.modules.PriceMonitor.tokenflitter as tokenflitter
import dexprice.modules.db.insert_db as insert_db

import dexprice.modules.tg.mexctg as mexctg
import dexprice.modules.utilis.define as define
import dexprice.modules.db.insert_db as insert_db
import time
import dexprice.modules.db.multidb as multidb
import dexprice.modules.tg.tgbot as tgbot
import dexprice.modules.strategy.basefunction as  basefunction

import  dexprice.modules.pgpworker.senddb as senddb
def refreshmaindb(db_folder,db_name,criteria: FilterCriteria,send_dbname):
    # we need refresh the whole db
    # criteria = FilterCriteria(
    #     liquidity_usd_min=10000,
    #     liquidity_usd_max=None,
    #     fdv_min=10000,
    #     fdv_max=None,
    #     pair_age_min_hours=None,
    #     pair_age_max_hours= None,
    #     txn_buy=10,
    #     txn_sell=10,
    #     volume=10000
    #    )

    tokennew = dexrefreshmaindb.refresh_database(db_name, db_folder, criteria)
    token_5m = []



    # here we get the token that satisfied the fdv>5m
    criteria2 = FilterCriteria(
        liquidity_usd_min=10000,
        liquidity_usd_max=None,
        fdv_min=5000000,
        fdv_max=50000000,
        pair_age_min_hours=None,
        pair_age_max_hours= None,
        txn_buy=10000,
        txn_sell=10000,
        volume=100000
       )
    for token in tokennew:
        if (tokenflitter.normal_token_filter(token, criteria2)):
            if (token.creattime == '1970-01-01 00:00:00'):
                pass
            else:
                token_5m.append(token)
    if(len(token_5m) > 0):
        db = insert_db.SQLiteDatabase(db_folder, db_name)
        db.connect()
        find_address  = [ ]
        for token in token_5m:
            pairaddress = token.pair_address
            tokenid = db.FindParetokenid(pairaddress)
            tokendb = db.read_token_withid(tokenid)
            senddb.insertsenddb(db_folder, send_dbname, tokendb)
            db.delete_token(pairaddress)
            find_address.append(pairaddress)

        string = ''
        for address in find_address:
            string = string+'\n'+str(address)

        mexctg.longstring("@jingou26", string)

    #    print(token.address)
    #print(token_5m)








