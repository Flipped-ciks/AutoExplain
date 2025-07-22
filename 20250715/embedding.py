import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

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

# ✅ 示例
question = "下列属于系统软件的是（）"
results = match_question(question)

for r in results:
    print(f"[{r['score']:.4f}] {r['name']} (id={r['id']})")
