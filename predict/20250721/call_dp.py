import requests

def call_deepseek(prompt: str, model: str = "deepseek-r1:1.5b", stream: bool = False) -> str:
    """
    调用本地 Ollama 的 deepseek 模型进行推理

    参数:
        prompt: 输入提示词（如：题目 + 知识点候选 + 指令）
        model: 使用的模型名称，默认是 'deepseek-r1:1.5b'
        stream: 是否使用流式输出，默认关闭

    返回:
        模型生成的完整回答文本
    """
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }

    response = requests.post(url, json=payload, stream=stream)

    if not response.ok:
        raise RuntimeError(f"请求失败: {response.status_code} - {response.text}")

    if stream:
        # 流式输出（你可以实时打印）
        full_response = ""
        for line in response.iter_lines():
            if line:
                content = line.decode("utf-8")
                full_response += content
                print(content, end="", flush=True)
        return full_response
    else:
        result = response.json()
        return result.get("response", "").strip()


# 🧪 示例用法
if __name__ == "__main__":
    example_prompt = """以下是试题内容和候选知识点，请判断题目最可能对应哪个知识点：

题目：
以下哪个设备用于连接多个计算机并在网络中转发数据包？
A. 显示器
B. 路由器
C. 键盘
D. 打印机

候选知识点：
1. 信息与信息技术基础
2. 网络基础与应用
3. 文件管理

请直接输出最匹配的知识点编号，例如：“1” 或 “2”。
"""

    result = call_deepseek(example_prompt)
    print("\n\n🧠 结果：", result)
