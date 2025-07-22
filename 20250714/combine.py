import json

# 1. 读取原始知识点文件
with open("big_point.json", "r", encoding="utf-8") as f:
    big_points = json.load(f)

# 2. 读取关键词结果
with open("knowledge_keywords_by_id.json", "r", encoding="utf-8") as f:
    keyword_map = json.load(f)

# 3. 合并关键词到对应知识点
for kp in big_points:
    kp_id_str = str(kp["id"])
    if kp_id_str in keyword_map:
        kp["keywords"] = keyword_map[kp_id_str]["keywords"]

# 4. 保存为新文件
with open("big_point_with_keywords.json", "w", encoding="utf-8") as f:
    json.dump(big_points, f, ensure_ascii=False, indent=2)

print("✅ 已将关键词合并保存到 big_point_with_keywords.json")
