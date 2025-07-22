from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

# 1. 加载知识点数据
with open('20250714/point.json', 'r', encoding='utf-8') as f:
    knowledge_points = json.load(f)

# 2. 准备知识点文本
knowledge_texts = [
    f"{kp['name']}：{kp.get('description', '')}".strip() for kp in knowledge_points
]

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
question = "H.264视频编码具有什么优势（） 无损压缩，保持视频原有质量 高效压缩性能和良好视频质量 压缩比低，但视频质量高 主要用于低分辨率视频编码"
matched = match_question_to_knowledge(question)
print("匹配结果：")
for m in matched:
    print(f"✔ {m['name']} (id={m['id']})")
