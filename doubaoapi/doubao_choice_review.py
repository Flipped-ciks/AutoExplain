from volcenginesdkarkruntime import Ark
import re

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

def main(question):

    prompt = f"""
    这是一道选择题：
    题目：{question['stem']}
    选项：
    {', '.join([f"{key}. {value}" for key, value in question['options'].items()])}
    答案：{question['answer']}
    解析：{question['explanation']}
    知识点：{question['knowledgePointNames']}
    章节标签：{question['name']}
    请你按照以下要求对该题目所有部分进行审核：
    1. 检查题干，题型，答案，解析是否出现标点符号以及错别字等问题；
    2. 检查解析是否正确，各个选项解析的正确或者错误，以及英文与中文之间不允许出现空格。
    3. 检查知识点是否合理。
    4. 检查章节标签是否合理。
    5. 审核要严格，不能任何错误。
    审核如果通过，则直接返回通过即可。否则，返回错误原因。
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

    # 3. 最终文本结果
    cleaned_content = content.strip()

    # 返回清理后的文本
    return cleaned_content