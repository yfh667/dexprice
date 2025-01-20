import threading
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
import sqlite3
import threading
import time
import math
from queue import Queue, Empty
from tqdm import tqdm

import threading

class CexDatabaseReadTaskManager:
    def __init__(self, token_ids, db_path  ,max_threads=5):
        self.task_queue = Queue()
        self.results = []
        self.result_lock = threading.Lock()
        self.add_tasks(token_ids)
        self.db_path = db_path
        self.max_threads = max_threads
        self.stop_event = threading.Event()
        self.threads = []
        self.progress_lock = threading.Lock()
        self.batch_size = 1
        self.total_tasks = math.ceil(len(token_ids) / self.batch_size)
        self.progress_bar = tqdm(total=self.total_tasks, desc="Database Read Total Progress")

    def add_tasks(self, token_ids):
        for token_id in token_ids:
            self.task_queue.put(token_id)

    def worker(self):
        while not self.stop_event.is_set():
            try:
                token_id = self.task_queue.get(timeout=1)
                result = self.process_task(token_id)
                with self.result_lock:
                    self.results.append(result)
                self.task_queue.task_done()
                with self.progress_lock:
                    self.progress_bar.update(1)  # 每完成一个任务，更新进度条
            except Empty:
                break

    def process_task(self, token_id):
        # 每个线程创建自己的数据库连接
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            # 使用 f-string 拼接表名
            query = f"SELECT * FROM  price_history WHERE tokenid = ?"
            cursor.execute(query, (token_id,))
            rows = cursor.fetchall()
            return (token_id, rows)
        finally:
            cursor.close()
            conn.close()


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
        return self.results
