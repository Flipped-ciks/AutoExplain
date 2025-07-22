import json

# 加载 point.json 中的合法知识点 ID
with open('point.json', 'r', encoding='utf-8') as f:
    point_data = json.load(f)

valid_ids = set()
for item in point_data:
    valid_ids.add(item['id'])

# 加载 extracted_fields.json 并过滤
with open('extracted_fields.json', 'r', encoding='utf-8') as f:
    extracted_data = json.load(f)

filtered_data = []
for item in extracted_data:
    kp_ids = item.get('knowledgePointIds', [])
    if all(kp_id in valid_ids for kp_id in kp_ids):
        filtered_data.append(item)

# 保存过滤后的结果
with open('filtered_extracted_fields.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

print(f"过滤完成，原始数据 {len(extracted_data)} 条，保留 {len(filtered_data)} 条。")
