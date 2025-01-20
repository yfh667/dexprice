import requests
import json

import dexprice.modules.proxy.testproxy as testproxy


def get_all_proxies(clash_api_url,headers):
    response = requests.get(f"{clash_api_url}/proxies", headers=headers)
    if response.status_code == 200:
        return response.json()["proxies"]
    else:
        print("Failed to get proxies:", response.text)
        return None

def get_one_ip_proxy(startport,clash_api_url,headers):
    proxies = get_all_proxies(clash_api_url,headers)

    proxynumber =get_proxy_number(proxies)
    # startport = 50000
    proxys = []
    ips = []
    # 添加代理到代理池
    for i in range(proxynumber):
        port = startport + i
        socksproxy = '127.0.0.1:' + str(port)
        ip = testproxy.fetch_public_ip_via_http_proxy(socksproxy)
        if ip != None:
            if ip not in ips:
                ips.append(ip)
            #  ip = "127.0.0.1"  # 假设所有代理的 IP 都是本地地址
                proxys.append(port)
    return proxys


def get_proxy_number(proxies):
    formatted_json1 =json.dumps(proxies['GLOBAL']['all'], indent=4, ensure_ascii=False)
    formatted_list = json.loads(formatted_json1)
    allproxy = formatted_list[6:-3]

    return  (len(allproxy))