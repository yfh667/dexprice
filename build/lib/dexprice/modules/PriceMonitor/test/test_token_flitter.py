from modules.utilis.define import Config
from modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类
from token_bucket import Limiter, MemoryStorage
from modules.PriceMonitor.tokenflitter import liquid_token_filter,fdv_token_filter
import itertools
from modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类
from token_bucket import Limiter, MemoryStorage
from modules.utilis.define import Config,TokenInfo

from modules.db.readjson import extract_chain_and_ca,read_json_file,gettokenca

from modules.db.create_db import initialize_table
from modules.PriceMonitor.multi_geck_dexscreen_api import Get_DEX_From_GECK  # 导入类

# 示例使用
if __name__ == "__main__":
    manager = DexscreenApiManager()  # 实例化类

    chain_id = "ethereum"
    #pair_addresses = ["1", "0x8C6369252e4B54C212471303C3a6E6017be9ad62", "0x5c6919B79FAC1C3555675ae59A9ac2484f3972F5", "1"]  # 示例地址

    file_path = '/home/yfh/Desktop/linshi/result.json'  # 将路径替换为你的 JSON 文件路径
    json_data = read_json_file(file_path)

    # 从 JSON 数据中提取所有链和合约地址
    jsonresults = gettokenca(json_data)
    pair_addresses = [item['ca'] for item in jsonresults if item['chainid'] == 'ethereum']





    num_threads = 2
    proxy_ports = [30002, 30001]

    rate = 5  # 每秒生成的令牌数
    capacity = 300  # 令牌桶的最大容量
    # 调用类的方法，使用 Config.GECK 替代硬编码的 GECK
    results = manager.multi_get_token_dexscreen(Config.DEXS, pair_addresses, chain_id, num_threads, proxy_ports,5,300)
  #  print("All results:", results)
    # 使用列表解析展开嵌套列表
    flattened_results = [token for sublist in results for token in sublist]
    # # 现在 flattened_results 是一个一维列表，每个元素都是 TokenInfo 对象
    # print(flattened_results)

    # # 验证每个元素
    # for token_info in flattened_results:
    #  print(f"Address: {token_info.address}, Name: {token_info.name}")
    #

    #2.we need set the scale for fdv liquid etc.

    tokens=[]

    for results1 in flattened_results:
        if liquid_token_filter(results1) and fdv_token_filter(results1):
         #   print(results1)
            tokens.append(results1)
        else:
            pass
    print(tokens)
