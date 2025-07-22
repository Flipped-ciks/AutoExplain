import json

# 1. 加载合法知识点 ID（来自 point.json）
with open('point.json', 'r', encoding='utf-8') as f:
    point_data = json.load(f)

valid_ids = set()
for item in point_data:
    valid_ids.add(item['id'])

# 2. 加载 extracted_fields.json 并筛选 + 提取字段
with open('20250716/junoir_origin.json', 'r', encoding='utf-8') as f:
    extracted_data = json.load(f)

filtered_result = []
for item in extracted_data:
    kp_ids = item.get('knowledgePointIds', [])
    # 只保留知识点全部合法的项目
    if all(kp_id in valid_ids for kp_id in kp_ids):
        filtered_item = {
            "stem": item.get("stem", ""),
            "knowledgePointIds": kp_ids,
            "knowledgePointNames": item.get("knowledgePointNames", [])
        }
        filtered_result.append(filtered_item)

# 3. 保存为新文件
with open('20250716/junoir_stem_point.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_result, f, ensure_ascii=False, indent=2)

print(f"筛选完成：原始 {len(extracted_data)} 条，保留 {len(filtered_result)} 条。")
