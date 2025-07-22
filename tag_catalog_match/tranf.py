import json
import os

def extract_unique_qids(json_file_path, txt_output_path):
    """
    从 JSON 文件中提取唯一的 qid 并保存为 TXT 文件
    
    参数:
    json_file_path (str): JSON 输入文件路径
    txt_output_path (str): TXT 输出文件路径
    """
    # 检查 JSON 文件是否存在
    if not os.path.exists(json_file_path):
        print(f"错误：JSON 文件 '{json_file_path}' 不存在")
        return
    
    unique_qids = set()  # 使用集合确保唯一性
    
    try:
        # 读取 JSON 文件
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 根据 JSON 结构提取 qid
        if isinstance(data, list):  # 如果 JSON 是数组
            for item in data:
                if 'qid' in item:
                    unique_qids.add(str(item['qid']))  # 转为字符串避免类型问题
        elif isinstance(data, dict):  # 如果 JSON 是对象
            # 根据实际结构调整，这里假设对象包含列表或嵌套对象
            # 示例：遍历对象的每个值，检查是否包含 qid
            for value in data.values():
                if isinstance(value, list):
                    for item in value:
                        if 'qid' in item:
                            unique_qids.add(str(item['qid']))
                elif isinstance(value, dict) and 'qid' in value:
                    unique_qids.add(str(value['qid']))
        else:
            print(f"警告：JSON 根类型不支持（{type(data).__name__}），应为数组或对象")
            return
        
        # 保存唯一的 qid 到 TXT 文件
        if unique_qids:
            with open(txt_output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(unique_qids)))  # 排序后写入，便于查看
            print(f"成功提取 {len(unique_qids)} 个唯一 qid 到 {txt_output_path}")
        else:
            print("未找到任何 qid")
    
    except json.JSONDecodeError:
        print(f"错误：无法解析 JSON 文件 '{json_file_path}'")
    except Exception as e:
        print(f"发生未知错误：{e}")

# 使用示例
if __name__ == "__main__":
    
    json_file = "tag_catalog_match/response.json"  # 替换为实际 JSON 文件路径
    txt_file = "response.txt"        # 输出 TXT 文件路径
    
    extract_unique_qids(json_file, txt_file)