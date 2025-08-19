import json
from collections import defaultdict

# Step 1：加载知识点（big_point）
with open("20250715/big_point.json", "r", encoding="utf-8") as f:
    big_points = json.load(f)

# Step 2：加载题目-知识点配对（stem_bigpoint）
with open("20250715/stem_bigpoint.json", "r", encoding="utf-8") as f:
    stem_data = json.load(f)

# Step 3：统计知识点ID -> 出现次数
kp_count = defaultdict(int)

for item in stem_data:
    for kp_id in item["knowledgePointIds"]:
        kp_count[kp_id] += 1

# Step 4：输出每个知识点的题目数量
for kp in big_points:
    kp_id = kp["id"]
    name = kp["name"]
    count = kp_count.get(kp_id, 0)
    print(f"{kp_id} - {name} ：题目数量 = {count}")
