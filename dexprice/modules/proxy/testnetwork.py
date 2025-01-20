import requests
def test_google_through_proxy(proxy_port):
    try:
        proxy_url = f"http://127.0.0.1:{proxy_port}"
        proxies = {
            'http': proxy_url,
            'https': proxy_url,
        }

        response = requests.get("https://www.google.com", proxies=proxies, timeout=5)
        if response.status_code == 200:
            print("Proxy can reach Google. Network is fine.")
            return True
        else:
            print(f"Google returned status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Failed to connect to Google through proxy: {e}")
        return False
def test_baidu( ):
    try:


        response = requests.get("https://www.baidu.com", timeout=5)
        if response.status_code == 200:
            print("Network can reach baidu. Network is fine.")
            return True
        else:
            print(f"Google returned status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Failed to connect to baidu through proxy: {e}")
        return False
# if(test_baidu( )):
#     print("Test baidu succeeded")
# else:
#     print("Test baidu failed")