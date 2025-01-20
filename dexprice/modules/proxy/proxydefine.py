from dataclasses import dataclass
from typing import Dict, List
import  time
import dexprice.modules.proxy.testproxy as testproxy
# @dataclass
# class Proxy:
#     port: int
#     ip: str
#     is_available: bool
#
# class ProxyPool:
#     def __init__(self):
#         # 使用字典来存储代理，以端口为关键参数
#         self.proxies: Dict[int, Proxy] = {}
#
#     def add_proxy(self, port: int, ip: str, is_available: bool):
#         # 添加或更新代理（如果端口已存在，则更新 IP 和可用性）
#         self.proxies[port] = Proxy(port, ip, is_available)
#
#     def update_proxy_status(self, port: int, is_available: bool):
#         # 更新指定端口的代理的可用性
#         if port in self.proxies:
#             self.proxies[port].is_available = is_available
#         else:
#             print(f"Proxy with Port: {port} not found in pool.")
#
#     def get_available_proxies(self) -> List[Proxy]:
#         # 获取所有可用的代理
#         return [proxy for proxy in self.proxies.values() if proxy.is_available]
#
#     def get_all_proxies(self) -> List[Proxy]:
#         # 获取所有代理
#         return list(self.proxies.values())
#
#     def __str__(self):
#         # 显示代理池状态
#         result = "Current Proxy Pool:\n"
#         for port, proxy in self.proxies.items():
#             status = "Available" if proxy.is_available else "Unavailable"
#             result += f"Port: {proxy.port}, IP: {proxy.ip}, Status: {status}\n"
#         return result

# 测试代码
# proxy_pool = ProxyPool()
# proxy_pool.add_proxy(50011, "127.0.0.1", True)
# proxy_pool.add_proxy(50012, "127.0.0.1", False)
# proxy_pool.add_proxy(50013, "127.0.0.2", True)
#
# # 更新代理状态
# proxy_pool.update_proxy_status(50012, True)
#
# # 获取可用代理
# available_proxies = proxy_pool.get_available_proxies()
# print("Available Proxies:", available_proxies)
#
# # 打印代理池状态
# print(proxy_pool)


import threading
from typing import Dict, List
from token_bucket import Limiter, MemoryStorage

# 定义 Proxy 类
class Proxy:
    def __init__(self, port: int, ip: str, is_available: bool = True):
        self.port = port
        self.ip = ip
        self.is_available = is_available

    def __str__(self):
        status = "Available" if self.is_available else "Unavailable"
        return f"Port: {self.port}, IP: {self.ip}, Status: {status}"

class ProxyPool:
    def __init__(self, rate: float, capacity: int, max_threads_per_proxy: int):
        self.proxies: Dict[int, Proxy] = {}  # 存储所有代理
        self.failed_proxies: List[int] = []  # 存储失效的代理端口
        self.lock = threading.RLock()  # 使用可重入锁

        self.rate = rate  # 速率限制参数
        self.capacity = capacity  # 速率限制容量
        self.max_threads_per_proxy = max_threads_per_proxy  # 每个代理的最大线程数

        self.proxy_info = {}  # 存储每个代理的限速器和信号量


    def add_proxy(self, proxy: Proxy):
        with self.lock:
            # 添加或更新代理信息
            self.proxies[proxy.port] = proxy
            if proxy.is_available:
                # 如果代理可用，创建限速器和信号量
                storage = MemoryStorage()
                limiter = Limiter(self.rate, self.capacity, storage)
                semaphore = threading.Semaphore(self.max_threads_per_proxy)
                self.proxy_info[proxy.port] = {
                    'limiter': limiter,
                    'semaphore': semaphore
                }
            print(f"Proxy {proxy.port} added to pool.")

    def update_proxy_status(self, port: int, is_available: bool):
        with self.lock:
            if port in self.proxies:
                self.proxies[port].is_available = is_available
                if is_available:
                    if port not in self.proxy_info:
                        # 如果代理变为可用，创建限速器和信号量
                        storage = MemoryStorage()
                        limiter = Limiter(self.rate, self.capacity, storage)
                        semaphore = threading.Semaphore(self.max_threads_per_proxy)
                        self.proxy_info[port] = {
                            'limiter': limiter,
                            'semaphore': semaphore
                        }
                        print(f"Proxy {port} is now available.")
                else:
                    # 如果代理不可用，移除限速器和信号量
                    if port in self.proxy_info:
                        del self.proxy_info[port]
                    print(f"Proxy {port} is now unavailable.")
            else:
                print(f"Proxy with Port: {port} not found in pool.")
    def add_proxies(self, proxies: List[Proxy]):
        with self.lock:
            for proxy in proxies:
                # 添加或更新代理信息
                self.proxies[proxy.port] = proxy
                if proxy.is_available:
                    # 如果代理可用，创建限速器和信号量
                    storage = MemoryStorage()
                    limiter = Limiter(self.rate, self.capacity, storage)
                    semaphore = threading.Semaphore(self.max_threads_per_proxy)
                    self.proxy_info[proxy.port] = {
                        'limiter': limiter,
                        'semaphore': semaphore
                    }
                print(f"Proxy {proxy.port} added to pool.")
    def acquire_proxy(self):
        with self.lock:
            for proxy in self.proxies.values():
                if proxy.is_available and proxy.port in self.proxy_info:
                    proxy_data = self.proxy_info[proxy.port]
                    semaphore = proxy_data['semaphore']
                    if semaphore.acquire(blocking=False):
                        limiter = proxy_data['limiter']
                        return proxy, limiter, semaphore
            return None, None, None  # 没有可用的代理或信号量已用完

    def release_proxy(self, proxy_port: int, semaphore):
        semaphore.release()

    def remove_proxy(self, port: int):
        with self.lock:
            if port in self.proxies:
                # 将代理标记为不可用
                self.proxies[port].is_available = False
                # 移除限速器和信号量
                if port in self.proxy_info:
                    del self.proxy_info[port]
                # 添加到失效代理列表
                if port not in self.failed_proxies:
                    self.failed_proxies.append(port)
                print(f"Proxy {port} removed from pool.")
            else:
                print(f"Proxy with Port: {port} not found in pool.")

    def get_available_proxies(self) -> List[Proxy]:
        with self.lock:
            # 获取所有可用的代理
            return [proxy for proxy in self.proxies.values() if proxy.is_available]

    def get_all_proxies(self) -> List[Proxy]:
        with self.lock:
            # 获取所有代理
            return list(self.proxies.values())

    def __str__(self):
        with self.lock:
            # 显示代理池状态
            result = "Current Proxy Pool:\n"
            for proxy in self.proxies.values():
                result += str(proxy) + "\n"
            return result

    def monitor_failed_proxies(self, check_interval: int = 60):
        # 监控失效的代理，尝试恢复
        while True:
            with self.lock:
                for port in self.failed_proxies[:]:
                    ip = self.check_proxy(port)
                    if ip:
                        self.proxies[port].is_available = True
                        self.proxies[port].ip = ip
                        # 重新创建限速器和信号量
                        storage = MemoryStorage()
                        limiter = Limiter(self.rate, self.capacity, storage)
                        semaphore = threading.Semaphore(self.max_threads_per_proxy)
                        self.proxy_info[port] = {
                            'limiter': limiter,
                            'semaphore': semaphore
                        }
                        self.failed_proxies.remove(port)
                        print(f"Proxy {port} restored and added back to pool.")
            time.sleep(check_interval)

    def check_proxy(self, port: int) -> bool:
        # 实现您的代理检查逻辑，例如尝试建立连接等
        proxy = "127.0.0.1:"+str(port)  # 根据需要修改代理地址和端口
        ip = testproxy.fetch_public_ip_via_http_proxy(proxy)
        if not ip:
            print("Failed to fetch public IP via SOCKS proxy.")
            return False


        # 这里假设代理已恢复可用
        return ip  # 返回 True 表示代理可用，False 表示不可用
