import json

# 读取 JSON 文件
with open("tag_catalog_match/response_2024.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 提取 courseId = 20 的所有 qid
question_ids = []

for item in data:
    if item.get("courseId") == 20:
        qid = item.get("qid")
        if qid is not None:
            question_ids.append(str(qid))

# 写入到文件，每行一个 qid
with open("tag_catalog_match/question_ids_2024.txt", "w", encoding="utf-8") as f:
    for qid in question_ids:
        f.write(qid + "\n")

print(f"共提取 {len(question_ids)} 个 qid 写入")
