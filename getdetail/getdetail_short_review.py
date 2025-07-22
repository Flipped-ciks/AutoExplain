import requests
import certifi
from bs4 import BeautifulSoup

def main(qid, cookies):
    # 简答题

    url = "https://qbm.xkw.com/console/questions/"+ str(qid) +"/detail"

    response = requests.get(url, cookies=cookies, verify=certifi.where())

    json_str = response.json()
    stem = json_str['stem']                                 # 题目
    answer = json_str['answer']                             # 答案
    explanation = json_str['explanation']                   # 解析
    catalogs = json_str['catalogs']                         # 章节目录
    knowledgePointNames = json_str['knowledgePointNames']   # 知识点


    result = ""

    soup = BeautifulSoup(stem, 'html.parser')
    for element in soup.find_all(['span']):
        result += element.text

    soup = BeautifulSoup(answer, 'html.parser')
    answer = ""
    ans = soup.find('an')
    for span in ans.find_all('span'):
        answer += span.text

    # 获取解析
    soup = BeautifulSoup(explanation, 'html.parser')
    paras = soup.find('p')
    explanation = ""
    for span in paras.find_all('span'):
        explanation += span.get_text()

    # 获取章节目录
    name = []
    for catalog in catalogs:
        name.append(catalog['name'])

    problem = {}
    problem['stem'] = result
    problem['answer'] = answer
    problem['explanation'] = explanation
    problem['typeId'] = '2005'
    problem['name'] = name
    problem['knowledgePointNames'] = knowledgePointNames

    return problem

