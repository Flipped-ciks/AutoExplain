import requests
import certifi
import websocket
import re
import time

# 设置请求的 URL
url = "https://sso.zxxk.com/user/qrcode/qrcode-login/v2/content"

# 设置请求的参数
params = {
    # 'token': 'e32a14f180b44bd9a1409bf61fa6f9c6',  # 未知token，不知道怎么生成的
    # 'service': 'https://qbm.xkw.com/console/callback?client_name=qbm'  # service参数
}

# 设置请求头部
headers = {
    # 'Host': 'sso.zxxk.com',
    # 'Connection': 'keep-alive',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'X-Requested-With': 'XMLHttpRequest',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    # 'Accept': '*/*',
    # 'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    # 'sec-ch-ua-mobile': '?0',
    # 'Sec-Fetch-Site': 'same-origin',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Referer': 'https://sso.zxxk.com/login?service=https%3A%2F%2Fqbm.xkw.com%2Fconsole%2Fcallback%3Fclient_name%3Dqbm',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'xkw-device-id=511BE05CF3B4C7A52BEEA968212D5E86; UT1=ut-497666-rGWDN-w7YXgctw; UT2=ut-497666-rGWDN-w7YXgctw; qrcode-logined=true; service-number-logined=true; Hm_lvt_384e6cb5ddbf481e97ba12544207c0ee=1731465790,1732034952; ssoid=2cf372d0-5675-4b1b-ad97-f1f463f25a32'
}

# 发送 GET 请求
response = requests.get(url, headers=headers, params=params, verify=certifi.where())
print(response.text)

# 解析key_value
json_data = response.json()
url = json_data['data']['content']
match = re.search(r'key=([a-f0-9]+)', url)
key_value = match.group(1)
print(key_value)

WebSocket_URL = "wss://sso.zxxk.com/user/qrcode/socketServer?qrcodeKey=" + key_value + "&type=qrcode-login"

# 建立连接
try:
    ws = websocket.create_connection(WebSocket_URL, header=headers)
    print("Connected to WebSocket")

    # 接收服务器消息
    response = ws.recv()
    print("Received from server:", response)

except Exception as e:
    print("Error:", e)
