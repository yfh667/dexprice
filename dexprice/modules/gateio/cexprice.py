import requests
from typing import Optional, Dict, Any
import  dexprice.modules.utilis.define as define
import  dexprice.modules.utilis.timedefine as timedefine

def get_cex_ohlcv_data(currency_pair: str, interval: str, limit: int,
                   end_timestamp: int, proxy_port: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """
    获取 K 线图数据，支持动态计算 `from` 参数。

    参数:
        currency_pair (str): 交易对，例如 "BTC_USDT"。
        interval (str): 时间间隔，例如 "1m", "1d"。
        limit (int): 数据点的数量，用于动态计算 `from` 参数。
        end_timestamp (int): 结束时间戳（秒级 Unix 时间戳）。
        proxy_port (int): 本地代理端口，例如 7890。

    返回:
        Optional[Dict[str, Any]]: 请求结果 JSON 数据，或者 None（请求失败）。
    """

    # 每种时间间隔对应的秒数
    interval_seconds = {
        "10s": 10,
        "1m": 60,
        "5m": 300,
        "15m": 900,
        "30m": 1800,
        "1h": 3600,
        "4h": 14400,
        "8h": 28800,
        "1d": 86400,
        "7d": 604800,
        "30d": 2592000
    }

    # 确保 interval 合法
    if interval not in interval_seconds:
        raise ValueError(f"Invalid interval: {interval}")

    # 根据 `limit` 和 `interval` 计算起始时间戳
    start_timestamp = end_timestamp - (limit * interval_seconds[interval])

    # 构建请求参数
    url = "https://api.gateio.ws/api/v4/spot/candlesticks"
    params = {
        "currency_pair": currency_pair,
        "interval": interval,
        "from": start_timestamp,
        "to": end_timestamp
    }

    # 设置代理
    proxies = None
    if proxy_port:
        proxy_url = f"http://127.0.0.1:{proxy_port}"
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }

    # 发起请求
    try:
        response = requests.get(url, params=params, proxies=proxies, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"HTTP error: {response.status_code}")
            print(response.text)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return None

# 示例用法


def clean_currency_pair(currency_pair: str) -> str:
    """
    去掉交易对中的 `_USDT` 后缀。
    """
    if currency_pair.endswith("_USDT"):
        return currency_pair.replace("_USDT", "")
    return currency_pair
def get_token_history(ohlcv_data, currency_pair):
    historydatas = []
    if(ohlcv_data):
        for entry in ohlcv_data :

            historydata =  define.OvhlFromCex(clean_currency_pair(currency_pair),entry[5],entry[3],entry[4],entry[2],timedefine.timestamp_to_datetime(int(entry[0])),entry[6])
            # print(entry)
            historydatas.append(historydata)
    return historydatas

def get_token_history2(currency_pair: str, interval: str, limit: int,
                       end_timestamp: int, proxy_port: Optional[int] = None) -> Optional[Dict[str, Any]]:
    ohlcv_data = get_cex_ohlcv_data(currency_pair, interval, limit, end_timestamp,  proxy_port)

    historydatas = get_token_history(ohlcv_data,currency_pair)
    return historydatas

