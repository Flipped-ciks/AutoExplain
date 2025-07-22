import requests

url = "https://qbm.xkw.com/console/questions/3792007346266112/qml/answer"
cookies = {
  "SESSION": "OGE3MmY1YzQtZTIyMS00ODQyLWIwNTYtZTAwNGQ1OWU4NmI2"
}

answer = "正确"
data = {'answer': f'<ans><sq><an><span>{answer}</span></an></sq></ans>'}

res = requests.put(url, cookies=cookies, json=data)
print(res.text)
