
import modules.db.insert_db as insert_db


import modules.utilis.define as define
import modules.strategy.deadcoin as deadcoin



if __name__ == "__main__":


    chain_id = "solana"




    db_folder = '/home/yfh/Desktop/mywork/pgp2/bestdex/DexPrice/Data'  # 数据库存储文件夹
    db_name = 'solana_db.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder, db_name,chain_id)
    db.connect()
    #  1. we need fecth all the token in the db
    token_new = db.readdbtoken()
    #  print(token_new)
    # 2.second we need put our strategy on the coin,we specific the tokenid
    tokenvalue = []
    for token in token_new:
        tokenprice = insert_db.retrieve_token_price_history(db,token)
        #  print(tokenprice)
        if(deadcoin.deadallday(tokenprice)):
            tokenvalue.append(token.tokenid)
          #  print("tokenid is",token.tokenid)
        else:
            print("no")



    print(tokenvalue)
    print(len(tokenvalue))  # 打印 tokenvalue 的长度（元素个数）
    filter_token = insert_db.read_token_andid(db,tokenvalue)
    print(filter_token)
    # 关闭数据库连接
    db.close()




