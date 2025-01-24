import requests
import dexprice.modules.PriceMonitor.dexscreen_priceapi as dexscreen_priceapi
from dexprice.modules.utilis.define import Config,TokenInfo

# 示例使用

import sys
import os

import dexprice.modules.utilis.findroot as findroot
import dexprice.modules.db.insert_db as insert_db

current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = findroot.find_project_root(current_dir)
DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

db_folder = DATA_FOLDER + '/Project'  # 数据库存储文件夹
db_name = 'newpair.db'  # 数据库文件名

db = insert_db.SQLiteDatabase(db_folder, db_name)

db.connect()

ca = '6AJcP7wuLwmRYLBNbi825wgguaPsWzPBEHcHndpRpump'

if db.check_ca_exists(ca):
    print("CA found")
else:
    print("CA not found")