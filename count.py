import json

# 假设你已经从 res.json 中加载了数据
with open("res.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 初始化总和
total_amount = 0.0

# 遍历 items，筛选 courseId == 20 的条目
for item in data.get("items", []):
    if item.get("courseId") == 35:
        total_amount += item.get("amount", 0)

print(f"courseId=20 的 amount 总和为: {total_amount}")
