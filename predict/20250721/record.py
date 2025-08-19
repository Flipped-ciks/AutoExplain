import requests

url = "https://qbm.xkw.com/console/reports/account/record?currentpage=1&pagesize=50000&scope=my&yearmonth=2025-07"
cookies = {
  "UT1": "ut-1489555-Fb11R6E9J6XiEw",
  "xkw-device-id": "8190A31A786C3D4DF7F37DAEA8241220",
  "xkw-fs-id": "cb1ed2549895c8ca281442223f5d5e68",
  "xk.identity": "%7b%22g%22%3a%7b%22ids%22%3a%5b%5d%7d%7d",
  "JSESSIONID": "D617156CC2B08D86674676E95BD27C94",
  "SESSION": "MjFkZGRlMTgtZDc3Yy00YjllLTllMzYtYjE0ZjRjZDEwMmFl",
  "acw_tc": "0a47308f17533633298947129e00598be6fc8bdde3b97d25773fc18b309c36",
  "sid": "1c393efc-14db-4f99-abc1-aa00ddc9c595",
}

headers = {
  "Host": "qbm.xkw.com",
  "Connection": "keep-alive",
  "is-ajax-request": "true",
  "sec-ch-ua-platform": "\"Windows\"",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
  "Accept": "application/json, text/plain, */*",
  "X-Qbm-Sign": "aurora690",
  "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
  "sec-ch-ua-mobile": "?0",
  "Sec-Fetch-Site": "same-origin",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Dest": "empty",
  "Referer": "https://qbm.xkw.com/",
  "Accept-Encoding": "gzip, deflate, br, zstd",
  "Accept-Language": "zh-CN,zh;q=0.9"
}

res = requests.get(url, headers=headers, cookies=cookies)

with open("predict/20250721/record.json", "w", encoding="utf-8") as f:
    f.write(res.text)

import json

def sum_amount_for_course(data, target_course_id=20):
    total_amount = 0
    for item in data.get('items', [])[:-2]:
        if item.get('courseId') == target_course_id:
            # if(item.get('amount') > 0):
                total_amount += float(item.get('amount'))
    return total_amount

# 举例加载数据和调用
with open('predict/20250721/record.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total_20 = sum_amount_for_course(data, 20)
total_35 = sum_amount_for_course(data, 35)
print(f"amount总和为: {(total_20 * (1 + 0.195) + total_35 * (1 + 0.26)) * 0.93}")

