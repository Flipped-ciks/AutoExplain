import requests

url = "https://qbm.xkw.com/console/reports/account/record?currentpage=1&pagesize=5000&scope=my&yearmonth=2025-07"
cookies = {
  "UT1": "ut-1489555-Fb11R6E9J6XiEw",
  "xkw-device-id": "8190A31A786C3D4DF7F37DAEA8241220",
  "xkw-fs-id": "cb1ed2549895c8ca281442223f5d5e68",
  "xk.identity": "%7b%22g%22%3a%7b%22ids%22%3a%5b%5d%7d%7d",
  "JSESSIONID": "59475D832F7EB22F8AA22C5A9C08B9D8",
  "SESSION": "OGJjY2E3OWMtZTNiMy00NTFjLWFlNjktZTIyNjNkYTM5MjIw",
  "sid": "8bcca79c-e3b3-451c-ae69-e2263da39220",
  "acw_tc": "1a0c39d117531055282452325e0063aee0cbce15d6786ccbf91fa359035948",
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

with open("record.json", "w", encoding="utf-8") as f:
    f.write(res.text)
