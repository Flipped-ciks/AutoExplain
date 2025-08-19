import requests
from dotenv import load_dotenv
import os
import time
import json
import certifi
import sys
from datetime import datetime

load_dotenv()  # 默认会读取 .env 文件
cookies = {
    "SESSION": os.getenv("SESSION")
}

def bark():
    url = "https://api.day.app/VfdheAWDPBRmF4h9d5d4mC/学科网来题了?level=critical&call=1"
    requests.post(url)

def execute_specific_script():
    url_high = "https://qbm.xkw.com/console/question-tasks/blind-pick?courseids=35&phase=p3"
    num = 15
    for _ in range(num):
        response = requests.get(url_high, cookies=cookies, verify=certifi.where())
        if response.status_code != 200:
            break
    bark()

def check_status(url, cookies):
    """轮询检查状态，直到执行特定函数后退出，提示信息包含当前时间"""
    while True:
        try:
            res = requests.get(url, cookies=cookies, verify=certifi.where())
            res.raise_for_status()
            
            data = json.loads(res.text)
            
            if "items" in data and isinstance(data["items"], list) and len(data["items"]) > 0:
                first_item = data["items"][0]
                if "type" in first_item and first_item["type"] == 11:
                    execute_specific_script()
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 已领取题目，退出轮询")
                    return data
            
            # 输出当前时间和提示信息，时间格式为：年-月-日 时:分:秒
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] 未检测到目标条件，1秒后重试...")
            
        except requests.exceptions.RequestException as e:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] 请求发生错误: {e}，1秒后重试...")
        except json.JSONDecodeError as e:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] JSON解析错误: {e}，1秒后重试...")
        except Exception as e:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] 发生意外错误: {e}，1秒后重试...")
        
        time.sleep(1)

if __name__ == "__main__":

    # 替换为实际的URL和cookies
    target_url = "https://qbm.xkw.com/console/question-tasks?courseid=35&currentpage=1&pagesize=50&status=0"
    
    print("开始监控状态...")
    check_status(target_url, cookies)
    print("处理完成")
