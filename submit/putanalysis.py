import requests
import certifi
import re

def split_text_into_spans(answer_text):
    # 定义中文、英文、数字和标点符号的正则表达式
    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]')
    english_pattern = re.compile(r'[a-zA-Z0-9]')
    punctuation_pattern = re.compile(r'[，。！？、；：“”‘’《》【】（）]')
    
    spans = []  # 用于存储生成的span元素
    current_span = ""  # 当前span内容
    current_font = None  # 当前span的字体
    
    # 遍历每个字符并根据类型生成相应的span
    for char in answer_text:
        if chinese_pattern.match(char) or punctuation_pattern.match(char):  # 中文或中文标点
            # 如果当前span是英文或数字，需要闭合span并开始新的span
            if current_font != "宋体":
                if current_span:
                    spans.append(f'<span word-font="Times New Roman">{current_span}</span>')
                current_span = char
                current_font = "宋体"
            else:
                current_span += char
        elif english_pattern.match(char):  # 英文或数字
            # 如果当前span是中文，需要闭合span并开始新的span
            if current_font != "Times New Roman":
                if current_span:
                    spans.append(f'<span word-font="宋体">{current_span}</span>')
                current_span = char
                current_font = "Times New Roman"
            else:
                current_span += char
        else:
            # 对于不属于中文、英文或标点的字符，按照宋体处理
            if current_font != "Times New Roman":
                if current_span:
                    spans.append(f'<span word-font="宋体">{current_span}</span>')
                current_span = char
                current_font = "Times New Roman"
            else:
                current_span += char

    # 在循环结束后，确保将最后的span添加到结果中
    if current_span:
        if current_font == "宋体":
            spans.append(f'<span word-font="宋体">{current_span}</span>')
        else:
            spans.append(f'<span word-font="Times New Roman">{current_span}</span>')
    
    # 将所有span合并为一个字符串并返回
    return ''.join(spans)

def main(qid, cookies, answer_text):

    url = "https://qbm.xkw.com/console/questions/" + str(qid) + "/qml/explanation"

    data = {
        "explanation": f"<exps><seg name=\"详解\"><p align=\"left\">{split_text_into_spans(answer_text)}</p></seg></exps>"
    }

    response = requests.put(url, cookies = cookies, json=data)

    return response.text

# 这里为修改判断题的答案，answer取值为正确or错误
def answer_judge(qid, cookies, answer):

    url = "https://qbm.xkw.com/console/questions/" + str(qid) + "/qml/answer"

    data = {
        "answer": f"<ans><sq><an><span>{answer}</span></an></sq></ans>"
    }

    response = requests.put(url, cookies = cookies, json=data)

    return response.text

# 这里为修改填空题的答案，answer取值为
def answer_blank(qid, cookies, answer):

    answer_list = answer.split('、')
    url = "https://qbm.xkw.com/console/questions/" + str(qid) + "/qml/answer"

    answer_str = "<ans><sq>"
    for answer in answer_list:
        answer_str += f"<an><span>{answer}</span></an>"
    answer_str += "</sq></ans>"

    data = {
        "answer": answer_str
    }

    response = requests.put(url, cookies = cookies, json=data)

    print(response.text)

# 这里为修改选择题的答案，answer取值为A、B、C、D等，仅针对单选，多选后续需要优化
def answer_choice(qid, cookies, answer):

    url = "https://qbm.xkw.com/console/questions/" + str(qid) + "/qml/answer"
    data = {
        "answer": f"answer=<ans><sq><an isop=\"true\">{','.join(str(ord(option) - ord('A') + 1) for option in answer.split('、'))}</an></sq></ans>"
    }

    response = requests.put(url, cookies = cookies, json=data)
    return response.text

def get_analysis(qid, cookies):
    
    url = "https://qbm.xkw.com/console/questions/"+ str(qid) +"/detail"
    response = requests.get(url, cookies=cookies, verify=certifi.where())
    json_str = response.json()
    explaination = json_str['explanation']
    

def answer(qid, cookies):

    url = "https://qbm.xkw.com/console/questions/" + str(qid) + "/qml/answer"
    data = {
        "answer": "<ans><sq><an isop=\"true\">2</an></sq></ans>"
    }
    response = requests.put(url, cookies = cookies, json=data)

    return response.text

def stem(qid, cookies):

    url = "https://qbm.xkw.com/console/questions/" + str(qid) + "/qml/stem"

    data = {
        "stem": "<stem><p align=\"left\"><span word-font=\"宋体\">在多人协同制作网页时，可能遇到的挑战有沟通不畅、</span><bk index=\"1\" size=\"6\" type=\"underline\"/><span word-font=\"宋体\">等。</span></p></stem>"
    }

    response = requests.put(url, cookies = cookies, json=data)
    print(response.text)
    return response.text