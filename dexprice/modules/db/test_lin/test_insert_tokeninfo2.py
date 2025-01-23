import requests
import dexprice.modules.PriceMonitor.dexscreen_priceapi as dexscreen_priceapi
from dexprice.modules.utilis.define import Config,TokenInfo

# 示例使用

import sys
import os

import dexprice.modules.utilis.findroot as findroot
import dexprice.modules.db.insert_db as insert_db
if __name__ == '__main__':

    ca_addresses = ["6AJcP7wuLwmRYLBNbi825wgguaPsWzPBEHcHndpRpump"]

    proxy_port = 7890  # 示例代理端口    chain_id = "solana"  # 这里使用示例的链 ID

    tokens_info = dexscreen_priceapi.Get_Token_Dexscreen(Config.DEXCA,'', ca_addresses, proxy_port)

    tokens_infos = []
    tokens_infos.append(tokens_info)
    print(tokens_info)



    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = findroot.find_project_root(current_dir)
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

    db_folder = DATA_FOLDER +'/Project'# 数据库存储文件夹
    db_name = 'test32.db'  # 数据库文件名



    db = insert_db.SQLiteDatabase(db_folder, db_name)



    db.connect()


    db.insert_multiple_tokeninfo( tokens_info)

    # 关闭数据库连接
    db.close()
