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
    stem_options = json_str['stem']             # 题干与选项混合
    answer = json_str['answer']                 # 答案

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

    question = {}
    question['stem'] = stem
    question['answer'] = answer

    return question
