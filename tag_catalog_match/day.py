import requests
import json
from datetime import datetime, timedelta
import time

def date_range(start_date, end_date):
    """生成从start_date到end_date的日期列表（包含两端）"""
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates

def load_existing_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)  # 返回现有列表
    except FileNotFoundError:
        return []  # 文件不存在时返回空列表
    except json.JSONDecodeError:
        print("JSON 文件格式错误，将清空并重新写入")
        return []
    
def fetch_new_data(date):

    url = f"https://qbm.xkw.com/console/question-tasks/completed?maxendtime={(date + timedelta(days=1)).strftime('%Y-%m-%d')}T16:00:00.000Z&minendtime={date.strftime('%Y-%m-%d')}T16:00:00.000Z&onlymistake=false"
    cookies = {
    "SESSION": "MDE0MWU3NDctOWQ2My00YzE2LThiNTAtMzY5NWRjYzk3YmU1"
    }

    res = requests.get(url, cookies=cookies)
    return res.json()

def merge_and_save(file_path):

    for date in date_list:

        existing_data = load_existing_data(file_path)
        new_data = fetch_new_data(date)
        merged_data = existing_data + new_data
    
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=2)
        
        print(f"已成功追加 {len(new_data)} 条数据")

        time.sleep(0.3)


if __name__ == "__main__":

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_list = date_range(start_date, end_date)
    merge_and_save("tag_catalog_match/response_2024.json")