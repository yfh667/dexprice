
import dexprice.modules.utilis.define as define
import dexprice.modules.db.insert_db as insert_db
import time
from datetime import datetime, timedelta

# Assuming `OvhlFromDex` is defined in `define`
import os
import dexprice.modules.utilis.findroot as findroot

results1 = define.OvhlFromDex(
    pairaddress="FjWirfWNzcD3VZza2GSnotxivC4vEp7mXbCfEy4ekSu5",
    open=0.000123173850720194,
    high=0.00012411600564690744,
    low=0.000123173850720194,
    close=0.00012411600564690744,
    time=datetime(2024, 11, 15, 12, 0, 0),  # Convert to a datetime object
    volume=16.893328525477497
)


results = []

results.append(results1)
chain_id = "solana"
current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = findroot.find_project_root(current_dir)
DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

db_folder = DATA_FOLDER+'/Project'   # 数据库存储文件夹
db_name = "gecktest"+'.db'  # 数据库文件名
db = insert_db.SQLiteDatabase(db_folder, db_name,"solana")
db.connect()
token_price_history_list = db.collect_ovhl_data(results)
# 批量插入数据
db.insert_multiple_price_history(token_price_history_list)
db.close()
