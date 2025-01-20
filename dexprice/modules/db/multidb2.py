import threading
from queue import Queue, Empty
import sqlite3
import psycopg2
from psycopg2 import sql
import time
import math
from tqdm import tqdm
from abc import ABC, abstractmethod
import psycopg2.pool

# 定义抽象基类 DatabaseAdapter
class DatabaseAdapter(ABC):
    @abstractmethod
    def execute_query(self, token_ids):
        pass

    @abstractmethod
    def close(self):
        pass

# SQLiteAdapter 实现
class SQLiteAdapter(DatabaseAdapter):
    def __init__(self, db_path, chainid):
        self.db_path = db_path
        self.chainid = chainid

    def execute_query(self, token_ids):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            placeholders = ','.join('?' for _ in token_ids)
            query = f"SELECT * FROM {self.chainid}_price_history WHERE tokenid IN ({placeholders})"
            cursor.execute(query, token_ids)
            rows = cursor.fetchall()
            return rows
        finally:
            cursor.close()
            conn.close()

    def close(self):
        pass

# PostgreSQLAdapter 实现，使用连接池
class PostgreSQLAdapter(DatabaseAdapter):
    def __init__(self, db_config, chainid, minconn=1, maxconn=10):
        self.db_config = db_config
        self.chainid = chainid
        self.pool = psycopg2.pool.ThreadedConnectionPool(minconn, maxconn, **db_config)

    def execute_query(self, token_ids):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        try:
            query = sql.SQL("SELECT * FROM {} WHERE tokenid = ANY(%s)").format(
                sql.Identifier(f"{self.chainid}_price_history")
            )
            cursor.execute(query, (token_ids,))
            rows = cursor.fetchall()
            return rows
        finally:
            cursor.close()
            self.pool.putconn(conn)

    def close(self):
        self.pool.closeall()

# DatabaseReadTaskManager 实现
class DatabaseReadTaskManager:
    def __init__(self, token_ids, db_adapter, max_threads=5, batch_size=100):
        self.task_queue = Queue()
        self.results = []
        self.result_lock = threading.Lock()
        self.add_tasks(token_ids, batch_size)
        self.db_adapter = db_adapter
        self.max_threads = max_threads
        self.stop_event = threading.Event()
        self.progress_lock = threading.Lock()
        self.total_tasks = math.ceil(len(token_ids) / batch_size)
        self.progress_bar = tqdm(total=self.total_tasks, desc="Database Read Total Progress")

    def add_tasks(self, token_ids, batch_size):
        for i in range(0, len(token_ids), batch_size):
            batch = token_ids[i:i + batch_size]
            self.task_queue.put(batch)

    def worker(self):
        while not self.stop_event.is_set():
            try:
                token_ids_batch = self.task_queue.get(timeout=1)
                result = self.process_task(token_ids_batch)
                with self.result_lock:
                    self.results.extend(result)
                self.task_queue.task_done()
                with self.progress_lock:
                    self.progress_bar.update(1)
            except Empty:
                break

    def process_task(self, token_ids_batch):
        return self.db_adapter.execute_query(token_ids_batch)

    def run(self):
        threads = []
        for _ in range(self.max_threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            threads.append(thread)
        # 等待所有任务完成
        self.task_queue.join()
        # 停止所有线程
        self.progress_bar.close()
        self.stop_event.set()
        for thread in threads:
            thread.join()
        # 关闭数据库连接池或连接
        self.db_adapter.close()
        return self.results

# # 使用示例
# if __name__ == "__main__":
#     # 请根据需要选择 SQLite 或 PostgreSQL
#
#     # 示例 token_ids 列表
#     token_ids = [1, 2, 3, 4, 5]  # 请替换为您的实际 token_id 列表
#
#     # 对于 SQLite
#     db_path = 'path/to/your/sqlite.db'
#     chainid = 'your_chain_id'
#     sqlite_adapter = SQLiteAdapter(db_path, chainid)
#     task_manager = DatabaseReadTaskManager(token_ids, sqlite_adapter, max_threads=5, batch_size=100)
#     results = task_manager.run()
#     for row in results:
#         print(row)
#
#     # 对于 PostgreSQL
#     """
#     db_config = {
#         'host': 'localhost',
#         'port': 5432,
#         'dbname': 'your_database_name',
#         'user': 'your_username',
#         'password': 'your_password'
#     }
#     chainid = 'your_chain_id'
#     postgres_adapter = PostgreSQLAdapter(db_config, chainid, minconn=1, maxconn=10)
#     task_manager = DatabaseReadTaskManager(token_ids, postgres_adapter, max_threads=5, batch_size=100)
#     results = task_manager.run()
#     postgres_adapter.close()
#     for row in results:
#         print(row)
#     """
