import requests
import json
from bs4 import BeautifulSoup
import os
import time

def parse_question_response(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    
    # 提取题目文本
    stem_element = soup.find('stem')
    stem_text = ""
    if stem_element:
        # 提取题目文本内容
        p_elements = stem_element.find_all('p')
        stem_text = " ".join([p.get_text(strip=True) for p in p_elements])
        
        # 提取选项
        og_element = stem_element.find('og')
        if og_element:
            op_elements = og_element.find_all('op')
            options = [op.get_text(strip=True) for op in op_elements]
            stem_text += " " + " ".join(options)
    
    # 提取其他字段（假设这些字段在JSON结构中）
    catalog_ids = []
    catalogs = []
    knowledge_point_ids = []
    knowledge_point_names = []
    
    # 尝试从JSON中提取其他字段（如果响应包含JSON数据）
    try:
        response_json = json.loads(response_text)
        catalog_ids = response_json.get('catalogIds', [])
        catalogs = response_json.get('catalogs', [])
        knowledge_point_ids = response_json.get('knowledgePointIds', [])
        knowledge_point_names = response_json.get('knowledgePointNames', [])
    except json.JSONDecodeError:
        # 如果响应不是JSON格式，尝试从HTML中提取
        # 这里需要根据实际HTML结构调整提取逻辑
        pass
    
    # 构建结果JSON
    result = {
        "stem": stem_text,
        "catalogIds": catalog_ids,
        "catalogs": catalogs,
        "knowledgePointIds": knowledge_point_ids,
        "knowledgePointNames": knowledge_point_names
    }
    
    return result

def read_question_ids(file_path):
    """从txt文件读取题号列表"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 过滤空行并去除首尾空白
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"题号文件 {file_path} 不存在")
        return []

def save_to_file(data, filename='extracted_fields_2024.json'):
    """将数据追加保存到JSON文件（以列表形式叠加）"""
    existing_data = []
    
    # 读取已有的数据
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            print(f"文件 {filename} 格式错误，将创建新文件")
            existing_data = []
    
    # 添加新数据
    existing_data.append(data)
    
    # 保存更新后的数据
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已追加到 {filename}")


def process_question_ids(question_ids, base_url, cookies, sleep_time = 0.2):
    """处理题号列表并保存结果"""
    results = []
    
    for idx, question_id in enumerate(question_ids, 1):

        print(f"正在处理第 {idx}/{len(question_ids)} 题，题号: {question_id}")
        
        # 构建请求URL
        url = base_url.format(question_id=question_id)
        
        try:
            # 发送请求
            res = requests.get(url, cookies=cookies)
            res.raise_for_status()  # 检查请求是否成功
            
            # 解析响应
            parsed_data = parse_question_response(res.text)
            parsed_data["questionId"] = question_id  # 添加题号到结果中
            
            # 保存到文件
            save_to_file(parsed_data)
            
            results.append(parsed_data)
            print(f"题目 {question_id} 处理完成")
            
        except requests.RequestException as e:
            print(f"请求题目 {question_id} 出错: {e}")
        except Exception as e:
            print(f"处理题目 {question_id} 出错: {e}")

        # 添加请求间隔
        if idx < len(question_ids):  # 最后一题后不需要等待
            print(f"等待 {sleep_time} 秒后继续下一题...")
            time.sleep(sleep_time)  # 等待指定秒数
    
    return results

if __name__ == "__main__":

    # 基础URL
    base_url = "https://qbm.xkw.com/console/questions/{question_id}/detail?math-to-svg=false"
    
    # cookies
    cookies = {
        "SESSION": "MDE0MWU3NDctOWQ2My00YzE2LThiNTAtMzY5NWRjYzk3YmU1"
    }
    
    # 题号文件路径
    question_ids_file = "tag_catalog_match/question_ids_2024.txt"
    
    # 读取题号
    question_ids = read_question_ids(question_ids_file)
    
    if question_ids:
        print(f"共读取到 {len(question_ids)} 个题号")
        # 处理所有题号
        process_question_ids(question_ids, base_url, cookies)
    else:
        print("没有找到题号，请检查题号文件")



