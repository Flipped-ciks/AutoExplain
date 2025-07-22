from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

# 1. 加载知识点数据
with open('clouds/point.json', 'r', encoding='utf-8') as f:
    knowledge_points = json.load(f)

# 2. 准备知识点文本
knowledge_texts = [kp['name'] for kp in knowledge_points]

# 3. 加载句向量模型
model = SentenceTransformer('moka-ai/m3e-base')

# 4. 知识点编码为向量
knowledge_vectors = model.encode(knowledge_texts, normalize_embeddings=True)

# 5. 构建 FAISS 索引
dim = knowledge_vectors.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(np.array(knowledge_vectors))

# 6. 给定题目进行匹配
def match_question_to_knowledge(question, top_k=5):
    question_vector = model.encode([question], normalize_embeddings=True)
    scores, indices = index.search(question_vector, top_k)
    results = []
    for idx in indices[0]:
        kp = knowledge_points[idx]
        results.append({
            "id": kp["id"],
            "name": kp["name"],
            "parentId": kp["parentId"]
        })
    return results

# 7. 示例测试
with open('clouds/test.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

total = 0
full_match = 0
partial_match = 0
result_records = []

for item in test_data:
    question = item.get("stem", "")
    true_ids = set(item.get("knowledgePointIds", []))
    true_kps = set(item.get("knowledgePointNames", []))

    if not question or not true_ids:
        continue

    matched = match_question_to_knowledge(question, top_k=2)
    predicted_ids = [m["id"] for m in matched]
    predicted_names = [m["name"] for m in matched]

    # 判断匹配结果
    if predicted_ids[0] in true_ids:
        match_type = "full"
        full_match += 1
    elif any(pid in true_ids for pid in predicted_ids):
        match_type = "partial"
        partial_match += 1
    else:
        match_type = "none"

    total += 1

    # 保存匹配记录
    result_records.append({
        "stem": question,
        "knowledgePointIds": list(true_ids),
        "knowledgePointNames": list(true_kps),
        "predicted": [{"id": pid, "name": pname} for pid, pname in zip(predicted_ids, predicted_names)],
        "match": match_type
    })

# 9. 输出评估结果
print("\n📊 匹配评估结果：")
print(f"总题数：{total}")
print(f"完全匹配数：{full_match}")
print(f"部分匹配数（Top2 命中）：{partial_match}")
print(f"完全匹配率：{full_match / total:.2%}")
print(f"Top2 匹配率：{(full_match + partial_match) / total:.2%}")

# 10. 保存结果
with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(result_records, f, ensure_ascii=False, indent=2)

print("\n✅ 每题匹配结果已保存至 result.json")

