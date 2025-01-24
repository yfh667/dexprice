import requests
import dexprice.modules.PriceMonitor.dexscreen_priceapi as dexscreen_priceapi
from dexprice.modules.utilis.define import Config,TokenInfo

# 示例使用

import sys
import os
import dexprice.modules.utilis.define as define
import dexprice.modules.utilis.findroot as findroot
import dexprice.modules.db.insert_db as insert_db

def havesend(db_folder,db_name,caaddress):

    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()


    if db.check_ca_exists(caaddress):
        return  1
    #   represent we have send the token,so we can;t repulite
    else:
        return 0
     #

def insertsenddb(db_folder,db_name,tokendb:define.Tokendb):
    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    tokendbs = []
    tokendbs.append(tokendb)
    db.insert_multiple_tokeninfo2(tokendbs)
    db.close()

