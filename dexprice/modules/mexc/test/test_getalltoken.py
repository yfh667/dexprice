import dexprice.modules.mexc.getalltoken as getalltoken
import dexprice.modules.cexdb.cexdb as cexdb

import dexprice.modules.utilis.define as define
import os
import dexprice.modules.utilis.findroot as findroot

if __name__ == '__main__':


    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = findroot.find_project_root(current_dir)
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

    db_folder = DATA_FOLDER + '/cex'  # 数据库存储文件夹
    db_name = "cexmain" + '.db'  # 数据库文件名
    db = cexdb.CexSQLiteDatabase(db_folder, db_name)

    db.connect()
    # 创建一个 Tokendb 实例


    # token = define.CexTokenInfo(
    #     name="ETH",  # Token name (string)
    #     chainid="USD",  # Chain ID (string)
    #
    # )
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
    db.insert_Multidata(tokens)
    # 打印实例属性

    db.close()