import os
from openai import OpenAI
import logging
import re

logging.getLogger('openai').setLevel(logging.WARNING)

XAI_API_KEY = os.getenv("XAI_API_KEY")
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

def main(question):

    prompt = f"""
    这是一道选择题：
    题目：{question['stem']}
    选项：
    {', '.join([f"{key}. {value}" for key, value in question['options'].items()])}
    答案：{question['answer']}
    请根据以下格式分析选项：
    本题考查{{某知识点}}。{{具体分析为什么选择该答案}}。{{故答案为：{{A/B/C/D}}}}。
    不要保留"{{}}"或其他非预期符号。
    如果答案有多个选项用、隔开
    """

    completion = client.chat.completions.create(
        model="grok-beta",
        messages=[
            {"role": "system", "content": "你是一个信息技术学科的老师"},
            {"role": "user", "content": prompt},
        ],
        temperature = 0
    )

    content = completion.choices[0].message.content

    # 1. 清除格式化符号（例如 `**`）
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)

    # 2. 移除所有换行符和多余的空格
    content = re.sub(r'\s+', ' ', content)

    # 3. 删除所有 `{` 和 `}`
    content = re.sub(r'[{}]', '', content)

    # 4. 只保留英文单词之间的空格，其他空格全部删除
    # - 匹配字母与字母之间的空格，保留它们
    # - 删除其他情况的空格（例如字母前、字母后、中文之间的空格）
    content = re.sub(r'([a-zA-Z])\s+([a-zA-Z])', r'\1 \2', content)  # 保留英文单词之间的空格
    content = re.sub(r'\s+', '', content)  # 删除所有其他空格

    # 5. 最终文本结果
    cleaned_content = content.strip()

    # 返回清理后的文本
    return cleaned_content
