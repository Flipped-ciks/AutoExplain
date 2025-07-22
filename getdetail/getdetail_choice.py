import requests
import certifi
from bs4 import BeautifulSoup

# 选择题有三个部分，分别为题干、选项、答案
# 最终的返回结果是一个字典，包含题干、选项、答案

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
    options = {}

    soup = BeautifulSoup(stem_options, 'html.parser')

    # 解析题干，把所有span标签中的文本合并到一起
    paras = soup.find_all('p')
    for p in paras:
        for span in p.find_all('span'):
            stem += span.text
        stem += '\n'
    stem = stem[:-1]

    # 解析选项，把选项放在字典中
    og = soup.find('og')
    i = 0
    for op in og.find_all('op'):
        # 这里竟然有些没有span，这就要首先判断是否包含span
        if op.find('span'):
            span_str = ""
            spans = op.find_all('span')
            for span in spans:
                span_str += span.text
            options[chr(65 + i)] = span_str
        else:
            options[chr(65 + i)] = op.text
        i += 1

    # 解析答案选项，把对应数字映射到选项字母
    soup = BeautifulSoup(answer, 'html.parser')
    an_element = soup.find('an')
    if an_element and an_element.has_attr('isop'):                  # 这个isop属性可以判断是否为选择题！！！
        if an_element.text == '':
            answer = '无答案'
        else:
            numbers = an_element.text.split(',')
            # 如果ans只有一个元素，那就是单选；如果是多个数字，那就是多选。这里作为判断单选多选的方法。
            ans = [chr(64 + int(num)) for num in numbers]
            answer = "".join(ans)

    question = {}

    question['stem'] = stem
    question['options'] = options
    question['answer'] = answer

    return question
