from volcenginesdkarkruntime import Ark
import re

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

def main(question):

    # prompt = f"""
    # 这是一道填空题：
    # 题目：{question['stem']}
    # 答案：{question['answer']}
    # 请你严格按照以下格式对题目进行解析：
    # 本题考查[知识点]。[给出这道题目的解析]。故答案为：[XXXX]。
    # 注意：知识点为没有形容词修饰的名词形式，聚焦核心概念。解析内容不要包含总结性表述。
    # 如果有多个答案，将答案用"、"隔开。
    # 输出时请删除所有[]占位符，仅保留有效内容。
    # """

    prompt = f"""
    这是一道填空题：
    题目：{question['stem']}
    请你严格按照以下格式对题目进行解析：
    本题考查[知识点]。[给出这道题目的解析]。故答案为：[XXXX]。
    注意：知识点为没有形容词修饰的名词形式，聚焦核心概念。解析内容不要包含总结性表述。
    如果有多个答案，将答案用"、"隔开。
    输出时请删除所有[]占位符，仅保留有效内容。
    """


    completion = client.chat.completions.create(
        model="ep-20241202163303-l2gcl",
        messages = [
            {"role": "system", "content": "你是一个信息技术学科的老师，工作就是给信息技术学科的试题写符合标准的解析"},
            {"role": "user", "content": prompt},
        ],
    )

    content = completion.choices[0].message.content

    # 1. 清除格式化符号（例如 `**`）
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)

    # 2. 移除所有换行符和多余的空格
    content = re.sub(r'\s+', ' ', content)

    content = re.sub(r"[\[\]\']", "", content)

    # 3. 最终文本结果
    cleaned_content = content.strip()

    # 返回清理后的文本
    return cleaned_content