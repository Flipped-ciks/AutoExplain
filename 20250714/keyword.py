import json
import jieba.analyse
from collections import defaultdict, Counter

# ✅ 1. 读取知识点数据
with open("big_point.json", "r", encoding="utf-8") as f:
    point_data = json.load(f)

knowledge_points = {kp["id"]: kp["name"] for kp in point_data}

# ✅ 2. 读取题目数据
with open("20250714/stem_bigpoint_2024.json", "r", encoding="utf-8") as f:
    stem_data = json.load(f)

# ✅ 3. 按知识点 ID 汇总题干
id2stems = defaultdict(list)
for item in stem_data:
    kp_ids = item.get("knowledgePointIds", [])
    stem = item.get("stem", "")
    for kid in kp_ids:
        if kid in knowledge_points:
            id2stems[kid].append(stem)

# ✅ 4. 提取关键词并统计频率
output = {}
for kid, stems in id2stems.items():
    word_counter = Counter()
    for stem in stems:
        keywords = jieba.analyse.extract_tags(stem, topK=5, allowPOS=("n", "vn", "v"))
        word_counter.update(keywords)
    output[str(kid)] = {
        "name": knowledge_points[kid],
        "keywords": dict(word_counter.most_common(50))  # 最多保留前 50 个
    }

# ✅ 5. 保存结果到 JSON 文件
with open("keywords_by_id_2024.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("✅ 已完成关键词提取，保存")