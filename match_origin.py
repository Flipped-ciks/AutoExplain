from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
from volcenginesdkarkruntime import Ark

# 初始化 Ark 客户端
client = Ark(base_url="https://ark.cn-beijing.volces.com/api/v3")

def encode(texts, mrl_dim=1024):
    # 使用豆包 embedding 模型生成向量
    resp = client.embeddings.create(
        model="doubao-embedding-large-text-250515",
        input=texts,
        encoding_format="float"
    )
    embeddings = np.array([d.embedding[:mrl_dim] for d in resp.data])
    # 归一化，方便做余弦匹配
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return (embeddings / norms).astype('float32')

# 1. 加载知识点数据
with open('point.json', 'r', encoding='utf-8') as f:
    knowledge_points = json.load(f)

# 2. 准备知识点文本
knowledge_texts = [kp['name'] for kp in knowledge_points]

# 3. 加载句向量模型
# knowledge_vectors = encode(knowledge_texts, mrl_dim=1024)
knowledge_vectors = np.load("knowledge_vectors.npy")

# 4. 构建 FAISS 索引
dim = knowledge_vectors.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(np.array(knowledge_vectors))

# 6. 给定题目进行匹配
def match_question_to_knowledge(question, top_k=5):
    question_vector = encode([question], mrl_dim=1024)
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
with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("\n✅ 每题匹配结果已保存至 result.json")