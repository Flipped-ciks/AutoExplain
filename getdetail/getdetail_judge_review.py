import requests
import certifi
from bs4 import BeautifulSoup

def main(qid, cookies):

    # 设置URL，题号为传入参数
    url = "https://qbm.xkw.com/console/questions/" + str(qid) + "/detail"

    # 发送GET请求，cookies为传入参数
    response = requests.get(url, cookies=cookies, verify=certifi.where())

    # 下面开始解析JSON数据
    json_str = response.json()
    stem_options = json_str['stem']                         # 题干与选项混合
    answer = json_str['answer']                             # 答案
    explanation = json_str['explanation']                   # 解析
    catalogs = json_str['catalogs']                         # 章节目录
    knowledgePointNames = json_str['knowledgePointNames']   # 知识点


    stem = ""
    soup = BeautifulSoup(stem_options, 'html.parser')

    # 这里解析出来题干
    paras = soup.find('p')
    for span in paras.find_all('span'):
        stem += span.text
    stem += '（正确/错误）'

    # 这里默认有答案，没有的话看是否需要改？
    soup = BeautifulSoup(answer, 'html.parser')
    an = soup.find('an')
    answer = an.find('span').text

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

    question = {}
    question['stem'] = stem
    question['answer'] = answer
    question['explanation'] = explanation
    question['typeId'] = '2003'
    question['name'] = name
    question['knowledgePointNames'] = knowledgePointNames

    return question
