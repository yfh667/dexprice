
import requests
import dexprice.modules.PriceMonitor.dexscreen_priceapi as dexscreen_priceapi
from dexprice.modules.utilis.define import Config,TokenInfo

# 示例使用

import sys
import os

import dexprice.modules.utilis.findroot as findroot
import dexprice.modules.db.insert_db as insert_db
import  dexprice.modules.utilis.define as define

import dexprice.modules.db.insert_db as insert_db

import dexprice.modules.PriceMonitor.dexscreen_priceapi as dexscreen_priceapi
def WriteNewPair2db(chain_id,pairaddress):
   #  chain_id = "solana"



    db_folder = '/home/yfh/Desktop/Data/NewPair'   # 数据库存储文件夹


    db_name = "newpair"+'.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    print(f"we check {pairaddress}")
    tmp =  dexscreen_priceapi.Get_Token_Dexscreen(define.Config.DEXS,chain_id, pairaddress, 7890)

    if(tmp):
      #  print("we find")
        ca = tmp[0].address
     #   print(ca)
        cas = []
        cas.append(ca)
        tokeninfo2 = dexscreen_priceapi.Get_Token_Dexscreen(define.Config.DEXCA, '', cas, 7890)

        db.insert_multiple_tokeninfo(tokeninfo2)


    db.close()
    db_name = "beifen"+'.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    if(tokeninfo2):
        db.insert_multiple_tokeninfo(tokeninfo2)
    db.close()



WriteNewPair2db('solana',['6eBx4MP9f9VbjrZrDYJitR6QfYhZ1NVg3c7wkZiwCowS'])