from volcenginesdkarkruntime import Ark
import numpy as np
import json

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
knowledge_vectors = encode(knowledge_texts, mrl_dim=1024)

np.save("knowledge_vectors.npy", knowledge_vectors)
