import time
import threading
import math
from token_bucket import Limiter, MemoryStorage
from dexprice.modules.utilis.define import Config

from dexprice.modules.PriceMonitor.dexscreen_priceapi import Get_Token_Dexscreen  # 导入类
from tqdm import tqdm
import threading
import math
from queue import Queue
#
class DexscreenApiManager:
    def __init__(self):
        self.results_geck = []
        self.result_mutex_geck = threading.Lock()
        self.failed_tasks = Queue()  # 添加一个队列用于管理失败的任务

    def multi_get_price_dexscreen(self, sourcetype, limiter, thread_id, chain_id, pair_addresses, proxy_port, progress_bar, progress_lock, thread_progress_bar,progress_callback=None):

        if sourcetype==Config.DEXS:
            max_batch_size = 30
        else:
            max_batch_size = 1
        total_addresses = len(pair_addresses)
        num_batches = math.ceil(total_addresses / max_batch_size)
        # print(f"Thread {thread_id}: begin work ")

        for i in range(num_batches):
            start = i * max_batch_size
            end = min(start + max_batch_size, total_addresses)
            batch = pair_addresses[start:end]

            while True:
                if limiter.consume("api_call", 1):
                    # 获取数据

                    tokens_info = Get_Token_Dexscreen(sourcetype, chain_id, batch, proxy_port)
                    if tokens_info == "FAILED":
                        # 如果请求失败，将任务重新放回队列并等待一段时间后重试
                        print(f"Thread {thread_id}: Request failed for batch {batch}. Adding to retry queue.")
                        self.failed_tasks.put(batch)  # 将失败的任务批次放回失败任务队列
                        time.sleep(2)  # 等待一段时间后继续处理其他任务
                        break  # 跳出当前循环以处理下一个任务或重新尝试
                  #  print(f"tokens_info{tokens_info}")
                    else:
                        with self.result_mutex_geck:
                            self.results_geck.append(tokens_info)

                        # 更新线程自己的进度条
                        thread_progress_bar.update(len(batch))

                        # 更新总的进度条
                        with progress_lock:
                            progress_bar.update(len(batch))
                            # if progress_callback:
                            #      progress_callback(progress_bar.n / progress_bar.total * 100)  # 将总进度传递给回调
                            if progress_callback:
                                progress_percentage = progress_bar.n / progress_bar.total * 100
                                print(f"Progress updated to: {progress_percentage}%")
                                progress_callback(progress_percentage)


                        break  # 成功处理后跳出循环
                else:
                    # print(f"Thread {thread_id}: No bucket token available for batch {i}")
                    time.sleep(0.1)  # 等待一段时间后重试
        if not self.failed_tasks.empty():
            failed_thread = threading.Thread(target=self.retry_failed_tasks, args=(sourcetype, chain_id, proxy_port, progress_bar, progress_lock, progress_callback))
            failed_thread.start()
            failed_thread.join()


    def multi_get_token_dexscreen(self, sourcetype, addresses, chain_id, num_threads, proxy_ports, rate, capacity, progress_callback=None):
        port_count = len(proxy_ports)
        threads_per_port = num_threads // port_count
        remaining_threads = num_threads % port_count

        threads = []
        self.results_geck.clear()  # 清空之前的结果

        total_addresses = len(addresses)
        progress_bar = tqdm(total=total_addresses, desc="Total Progress", position=0)

        # 为了在线程之间共享进度，需要一个线程安全的计数器
        progress_lock = threading.Lock()

        # 修改目标函数，使其在处理每个地址后更新进度条
        def thread_target(sourcetype, limiter, thread_id, chain_id, thread_addresses, proxy_port):
            # 为每个线程创建自己的进度条
            thread_progress_bar = tqdm(total=len(thread_addresses), desc=f"Thread {thread_id}", position=thread_id+1)
            self.multi_get_price_dexscreen(sourcetype, limiter, thread_id, chain_id, thread_addresses, proxy_port, progress_bar, progress_lock, thread_progress_bar, progress_callback)
            # 线程完成后关闭自己的进度条
            thread_progress_bar.close()

        thread_id = 0
        for port_index, proxy_port in enumerate(proxy_ports):
            # 为每个端口分配线程数量
            storage = MemoryStorage()
            limiter = Limiter(rate, capacity, storage)

            assigned_threads = threads_per_port + (1 if remaining_threads > 0 else 0)
            if remaining_threads > 0:
                remaining_threads -= 1

            # 根据分配的线程数量来划分地址
            addresses_per_thread = math.ceil(len(addresses) / num_threads)
            for _ in range(assigned_threads):
                start = thread_id * addresses_per_thread
                if start >= len(addresses):
                    break
                end = min(start + addresses_per_thread, len(addresses))
                thread_addresses = addresses[start:end]

                # 启动线程，使用新的目标函数
                thread = threading.Thread(target=thread_target,
                                          args=(sourcetype, limiter, thread_id, chain_id, thread_addresses, proxy_port))
                threads.append(thread)
                thread.start()
                thread_id += 1

        for thread in threads:
            thread.join()

        progress_bar.close()
        return self.results_geck