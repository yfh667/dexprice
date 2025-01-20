import dexprice.modules.proxy.testproxy as proxy2
# def fetch_public_ip_via_socks_proxy(proxy_url):
#     try:
#         # 设置SOCKS代理
#         proxies = {
#             'http': f'socks5://{proxy_url}',
#             'https': f'socks5://{proxy_url}',
#         }
#
#         # 发送请求
#         response = requests.get("http://ipinfo.io/ip", proxies=proxies)
#
#         # 检查响应状态码
#         if response.status_code == 200:
#             print("Your Public IP:", response.text.strip())
#             return True
#         else:
#             print(f"Failed to fetch public IP. Status code: {response.status_code}")
#             return False
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")
#         return False
# [50000, 50001, 50002, 50003, 50004, 50005, 50008, 50009, 50010]
# sing-bpx
#[30006, 30007, 30008]
if __name__ == "__main__":
    proxy = "127.0.0.1:7890"  # 根据需要修改代理地址和端口



    if not proxy2.fetch_public_ip_via_http_proxy(proxy):
        print("Failed to fetch public IP via http proxy.")
    if not proxy2.fetch_public_ip_via_socks_proxy(proxy):
        print("Failed to fetch public IP via SOCKS proxy.")
