
import dexprice.modules.db.multidb   as multidb
# 假设您的数据库路径为 'your_database.db'
db_path = '/home/yfh/Desktop/MarketSystem/Data/Project/solana_100kover.db'
# 需要读取的 token_id 列表
token_ids = [1,8,9,90]

task_manager = multidb.DatabaseReadTaskManager(token_ids, db_path,'solana', max_threads=5)
results = task_manager.run()

# 处理结果
for token_id, rows in results:
    print(f"Token ID: {token_id}, Rows: {rows}")
