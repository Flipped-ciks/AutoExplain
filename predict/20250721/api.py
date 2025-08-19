import requests
import json
from time import sleep

# ANSI 颜色代码
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# 读取试题数据
with open("Ques-KP-Chap-Map-2024.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

cookies = {
    "SESSION": "OGJjY2E3OWMtZTNiMy00NTFjLWFlNjktZTIyNjNkYTM5MjIw"
}
base_url = "https://qbm.xkw.com/console/question-aigc/ai-predict-kpoint"

matched = 0
total = 0

for q in questions:
    question_id = q["questionId"]
    true_kps = set(q["knowledgePointIds"])
    stem = q["stem"]

    url = f"{base_url}?questionid={question_id}&repredict=true&toptypeid=2001"
    try:
        res = requests.get(url, cookies=cookies, timeout=10)
        res.raise_for_status()
        result = res.json()

        predicted_kps = set(result.get("predictedPointIds", []))

        # 是否命中
        is_hit = bool(true_kps & predicted_kps)
        color = GREEN if is_hit else RED
        status = "✅ 命中" if is_hit else "❌ 未命中"

        # 打印可视化信息
        print(f"{color}{status}{RESET} | 题目：{stem}")
        print(f"   标注ID: {true_kps}")
        print(f"   预测ID: {predicted_kps}")
        print()

        if is_hit:
            matched += 1

    except Exception as e:
        print(f"{RED}[错误]{RESET} {question_id}: {e}")
        continue

    total += 1
    sleep(0.2)

# 总结统计
hit_rate = matched / total * 100 if total else 0
print(f"\n总题数: {total}")
print(f"命中数: {matched}")
print(f"命中率: {hit_rate:.2f}%")
