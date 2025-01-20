import time
import threading
from token_bucket import Limiter, MemoryStorage

# 模拟实际的API调用
def simulateApiCall(limiter, thread_id, rate):
    for i in range(10):
        if limiter.consume("api_call", 1):  # 尝试消耗一个令牌
            print(f"Thread {thread_id}: Token acquired at iteration {i}")
        else:
            print(f"Thread {thread_id}: No token available at iteration {i}")
        time.sleep(0.1)

def main():
    rate = 10  # 每秒生成10个令牌
    capacity = 20  # 令牌桶的最大容量
    storage = MemoryStorage()
    limiter = Limiter(rate, capacity, storage)

    num_threads = 5  # 线程数量
    threads = []

    # 启动多个线程模拟并行API调用
    for i in range(num_threads):
        thread = threading.Thread(target=simulateApiCall, args=(limiter, i, rate))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
