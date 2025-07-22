import json

# 假设你已经加载好了所有知识点的列表
with open("20250715/big_point_with_keywords.json", "r", encoding="utf-8") as f:
    knowledge_points = json.load(f)

# 遍历统计每个知识点的关键词总频次
for kp in knowledge_points:
    total_freq = sum(kp["keywords"].values())
    print(f"{kp['id']} - {kp['name']} ：关键词频率总和 = {total_freq}")
