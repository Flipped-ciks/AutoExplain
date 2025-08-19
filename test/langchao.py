import requests

url = "https://api.m.riskbird.com/companyInfo/list"
headers = {
  "Host": "api.m.riskbird.com",
  "app-uuid": "RANDOM-2dcb0d4d-0c58-404c-96b7-41fc8248081f",
  "app-versionCode": "47020",
  "Accept": "*/*",
  "app-version": "lasted",
  "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXNzd29yZCI6IjVjOGYzYjUzOGRiYTVmYzg5NWNhNDA2NWEwNTVlMjg0IiwibW9iaWxlIjoiNjRBRTAzREY0MjI5QTczOUM2RThENTgyOTExOTE1ODQiLCJleHAiOjE3NTQzMTgyMTMsInVzZXJJZCI6MjA5MzA2LCJ1dWlkIjoiNWIzYWEzM2EtYzYyZC00ZGI0LTg2YTUtNTVhMWM1ODFkN2FjIiwidXNlcm5hbWUiOiIxODczODIxODAyMyJ9.woGkDw8FSnHY2cEvdB1LM-Ztpy7VoL-rqNUPnrKUDaA",
  "app-device": "ios",
  "Accept-Language": "zh-CN,zh-Hans;q=0.9",
  "Accept-Encoding": "gzip, deflate, br",
  "mobile-model": "H5",
  "Content-Type": "application/json",
  "Origin": "https://m.riskbird.com",
  "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/20) uni-app",
  "Referer": "https://m.riskbird.com/",
  "app-env": "prod",
  "Connection": "keep-alive",
  "mobile-brand": "Unknown",
  "app-fromPlatform": "riskbird"
}

data = {
	"orderNo": "APP202508042255519681069",
	"dataType": "job",
	"extractType": "job",
	"page": 1,
	"size": 344
}

res = requests.post(url, headers=headers, json=data)

with open("test/result.json", "w", encoding="utf-8") as f:
    f.write(res.text)