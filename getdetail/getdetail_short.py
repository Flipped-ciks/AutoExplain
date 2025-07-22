import requests
import certifi
from bs4 import BeautifulSoup

def main(qid, cookies):
    # 简答题

    url = "https://qbm.xkw.com/console/questions/"+ str(qid) +"/detail"

    response = requests.get(url, cookies=cookies, verify=certifi.where())

    json_str = response.json()
    stem = json_str['stem']             # 题目
    answer = json_str['answer']         # 答案

    result = ""

    soup = BeautifulSoup(stem, 'html.parser')
    for element in soup.find_all(['span']):
        result += element.text

    soup = BeautifulSoup(answer, 'html.parser')
    answer = ""
    ans = soup.find('an')
    for span in ans.find_all('span'):
        answer += span.text

    problem = {}
    problem['stem'] = result
    problem['answer'] = answer

    return problem

