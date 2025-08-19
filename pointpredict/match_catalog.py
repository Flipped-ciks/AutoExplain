from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

# Step 0: 加载知识点数据
with open("Catalog.json", "r", encoding="utf-8") as f:
    chapters = json.load(f)

# Step 1: 加载模型
model = SentenceTransformer("moka-ai/m3e-base")

# Step 2: 编码章节名
def get_chapter_vector(name: str) -> np.ndarray:
    vec = model.encode(name, normalize_embeddings=True)
    return vec

# Step 3: 构建章节向量列表
chapter_vectors = []
chapter_ids = []
chapter_names = []

for ch in chapters:
    vec = get_chapter_vector(ch["name"])
    chapter_vectors.append(vec)
    chapter_ids.append(ch["id"])
    chapter_names.append(ch["name"])

chapter_vectors = np.array(chapter_vectors)

# Step 4: 构建 FAISS 索引
dim = chapter_vectors.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(chapter_vectors)

# Step 5: 匹配函数：输入题干文本，输出最相似的章节
def match_chapter(question_text: str, top_k: int = 5):
    q_vec = model.encode(question_text, normalize_embeddings=True)
    D, I = index.search(np.array([q_vec]), top_k)
    results = []
    for score, idx in zip(D[0], I[0]):
        results.append({
            "id": chapter_ids[idx],
            "name": chapter_names[idx],
            "score": float(score)
        })
    return results

# Step 6: 示例测试
test_question = "下面哪种方法可以为网页添加动态效果？"
matched = match_chapter(test_question)

print("🔍 匹配结果:")
for item in matched:
    print(f"- {item['name']}（得分: {item['score']:.4f}）")
