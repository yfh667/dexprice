import requests

# API URL

# 发起 GET 请求

def getalltoken():
    #url = "https://contract.mexc.com/api/v1/contract/detail"
    url = "https://contract.mexc.com/api/v1/contract/detail"
    symbol = []
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    try:
        response = requests.get(url, proxies=proxies)  # 添加代理

       # response = requests.get(url)
        # 检查 HTTP 响应状态码
        if response.status_code == 200:
            data = response.json()
            # 检查请求是否成功
            if data.get("success"):
                # 输出所有合约详情
                for contract in data.get("data", []):
                    symbol.append(contract["symbol"])
                    # print(f"Symbol: {contract['symbol']}")
                    # print(f"Display Name: {contract['displayName']}")
                    # print(f"Base Coin: {contract['baseCoin']}")
                    # print(f"Quote Coin: {contract['quoteCoin']}")
                    # print(f"Max Leverage: {contract['maxLeverage']}")
                    # print(f"Min Leverage: {contract['minLeverage']}")
                    # print(f"Maker Fee Rate: {contract['makerFeeRate']}")
                    # print(f"Taker Fee Rate: {contract['takerFeeRate']}")
                    # print("-" * 50)
            else:
                print(f"API returned an error: {data.get('code')} - {data.get('message', 'Unknown error')}")
        else:
            print(f"HTTP Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return symbol
# symbol = getalltoken()
# print(symbol)