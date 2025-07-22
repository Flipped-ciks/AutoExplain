from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

# Step 1: 加载知识点数据
with open("20250715/big_point_with_keywords.json", "r", encoding="utf-8") as f:
    knowledge_points = json.load(f)

# Step 2: 加载模型
model = SentenceTransformer("moka-ai/m3e-base")

# Step 3: 构建知识点向量
def get_knowledge_vector(name: str, keywords: dict, name_weight: float = 1.0) -> np.ndarray:
    # 编码知识点名称
    name_vec = model.encode(name)
    weighted_sum = name_vec * name_weight
    total_weight = name_weight

    # 编码关键词 + 加权
    for word, freq in keywords.items():
        vec = model.encode(word)
        weighted_sum += vec * freq
        total_weight += freq

    # 平均并归一化
    final_vec = weighted_sum / total_weight
    final_vec = final_vec / np.linalg.norm(final_vec)
    return final_vec

# Step 4: 生成所有知识点向量
knowledge_vectors = []
kp_ids = []
kp_names = []

for kp in knowledge_points:
    vec = get_knowledge_vector(kp["name"], kp["keywords"])
    knowledge_vectors.append(vec)
    kp_ids.append(kp["id"])
    kp_names.append(kp["name"])

knowledge_vectors = np.array(knowledge_vectors)

# Step 5: 构建 FAISS 索引
dim = knowledge_vectors.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(knowledge_vectors)

# Step 6: 匹配函数
def match_question(question_text: str, top_k: int = 5):
    q_vec = model.encode(question_text, normalize_embeddings=True)
    D, I = index.search(np.array([q_vec]), top_k)
    results = []
    for score, idx in zip(D[0], I[0]):
        results.append({
            "id": kp_ids[idx],
            "name": kp_names[idx],
            "score": float(score)
        })
    return results

# 7. 示例测试
with open('20250715/stem_bigpoint.json', 'r', encoding='utf-8') as f:
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

    matched = match_question(question, top_k=2)
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
summary = {
    "total": total,
    "full_match": full_match,
    "partial_match": partial_match,
    "full_match_rate": f"{full_match / total:.2%}" if total > 0 else "N/A",
    "top2_match_rate": f"{(full_match + partial_match) / total:.2%}" if total > 0 else "N/A"
}

output = {
    "summary": summary,
    "details": result_records
}

# 10. 保存结果
with open('20250715/result.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("\n✅ 每题匹配结果已保存至 result.json")

