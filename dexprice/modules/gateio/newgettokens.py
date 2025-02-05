
# coding: utf-8
import requests
import dexprice.modules.utilis.timedefine as timedefine
import dexprice.modules.utilis.define as define
import dexprice.modules.mexc.getalltoken as getalltoken
import dexprice.modules.cexdb.cexdb as cexdb

import dexprice.modules.utilis.define as define
import os
import dexprice.modules.utilis.findroot as findroot
import dexprice.modules.mexc.initial_timesta as initial_timesta
import dexprice.modules.mexc.initial_timesta_parall as initial_timesta_parall
import dexprice.modules.proxy.proxymultitheread as proxymultitheread
host = "https://api.gateio.ws"
prefix = "/api/v4"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

url = '/futures/usdt/contracts'
query_param = ''
r = requests.request('GET', host + prefix + url, headers=headers)
# print(r.json())
t = r.json()

tokens = []
for item in t:
    name = item['name']
    created_at = item['create_time']
    time = timedefine.timestamp_to_datetime(created_at)
    token = define.CexTokenInfo(
                        name=name,  # Token name (string)
                        chainid='USDT',  # Chain ID (string)
                        creattime=time
                    )
    tokens.append(token)

print(tokens)
current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = findroot.find_project_root(current_dir)
DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

db_folder = DATA_FOLDER + '/cex'  # 数据库存储文件夹
db_name = "gateio" + '.db'  # 数据库文件名
db = cexdb.CexSQLiteDatabase(db_folder, db_name)

db.connect()
db.insert_Multidata(tokens)
# 打印实例属性

db.close()