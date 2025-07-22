import os
import json
import time
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

# 构造提示词
def build_prompt(kp_name):
    return (
        f"你是一名初中信息技术教师，正在为知识点“{kp_name}”编写教学描述，"
        f"该描述用于帮助试题自动识别其所属知识点标签。"
        f"请用简洁准确的语言说明该知识点的定义、核心内容或应用场景，"
        f"语言尽量贴近考试题干表述，不少于30字。"
    )

def generate_description(point):
    completion = client.chat.completions.create(
        model="ep-20241202163303-l2gcl",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一名具备丰富教学经验的初中信息技术教师，"
                    "擅长为各类信息技术知识点编写简洁、准确、贴近考题风格的语义描述，"
                    "这些描述将用于自动将试题与知识点进行语义匹配。"
                    "请你保证生成的内容符合教纲，语言自然、信息准确。"
                )
            },
            {
                "role": "user",
                "content": (
                    f"请为初中信息技术知识点“{point}”生成一段简洁、清晰、语义明确的描述，"
                    "描述应说明该知识点的定义、核心内容或应用场景，语言风格贴近选择题或判断题题干，"
                    "不少于30字，用于试题自动标注知识点。"
                )
            },
        ]
    )
    return completion.choices[0].message.content



# 读取原始知识点
with open("20250714/point.json", "r", encoding="utf-8") as f:
    points = json.load(f)

# 补充 description 字段
for i, kp in enumerate(points):
    if "description" not in kp or not kp["description"]:
        print(f"📝 [{i+1}/{len(points)}] 生成：{kp['name']}")
        kp["description"] = generate_description(kp["name"])
        time.sleep(1.5)  # 控制请求速率，避免 429

# 保存新文件
with open("20250714/point_with_desc.json", "w", encoding="utf-8") as f:
    json.dump(points, f, ensure_ascii=False, indent=2)

print("✅ 所有知识点描述已生成并保存至 point_with_desc.json")