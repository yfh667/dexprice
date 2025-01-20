# Example usage with PostgreSQL
# Database configuration dictionary
from dexprice.modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类
from dexprice.modules.utilis.define import Config,TokenInfo
import  dexprice.modules.utilis.define as define
from dexprice.modules.db.create_db import initialize_table
import dexprice.modules.db.insert_db as insert_db
import dexprice.modules.allmodules.geckpricehistory as geckpricehistory
import dexprice.modules.db.postsql as postsql
import dexprice.modules.db.multidb2 as multidb2
db_config = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'solana10days',
    'user': 'yfh',
    'password': 'yfh'
}


token_ids = [1]  # Replace with your actual token IDs

chainid = 'solana'

# Initialize the PostgreSQL adapter
postgres_adapter = multidb2.PostgreSQLAdapter(db_config, chainid)

# Initialize the task manager with the adapter
task_manager = multidb2.DatabaseReadTaskManager(token_ids, postgres_adapter, max_threads=5)

# Run the task manager
results = task_manager.run()

# Process the results
for result in results:
    print(f"Token ID: {result}")