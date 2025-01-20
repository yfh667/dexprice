import queue
from typing import List

class TaskQueue:
    def __init__(self):
        # 初始化一个先进先出队列
        self.queue = queue.Queue()

    def add_task(self, addresses: List[str]):
        """将地址列表作为任务添加到队列中"""
        self.queue.put(addresses)
        print(f"Task added: {addresses}")

    def get_task(self) -> List[str]:
        """从队列中获取任务（地址列表），如果队列为空则返回 None"""
        if not self.queue.empty():
            addresses = self.queue.get()
            print(f"Task retrieved: {addresses}")
            return addresses
        else:
            print("No tasks in the queue.")
            return None

    def task_done(self):
        """标记任务完成，通知队列已完成此任务"""
        self.queue.task_done()

    def is_empty(self) -> bool:
        """检查队列是否为空"""
        return self.queue.empty()

    def size(self) -> int:
        """获取当前队列中的任务数量"""
        return self.queue.qsize()

# 测试代码
