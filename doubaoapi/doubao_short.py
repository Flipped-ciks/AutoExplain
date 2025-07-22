from volcenginesdkarkruntime import Ark
import re

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

def main(question):

    prompt = f"""
    这是一道简答题：
    题目：{question['stem']}
    请你严格按照以下格式对题目进行解析：
    本题考查[最精炼的知识点名词，聚焦核心概念]。[给出这道题目的解析]。
    注意：知识点为没有形容词修饰的名词形式。解析内容不要包含总结性表述。
    输出时请删除所有[]占位符，仅保留有效内容。
    """

    # prompt = f"""
    # 这是一道简答题：
    # 题目：{question['stem']}
    # 答案：{question['answer']}
    # 请你严格按照以下格式对题目进行解析：
    # 本题考查[最精炼的知识点名词，聚焦核心概念]。[给出这道题目的解析]。
    # 注意：知识点为没有形容词修饰的名词形式。解析内容不要包含总结性表述。
    # 输出时请删除所有[]占位符，仅保留有效内容。
    # """

    # 原版，由于后面可以会有无答案的情况，因此，我们继续进行prompt调优。
    # prompt = f"""
    # 这是一道简答题：
    # 题目：{question['stem']}
    # 答案：{question['answer']}
    # 请你严格按照以下格式对题目进行解析：
    # 本题考查[知识点名词]。[分析这道题目为什么是这个答案]。
    # 注意：知识点为名词形式，简要精炼，分析内容不要包含总结性表述。
    # """

    completion = client.chat.completions.create(
        model="ep-20241202163303-l2gcl",
        messages = [
            {"role": "system", "content": "你是一个信息技术学科的老师，工作就是给试题写符合标准的解析"},
            {"role": "user", "content": prompt},
        ],
    )

    content = completion.choices[0].message.content

    # 1. 清除格式化符号（例如 `**`）
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)

    # 2. 移除所有换行符和多余的空格
    content = re.sub(r'\s+', ' ', content)

    # 3. 删除所有的[]
    # content = re.sub(r'\[\]', '', content)

    # 3. 最终文本结果
    cleaned_content = content.strip()

    # 返回清理后的文本
    return cleaned_content