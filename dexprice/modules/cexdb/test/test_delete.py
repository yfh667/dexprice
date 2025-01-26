import dexprice.modules.cexdb.cexdb as cexdb
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
    tokens = db.readdbtoken()

    #print(tokens)
    # for token in tokens:
    #     print(token)
    delete_tone = tokens[0]
    delete_token_name= tokens[0].name
    db.delete_token(delete_token_name)
    db.close()