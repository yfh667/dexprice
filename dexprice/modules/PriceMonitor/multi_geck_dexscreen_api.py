from dexprice.modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类
from token_bucket import Limiter, MemoryStorage
from dexprice.modules.utilis.define import Config,TokenInfo



def Get_DEX_From_GECK(CA_addresses, chain_id, num_threads, proxy_ports):
    manager = DexscreenApiManager()  # 实例化类

    if(chain_id ==0):
        chain_id1 = 'solana'
        chain_id2 = 'solana'
    elif(chain_id ==1):
        chain_id1 = 'eth'
        chain_id2 = 'ethereum'






# 调用类的方法，使用 Config.GECK 替代硬编码的 GECK
    results = manager.multi_get_token_dexscreen(Config.GECK, CA_addresses, chain_id1, num_threads, proxy_ports,0.5,30)
    # 创建一个新的列表来存储 pair_address
    pair_addresses = []
    # 遍历 results 并提取 pair_address
    for result in results:
        for token_info in result:
            if isinstance(token_info, TokenInfo):  # 确保 token_info 是 TokenInfo 实例
                pair_addresses.append(token_info.pair_address)

    # 打印结果
  #  print(pair_addresses)

    results2= manager.multi_get_token_dexscreen(Config.DEXS, pair_addresses, chain_id2, num_threads, proxy_ports,5,300)

    return results2



