import re
import requests
import certifi
from bs4 import BeautifulSoup

def get_answer(qid, cookies):

    url = f"https://qbm.xkw.com/console/questions/{qid}/detail"
    res = requests.get(url, cookies=cookies)
    json_str = res.json()
    answer = json_str['answer']
    soup = BeautifulSoup(answer, 'html.parser')
    text = soup.get_text(strip=True)
    return text

def convert_choices(s):
    mapping = {
        'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5',
        'F': '6', 'G': '7', 'H': '8', 'I': '9', 'J': '10'
    }
    return ','.join(mapping[c] for c in sorted(s))

# 适用于选择题填入答案
def put_answer_choice(qid, cookies, answer):

    url = f"https://qbm.xkw.com/console/questions/{qid}/qml/answer"
    data = {'answer': f'<ans><sq><an isop="true">{convert_choices(answer)}</an></sq></ans>'}
    requests.put(url, cookies=cookies, json=data)

# 适用于填空题填入答案，去除字体属性
def put_answer_blank(qid, cookies, answer):

    url = f"https://qbm.xkw.com/console/questions/{qid}/qml/answer"
    data = {'answer': f'<ans><sq><an><span>{answer}</span></an></sq></ans>'}
    requests.put(url, cookies=cookies, json=data)

# 适用于判断题填入答案
def put_answer_judge(qid, cookies, answer):

    url = f"https://qbm.xkw.com/console/questions/{qid}/qml/answer"
    data = {'answer': f'<ans><sq><an><span>{answer}</span></an></sq></ans>'}
    requests.put(url, cookies=cookies, json=data)
def choice(qid, cookies, flag):

    url = f"https://qbm.xkw.com/console/questions/{qid}/detail"

    response = requests.get(url, cookies=cookies, verify=certifi.where())
    json_str = response.json()
    stem = json_str['explanation']
    soup = BeautifulSoup(stem, 'html.parser')
    text = soup.get_text(separator='', strip=True)
    pattern = r'[故]*答案为[:：]\s*([A-Z](?:[,、]?[A-Z])*)'
    match = re.search(pattern, text)
    if match:
        answer_str = match.group(1)
        answer = re.sub(r'[^A-Z]', '', answer_str)
        # print(f"提取的答案：{answer}")  # 输出：AB
        origin_answer = get_answer(qid, cookies)
        # print(f"真实的答案：{origin_answer}")
        if flag:
            put_answer_choice(qid, cookies, answer)
        elif(convert_choices(answer) != origin_answer):
            print(f"WARNING：题号{qid}答案不一致，请检查！")
        
    else:
        print("请检查模型的输出格式")

def blank(qid, cookies, flag):
    url = f"https://qbm.xkw.com/console/questions/{qid}/detail"

    response = requests.get(url, cookies=cookies, verify=certifi.where())
    json_str = response.json()
    stem = json_str['explanation']
    soup = BeautifulSoup(stem, 'html.parser')
    text = soup.get_text(separator='', strip=True)
    pattern = r"故答案为[:：](.*?)[。\.]"
    match = re.search(pattern, text)
    if match:
        answer = match.group(1)
        # print(f"提取的答案：{answer}")  # 输出：感知
        origin_answer = get_answer(qid, cookies)
        # print(f"真实的答案：{origin_answer}")
        if flag:
            put_answer_blank(qid, cookies, answer)
        elif(answer != origin_answer):
            print(f"WARNING：题号{qid}答案不一致，请检查！")
        
    else:
        print("请检查模型的输出格式")

def judge(qid, cookies, flag):
    url = f"https://qbm.xkw.com/console/questions/{qid}/detail"

    response = requests.get(url, cookies=cookies, verify=certifi.where())
    json_str = response.json()
    stem = json_str['explanation']
    soup = BeautifulSoup(stem, 'html.parser')
    text = soup.get_text(separator='', strip=True)
    
    pattern = r"故说法(正确|错误)"
    match = re.search(pattern, text)
    if match:
        answer = match.group(1)
        # print(f"提取的答案：{answer}")  # 输出：感知
        origin_answer = get_answer(qid, cookies)
        # print(f"真实的答案：{origin_answer}")
        if flag:
            put_answer_judge(qid, cookies, answer)
        elif(answer != origin_answer):
            print(f"WARNING：题号{qid}答案不一致，请检查！")

    else:
        print("请检查模型的输出格式")

def operation(qid, cookies):
    print("暂时无法处理操作题")

def short(qid, cookies):
    print("暂时无法处理简答题")

def compre(qid, cookies):
    print("暂时无法处理综合题")

# cookies = {
#     "SESSION": "OGE3MmY1YzQtZTIyMS00ODQyLWIwNTYtZTAwNGQ1OWU4NmI2"
# }

# judge(3792007346085888, cookies, True)

# blank(3784095191252992, cookies)

# choice(3792007344111616, cookies, True)

# get_answer(3784095191252992,cookies)
