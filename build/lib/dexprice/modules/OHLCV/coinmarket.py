import requests
from dexprice.modules.utilis.define import Config,TokenInfo,TokenPriceHistory
from tqdm import tqdm  # 导入 tqdm
import requests
import time
from threading import Lock
import  dexprice.modules.utilis.timedefine as mytime  # 导入类
from datetime import datetime, timedelta

def fetch_historical_data(params, api_key):
    # API 的基础 URL
    base_url = "https://pro-api.coinmarketcap.com/v4/dex/pairs/ohlcv/historical"

    # 包含 API 密钥的请求头
    headers = {
        "X-CMC_PRO_API_KEY": api_key
    }

    # 代理设置（硬编码）
    proxies = {
        "http": "http://127.0.0.1:7897",
        "https": "http://127.0.0.1:7897"
    }

    max_retries = 5    # 最大重试次数
    retry_delay = 10   # 每次重试前的等待时间（秒）

    for attempt in range(max_retries):
        try:
            # 发送 GET 请求，包含请求头、参数和代理设置
            response = requests.get(base_url, headers=headers, params=params, proxies=proxies)

            # 检查请求是否成功
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"获取数据失败: {response.status_code} - {response.text}")

                # 如果状态码为 429（请求过多），等待后重试
                if response.status_code == 429:
                    print(f"请求过于频繁，等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                else:
                    # 对于其他错误状态码，可以根据需要决定是否重试
                    print(f"发生错误，等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)

        except requests.exceptions.RequestException as e:
            print(f"发生异常: {e}")
            print(f"等待 {retry_delay} 秒后重试...")
            time.sleep(retry_delay)

    print("已达到最大重试次数，获取数据失败。")
    return None
def get_historical_data(pairaddress, chainid, time_start, time_end, api_key, time_period="daily", interval="daily"):
    # 将时间字符串转换为 datetime 对象
    time_start_dt = datetime.strptime(time_start, "%Y-%m-%d")
    time_end_dt = datetime.strptime(time_end, "%Y-%m-%d")

    params = {
        "contract_address": pairaddress,  # 合约地址
        "network_slug": chainid,  # 网络标识符
        "time_period": time_period,  # 数据的时间周期
        "time_start": time_start,  # 开始日期
        "time_end": (time_end_dt - timedelta(days=1)).strftime("%Y-%m-%d"),  # 结束日期
        "interval": interval,  # 数据的时间间隔
    }

    data = fetch_historical_data(params, api_key)
    return data
def process_and_store_token_prices(data,tokenid):
    token_prices = []

    # 解析 quotes 数据
    if 'data' in data and data['data']:
        for quote_data in data['data'][0]['quotes']:
            for quote_item in quote_data['quote']:
                # 从 quote_item 提取相关数据
                open_price = quote_item['open']
                high_price = quote_item['high']
                low_price = quote_item['low']
                close_price = quote_item['close']
                volume = quote_item['volume']
                time = quote_data['time_open']  # 使用 time_open 作为时间戳

                # 创建 TokenPriceHistory 对象
                token_price = TokenPriceHistory(
                    tokenid=tokenid,
                    open=open_price,
                    high=high_price,
                    low=low_price,
                    close=close_price,
                    time=time,
                    volume=volume
                )

                # 将 TokenPriceHistory 对象添加到数组中
                token_prices.append(token_price)

    return token_prices
def get_token_price_history(token_db_entry, chain_id, days_in_past, api_key):
    """
    获取给定 token 的价格历史数据并返回处理后的结果
    :param token_db_entry: Tokendb 类的实例，包含 token 的数据库信息
    :param chain_id: 区块链 ID
    :param days_in_past: 获取多少天前的历史数据
    :param api_key: 用于调用 API 的密钥
    :return: 处理后的 token 价格数据
    """
    pair_address = token_db_entry.pair_address

    # 获取时间区间
    start_date = mytime.get_past_utc_date(days_in_past)
    end_date = mytime.get_current_utc_date()

    # print(f"Time range: {start_date} to {end_date}")

    # 如果 token 的创建时间比 start_date 更早，调整 start_date 为创建时间
    if mytime.compare_utc_dates(start_date, token_db_entry.creattime):
        start_date = mytime.format_date(token_db_entry.creattime)
    #print(f"Time is: {start_date} to {end_date}")

    # 调用 coinmarket API 获取历史数据
    historical_data = get_historical_data(
        pair_address, chain_id, start_date, end_date, api_key, time_period="daily", interval="daily"
    )

    # 使用 token ID 处理和存储 token 的价格数据
    token_id = token_db_entry.tokenid
    token_price_history = process_and_store_token_prices(historical_data, token_id)

    return token_price_history


def get_multi_token_price_history(tokendbs, chain_id, days_in_past, api_key):
    token_price_historys = []

    # tqdm 用于显示进度条，传入 tokendbs 列表，并设置描述信息
    for tokendb in tqdm(tokendbs, desc="Fetching token price history", unit="token"):
        token_price_history = get_token_price_history(tokendb, chain_id, days_in_past, api_key)
        token_price_historys.extend(token_price_history)

    return token_price_historys