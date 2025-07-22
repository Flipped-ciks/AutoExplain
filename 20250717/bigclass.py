# 该代码用于将stem_point.json中的知识点替换为大类的知识点
# 用到point.json
import json

with open("point.json", "r", encoding="utf-8") as f:
    points = json.load(f)

point_dict = {kp["id"]: kp for kp in points}

with open("20250717/junoir_stem_point_2024.json", "r", encoding="utf-8") as f:
    data = json.load(f)

new_data = []

for item in data:
    new_item = item.copy()

    new_ids = []
    new_names = []

    for kp_id, kp_name in zip(item["knowledgePointIds"], item["knowledgePointNames"]):
        kp_info = point_dict.get(kp_id)
        if kp_info and kp_info.get("depth") == 2:
            # 替换为 parentId 和父节点名字
            parent_id = kp_info.get("parentId")
            parent_info = point_dict.get(parent_id)
            if parent_info:
                new_ids.append(parent_id)
                new_names.append(parent_info.get("name"))
            else:
                # 找不到父节点，保留原始
                new_ids.append(kp_id)
                new_names.append(kp_name)
        else:
            # depth 不为2，保持不变
            new_ids.append(kp_id)
            new_names.append(kp_name)

    new_item["knowledgePointIds"] = new_ids
    new_item["knowledgePointNames"] = new_names
    new_data.append(new_item)

# 保存到新文件
with open("20250717/stem_bigpoint_2024.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print("✅ 处理完成，已保存")