# 根据题目id，返回题目类型

import requests
import certifi
from bs4 import BeautifulSoup

# 题目类型，依次为：选择题、填空题、判断题、操作题、简答题、综合题
# 选择题分为单选和多选，需要进行区分
type = ['01', '02', '03', '04', '05', '06']

# 测试
# type = ['选择题', '填空题', '判断题', '操作题', '简答题', '综合题']
# cookies = {
#     "SESSION": "MmQ5Y2YzZjUtYjg5NS00NDM4LWJkN2EtZjE5NmMzNjAzM2Zl"
# }

# 通过判断stem标签的属性，来判断题目的类型
def main(qid, cookies):

    url = "https://qbm.xkw.com/console/questions/" + str(qid) + "/detail"

    response = requests.get(url, cookies=cookies, verify=certifi.where())

    json_str = response.json()
    stem = json_str['stem']
    soup = BeautifulSoup(stem, 'html.parser')
    if soup.find('og'):                         # 选择题，直接返回结果
        return type[0]
    elif len(soup.find_all('p')) == 1:          # 可能是填空题、判断题或者简答题
        bk = soup.find('bk')
        if not bk:                                  # 说明是简答题
            return type[4]
        else:
            if bk.get('type') == 'underline':       # 说明是填空题
                return type[1]
            elif bk.get('type') == 'bracket':       # 说明是判断题
                return type[2]
    else:
        bk = soup.find('bk')
        if not bk:                                  # 说明是操作题
            return type[3]
        else:                                       # 说明是综合题
            return type[5]

# 专门针对选择题，返回选择题的单选or多选
def choice(qid, cookies):

    url = "https://qbm.xkw.com/console/questions/" + str(qid) +"/infer-struct-question-type?typeid=2001"
    
    response = requests.get(url, cookies=cookies, verify=certifi.where())
    json_str = response.json()

    return json_str[0]["id"]

# 直接返回标签type
def gettype(qid, cookies):
    url = "https://qbm.xkw.com/console/questions/" + str(qid) + "/detail"

    response = requests.get(url, cookies=cookies, verify=certifi.where())

    json_str = response.json()

    return json_str['typeId']




# cookies = {
#     "SESSION": "NTAyYzdhYTUtNmU4ZC00ZThiLWE5YWQtZTczYmQwMTBjMGE5"
# }

# print(choice(3735884023898112,cookies))