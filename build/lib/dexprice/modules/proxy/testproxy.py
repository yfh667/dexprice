import requests

import requests

def fetch_public_ip_via_http_proxy(proxy_url, timeout=5):
    """
    使用 HTTP 代理获取公共 IP 地址。

    :param proxy_url: 代理服务器的 URL
    :param timeout: 请求超时时间，默认 5 秒
    :return: 成功则返回 IP 地址字符串，失败则返回 None
    """
    try:
        proxies = {
            'http': proxy_url,
            'https': proxy_url,
        }
        # 添加超时参数
        #"https://api.ipify.org"
        #"http://ipinfo.io/ip"
        response = requests.get("http://ipinfo.io/ip", proxies=proxies, timeout=timeout)

        if response.status_code == 200:
            ip_address = response.text.strip()  # 获取 IP 地址字符串
            print("Your Public IP:", ip_address)
            return ip_address  # 返回 IP 地址字符串
        else:
            print(f"Failed to fetch public IP. Status code: {response.status_code}")
            return None  # 返回 None 表示失败
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None  # 返回 None 表示失败



def fetch_public_ip_via_socks_proxy(proxy_url):
    try:
        # 设置SOCKS代理
        proxies = {
            'http': f'socks5://{proxy_url}',
            'https': f'socks5://{proxy_url}',
        }

        # 发送请求
        response = requests.get("http://ipinfo.io/ip", proxies=proxies)

        # 检查响应状态码
        if response.status_code == 200:
            print("Your Public IP:", response.text.strip())
            return True
        else:
            print(f"Failed to fetch public IP. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False

