import requests
import certifi

# 默认返回probably最大的知识点，后续需要优化

def main(qid, cookies, type):

    url = "https://qbm.xkw.com/console/tiger/predictions?questionid=" + str(qid) + "&type=" + type

    response = requests.get(url, cookies=cookies ,verify=certifi.where())
    json_str = response.json()

    return json_str['predictedPointIds'][0]
