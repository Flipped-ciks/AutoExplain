import requests
import certifi
from bs4 import BeautifulSoup


def main(qid, cookies):
    # 填空题

    url = "https://qbm.xkw.com/console/questions/"+ str(qid) +"/detail"

    response = requests.get(url, cookies=cookies, verify=certifi.where())

    json_str = response.json()
    stem = json_str['stem']             # 题目
    answer = json_str['answer']         # 答案

    result = ""

    soup = BeautifulSoup(stem, 'html.parser')
    for element in soup.find_all(['span', 'bk']):
        if element.name == 'span':
            result += element.text
        elif element.name == 'bk' and element.attrs.get('type') == 'underline':
            size = int(element.attrs.get("size", 0))
            result += "_" * size

    soup = BeautifulSoup(answer, 'html.parser')
    answer = []
    ans = soup.find_all('an')
    for an in ans:
        answer.append(an.find('span').text)  # 找到第一个 <span> 标签并获取内容，当然有可能是有多个 <span> 标签

    problem = {}
    problem['stem'] = result
    problem['answer'] = answer

    return problem