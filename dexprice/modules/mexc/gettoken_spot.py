import requests

# API URL

# 发起 GET 请求

def getalltoken():
    #url = "https://contract.mexc.com/api/v1/contract/detail"
    url = "https://api.mexc.com/api/v3/defaultSymbols"
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
            if data.get("data"):
                # 输出所有合约详情
                for spot in data.get("data", []):
                    symbol.append(spot)

            else:
                print(f"API returned an error: {data.get('code')} - {data.get('message', 'Unknown error')}")
        else:
            print(f"HTTP Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return symbol
symbol = getalltoken()
print(symbol)