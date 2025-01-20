import sys
import os
from modules.PriceMonitor.dexscreen_priceapi import Get_Token_Dexscreen,Get_Price_Dexscreen  # 导入类

from modules.utilis.define import Config,TokenInfo

def main():
    chain_id = "solana"  # 这里使用示例的链 ID
    pair_addresses = ["H72LGm51KajBhJniXh3Q3VakQzXToEuBHFvfAWPT9JmR"]  # 示例地址
   # CA_addresses=["4y9E3tJpGNzRr1592oWTPECgyp2VDSc1Bf3DqAm5FZsK","1"]

    CA_addresses = ["FtHCi9cxJSSizrzMzsPjAfTfJi32V1CGRDM5Skqn4QBF"]
    proxy_port = 50011  # 示例代理端口

    # 调用 Get_Price_Dexscreen 函数
    tokens_info = Get_Token_Dexscreen(Config.DEXS,chain_id, pair_addresses, proxy_port)

    for token in tokens_info:
        print(token)

if __name__ == "__main__":
    main()
