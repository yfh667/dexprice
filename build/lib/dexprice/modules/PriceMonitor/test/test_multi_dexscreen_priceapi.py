from modules.utilis.define import Config
from modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类
from token_bucket import Limiter, MemoryStorage

# 示例使用
if __name__ == "__main__":
    manager = DexscreenApiManager()  # 实例化类

    chain_id = "solana"
    pair_addresses = ["1", "14TAnpeomRgQmgQD7kfpDMxFF8MxkdGypikeqkmbF2aY", "HG4ocK8X1ZNEZfW9vjYQzvkGJSKXzAEK8E5yjcDrFrwB", "1"]  # 示例地址
    CA_addresses = ["1", "KENMdm22KMgjgGhQ19yLtsLD4vaheJBmg3v9KwuFnM3", "1"]

    num_threads = 2
    proxy_ports = [30002, 30001]

    rate = 5  # 每秒生成的令牌数
    capacity = 300  # 令牌桶的最大容量
    storage = MemoryStorage()
    limiter = Limiter(rate, capacity, storage)

    # 调用类的方法，使用 Config.GECK 替代硬编码的 GECK
    results = manager.multi_get_token_dexscreen(Config.DEXS, pair_addresses, chain_id, num_threads, proxy_ports,5,300)
    print("All results:", results)
