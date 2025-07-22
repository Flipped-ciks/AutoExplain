import json
import random
from sentence_transformers import InputExample

# 1. 加载题干配对数据
with open("20250714/stem_point.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. 加载全部知识点名称（用于负采样）
with open("20250714/point.json", "r", encoding="utf-8") as f:
    all_kp_data = json.load(f)
all_kps = [kp["name"] for kp in all_kp_data]

# 3. 构建训练样本
train_examples = []

for item in data:
    stem = item["stem"]
    pos_names = item["knowledgePointNames"]

    for pos_kp in pos_names:
        # 正样本
        train_examples.append(InputExample(texts=[stem, pos_kp], label=1.0))

        # 负样本：随机选一个不是当前正样本的知识点
        for _ in range(1):  # 每个正样本配一个负样本，可调整数量
            neg_kp = random.choice(all_kps)
            while neg_kp in pos_names:
                neg_kp = random.choice(all_kps)
            train_examples.append(InputExample(texts=[stem, neg_kp], label=0.0))


with open("20250714/train_pairs.jsonl", "w", encoding="utf-8") as f:
    for ex in train_examples:
        f.write(json.dumps({
            "text1": ex.texts[0],
            "text2": ex.texts[1],
            "label": ex.label
        }, ensure_ascii=False) + "\n")

print("✅ 已保存训练样本至 train_pairs.jsonl")


