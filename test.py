import json
from collections import defaultdict

# 从文件中读取 JSON 数据
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 合并数据
def merge_data(data1, data2):
    merged_data = {}

    # 遍历第一个数据字典
    for key, value in data1.items():
        if key in data2:
            # 如果两个文档有相同的 id，合并 keywords
            merged_keywords = defaultdict(int)
            
            # 合并 data1 的关键词
            for word, count in value["keywords"].items():
                merged_keywords[word] += count
            
            # 合并 data2 的关键词
            for word, count in data2[key]["keywords"].items():
                merged_keywords[word] += count
            
            # 更新合并后的数据
            merged_data[key] = {
                "name": value["name"],  # 知识点名称
                "keywords": dict(merged_keywords)  # 合并后的关键词字典
            }
        else:
            # 只有 data1 有的 id，直接加入
            merged_data[key] = value

    # 遍历 data2 中没有在 data1 中的 id
    for key, value in data2.items():
        if key not in data1:
            merged_data[key] = value

    return merged_data

# 按 id 排序并输出
def save_sorted_data(merged_data, output_file):
    sorted_merged_data = dict(sorted(merged_data.items()))  # 按 id 从小到大排序
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sorted_merged_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 合并后的数据已保存为 {output_file}")

# 文件路径
file1 = 'keywords_by_id_2024.json'  # 第一个 JSON 文件
file2 = 'knowledge_keywords_by_id.json'  # 第二个 JSON 文件
output_file = 'merged_data.json'  # 输出的文件路径

# 从文件中读取数据
data1 = read_json_file(file1)
data2 = read_json_file(file2)

# 合并数据
merged_data = merge_data(data1, data2)

# 保存合并后的结果，并按 id 排序
save_sorted_data(merged_data, output_file)
