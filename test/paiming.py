import json
import re

def extract_max_salary(salary_str):
    """从薪资字符串中提取最高薪资数值（单位：千元）"""
    # 使用正则表达式匹配"-"后面的数字部分
    match = re.search(r'-(\d+)k', salary_str)
    if match:
        return int(match.group(1))
    return 0  # 无法解析时返回0

# 读取JSON文件
with open('test/result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取apiData中的信息
jobs = []
if data.get('code') == 20000 and 'data' in data and 'apiData' in data['data']:
    for item in data['data']['apiData']:
        # 确保必要字段存在
        if 'id' in item and 'salary' in item and 'position' in item:
            job_info = {
                'id': item['id'],
                'salary': item['salary'],
                'position': item['position'],
                'max_salary': extract_max_salary(item['salary'])
            }
            jobs.append(job_info)

# 按最高薪资降序排序
jobs_sorted = sorted(jobs, key=lambda x: x['max_salary'], reverse=True)

# 输出结果
with open('result.txt', 'w', encoding='utf-8') as f:
    f.write("按最高薪资排序的岗位信息：\n")
    for job in jobs_sorted:
        line = f"ID: {job['id']}, 岗位: {job['position']}, 薪资: {job['salary']}, 最高薪资: {job['max_salary']}k\n"
        f.write(line)
        # 同时在控制台打印
        print(line.strip())

print("\n结果已保存到result.txt文件")

