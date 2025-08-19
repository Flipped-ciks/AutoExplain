import json
import re

# 读取原始 JSON 文件
with open("20250717/junoir_stem_point.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 处理每一项的 knowledgePointNames
for item in data:
    cleaned_names = []
    for name in item.get("knowledgePointNames", []):
        # 删除形如 (59030) 的前缀部分
        cleaned = re.sub(r"^\(\d+\)", "", name)
        cleaned = cleaned.strip()  # 去掉可能的空格
        cleaned_names.append(cleaned)
    item["knowledgePointNames"] = cleaned_names

# 保存为新文件或覆盖原文件
with open("20250717/junoir_stem_point.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("已清理所有 knowledgePointNames 中的 (数字) 前缀。")
