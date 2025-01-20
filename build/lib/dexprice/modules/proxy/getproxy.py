import requests
import dexprice.modules.proxy.testproxy as proxy2
# 假设 fetch_public_ip_via_http_proxy 函数在内部使用了 requests.get
def fetch_public_ip_via_http_proxy(proxy_url, timeout=5):
    try:
        # 设置代理
        proxies = {
            'http': f'socks5://{proxy_url}',
            'https': f'socks5://{proxy_url}',
        }
        # 发送请求，添加超时参数
        response = requests.get("http://ipinfo.io/ip", proxies=proxies, timeout=timeout)

        if response.status_code == 200:
            print("Your Public IP:", response.text.strip())
            return True
        else:
            print(f"Failed to fetch public IP. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False

def check_open_ports(start_port, number, proxy_host="127.0.0.1"):
    """
    检查指定范围内的端口是否有效，返回可以使用的端口列表。

    :param start_port: 起始端口号
    :param end_port: 结束端口号
    :param proxy_host: 代理服务器地址 (默认是本地 127.0.0.1)
    :return: 可用端口的列表
    """
    open_ports = []
    end_port = start_port+number-1
    for port in range(start_port, end_port + 1):
        proxy = f"{proxy_host}:{port}"
        print(f"正在测试端口: {proxy}")
        if proxy2.fetch_public_ip_via_http_proxy(proxy):
            print(f"端口 {port} 可用")
            open_ports.append(port)
        else:
            print(f"端口 {port} 不可用")

    return open_ports

