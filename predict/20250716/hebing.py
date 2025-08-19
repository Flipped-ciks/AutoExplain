import json

# 加载 big_point.json
with open("20250716/big_point.json", "r", encoding="utf-8") as f:
    big_points = json.load(f)

# 加载 knowledge_keywords_by_id.json
with open("20250716/merged_data.json", "r", encoding="utf-8") as f:
    keyword_dict = json.load(f)  # 结构形如：{"59052": {"name": ..., "keywords": {...}}}

# 遍历 big_points，每个 point 是一个 dict
for point in big_points:
    point_id = str(point["id"])  # 注意需要转成字符串形式
    if point_id in keyword_dict:
        point["keywords"] = keyword_dict[point_id].get("keywords", {})
    else:
        point["keywords"] = {}

# 保存到新文件 enriched_big_point.json
with open("20250716/kp_key.json", "w", encoding="utf-8") as f:
    json.dump(big_points, f, ensure_ascii=False, indent=2)
