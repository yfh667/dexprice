

import requests


from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def send_message(token, chat_id, text):
    """
    发送带有 MarkdownV2 格式的消息，使 address 显示为固定宽度字体，并具有重试机制。

    :param token: Telegram Bot API Token
    :param chat_id: Telegram Chat ID 或用户名
    :param text: 要发送的消息文本
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'MarkdownV2'
    }


    # 定义HTTP代理
    proxies = {
        'http': 'http://127.0.0.1:7897',
        'https': 'http://127.0.0.1:7897'
    }

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.proxies.update(proxies)  # 设置代理

    try:
        response = session.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                #  print("Message sent!")
                return data['result']
            else:
                print(f"Failed to send message: {data['description']}")
                return "Failed to send message."
        else:
            print(f"HTTP Error: {response.status_code}")
            return f"HTTP Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return f"Error: {e}"
def sendmessage(address):
    escaped_text = escape_markdown(address)

    link = f"https://dexscreener.com/solana/{address}"
    # 计算涨幅百分比

    message_content = (
        f"`{escaped_text}`\n"
    )

    token = "7190422738:AAEuhELn2QcVfEDa-cF4bAwe4KgyQmbNF_Q"
    send_message(token, "@jingou11", message_content)
def escape_markdown(text):
    """
    转义 MarkdownV2 中的特殊字符
    """
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    return ''.join(['\\' + char if char in escape_chars else char for char in text])

#
# sendmessage("22")