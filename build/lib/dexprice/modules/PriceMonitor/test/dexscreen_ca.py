import requests
import dexprice.modules.PriceMonitor.dexscreen_priceapi as dexscreen_priceapi
from dexprice.modules.utilis.define import Config,TokenInfo

def get_token_pairs(token_addresses):
    url = f'https://api.dexscreener.com/latest/dex/tokens/{token_addresses}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析 JSON 响应
      #  print(data)

        # 处理返回的数据
        if 'pairs' in data:
            return data['pairs']
        else:
            print("No pairs found.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def get_liquidmax_pair_addresses(pairs):

    if 'pairAddress' in pair:
     #   pair_addresses.append(pair['pairAddress'])
        return pair['pairAddress']

if __name__ == '__main__':

    ca_addresses = ["HPueqQjSgaSatMBKrvBvAnRmc6jnr51cPM1EjUJVpump"]
    # pairs = get_token_pairs(ca_addresses[0])
    # maxliquid = 0
    # CApairaddress =''
    # if(pairs ):
    #
    #     for pair in pairs:
    #         #  print(pair)
    #
    #         liquidity_info = pair.get('liquidity', {})
    #         liquid = liquidity_info.get('usd')
    #
    #         if liquid is not None:
    #             if liquid > maxliquid:
    #                 maxliquid = liquid
    #                 CApairaddress = pair['pairAddress']
    #         else:
    #             print("Warning: 'liquidity' or 'usd' key is missing in pair data.")
    #  #   print(pair)
    # print(CApairaddress)
    proxy_port = 50013  # 示例代理端口    chain_id = "solana"  # 这里使用示例的链 ID

    chain_id = "solana"  # 这里使用示例的链 ID
    # print(CApairaddress)
# 调用 Get_Price_Dexscreen 函数
    tokens_info = dexscreen_priceapi.Get_Token_Dexscreen(Config.DEXCA,chain_id, ca_addresses, proxy_port)
    pairaddress = []
    pairaddress.append(tokens_info[0].pair_address)
    realtoken = dexscreen_priceapi.Get_Token_Dexscreen(Config.DEXS,chain_id, pairaddress, proxy_port)
    print(tokens_info)

