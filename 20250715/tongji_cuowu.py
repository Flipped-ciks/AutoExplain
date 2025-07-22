import json

# 加载原始文件
with open("20250715/result.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data["details"][0])

# 保留 match != "full" 的项
filtered_detail = [item for item in data["details"] if item["match"] != "full"]

# 更新 details 字段
data["details"] = filtered_detail

# 保存为新文件（可选覆盖原文件）
with open("20250715/result_filtered.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"筛选完成，共保留 {len(filtered_detail)} 条记录。")
