
import  dexprice.modules.utilis.define as define

import dexprice.modules.db.insert_db as insert_db

import dexprice.modules.PriceMonitor.dexscreen_priceapi as dexscreen_priceapi

def WriteNewPair2db(chain_id,pairaddress):



  #  chain_id = "solana"
    db_folder = '/home/yfh/Desktop/MarketSystem/Data/NewPair'   # 数据库存储文件夹

    db_name = chain_id+"newpair2"+'.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name,chain_id)
    db.connect()
   # pairaddress = ['7TkVaEEG8CpMutTpkQMGDEdsRi1GxnjA1NzKiTPKbxnE']
    tokeninfo =  dexscreen_priceapi.Get_Token_Dexscreen(define.Config.DEXS,chain_id, pairaddress, 7897)
    cairaddress = []
    cairaddress.append(tokeninfo[0].address)
    tokens_info = dexscreen_priceapi.Get_Token_Dexscreen(define.Config.DEXCA,chain_id, cairaddress, 7897)
    pairaddress2 = []
    pairaddress2.append(tokens_info[0].pair_address)
    realtoken = dexscreen_priceapi.Get_Token_Dexscreen(define.Config.DEXS,chain_id, pairaddress2, 7897)

 #   print(realtoken)
    db.insert_multiple_tokeninfo(realtoken)
    db.close()





#
# if __name__ == "__main__":
#     chain_id = "solana"
#     pairaddress = ['Byc1iNgUsz8e7YudTyMcftGTbsgp1sUDraeDD8mQSFcw']
#
#     WriteNewPair2db(chain_id,pairaddress)

#
#
