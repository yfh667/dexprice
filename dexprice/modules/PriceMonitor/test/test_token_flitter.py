
import dexprice.modules.utilis.define as define
import dexprice.modules.PriceMonitor.dexscreen_priceapi as dexscreen_priceapi
import dexprice.modules.PriceMonitor.tokenflitter as tokenflitter
from dexprice.modules.utilis.define import FilterCriteria
def main():
    criteria = FilterCriteria(
        liquidity_usd_min=10000,
        liquidity_usd_max=None,
        fdv_min=100000,
        fdv_max=None,
        pair_age_min_hours=45,
        pair_age_max_hours= None,
        txn_buy=50,
        txn_sell=50,
        volume=1000
    )

    chain_id = "solana"  # 这里使用示例的链 ID
    pair_addresses = ["D17YeDGu5o9oByhWvMnQbaoSruuaRPgEFZDMLtow6Jyo"]  # 示例地址
    # CA_addresses=["4y9E3tJpGNzRr1592oWTPECgyp2VDSc1Bf3DqAm5FZsK","1"]

    CA_addresses = ["FtHCi9cxJSSizrzMzsPjAfTfJi32V1CGRDM5Skqn4QBF"]
    proxy_port = 50000  # 示例代理端口

    # 调用 Get_Price_Dexscreen 函数
    tokens_info = dexscreen_priceapi.Get_Token_Dexscreen(define.Config.DEXS, chain_id, pair_addresses, proxy_port)

    for token in tokens_info:
        print(token)

    if(tokenflitter.normal_token_filter(token, criteria)):
        print("yes")
    else:
        print("no")


if __name__ == "__main__":
    main()
