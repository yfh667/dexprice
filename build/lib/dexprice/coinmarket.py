import requests

# Base URL for the API
base_url = "https://pro-api.coinmarketcap.com/v4/dex/pairs/ohlcv/historical"

# Parameters
params = {
    "contract_address": "HTmWEinSYg115BinCgHXuWAdQF8wKHEGfHH5C8nsYERJ",  # 合约地址
    "network_slug": "solana",  # 网络标识符
    "time_period": "hourly",  # 数据的时间周期
    "time_start": "2024-07-28",  # 开始日期
    "time_end": "2024-07-30",  # 结束日期
    "interval": "4h",  # 数据的时间间隔
}

# Headers including the API key for authentication
headers = {
    "X-CMC_PRO_API_KEY": "9a0342b8-00fa-4ef3-a6c0-89c06644f0f1"  # 替换为实际的 API 密钥
}

# Proxy settings (if needed)
proxies = {
    "http": "http://127.0.0.1:7897",
    "https": "http://127.0.0.1:7897"
}

try:
    # Send GET request with headers, parameters, and proxy settings
    response = requests.get(base_url, headers=headers, params=params, proxies=proxies)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        print("Data received:")
        print(data)
    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
