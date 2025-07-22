import json

# 1. 读取清洗后的 JSON 文件
with open("20250714/extracted_fields_cleaned.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. 只保留需要的字段
cleaned = []
for item in data:
    if "stem" in item and "knowledgePointIds" in item and "knowledgePointNames" in item:
        cleaned.append({
            "stem": item["stem"],
            "knowledgePointIds": item["knowledgePointIds"],
            "knowledgePointNames": item["knowledgePointNames"]
        })

# 3. 保存为 Python 文件（变量名为 data）
with open("20250714/stem_point.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print("✅ 已成功保存为 stem_point.json")    
