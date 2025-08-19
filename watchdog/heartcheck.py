import requests
from dotenv import load_dotenv
import os
import time
import json
import certifi
import sys

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
            sys.exit(1)
    bark()

def check_status(url, cookies):
    """检查状态并根据action执行相应操作"""
    while True:
        try:
            # 发送请求
            res = requests.get(url, cookies=cookies, verify=certifi.where())
            res.raise_for_status()  # 检查请求是否成功
            
            # 解析JSON响应
            data = json.loads(res.text)
            
            # 确保数据是列表且不为空
            if not isinstance(data, list) or len(data) == 0:
                print("返回数据格式不正确，不是非空列表")
                time.sleep(5)  # 默认等待5秒后重试
                continue
            
            # 获取第一个元素的action
            first_item = data[0]
            action = first_item.get("action", "")
            print(f"当前action: {action}")
            
            # 根据不同的action执行不同操作
            if action == "开始查重" or action == "人工干预跳过查重":
                print(f"检测到'{action}'，将进行1分钟轮询")
                time.sleep(60)  # 1分钟轮询
            elif action == "受理抽审任务":
                print(f"检测到'{action}'，将进行1秒轮询")
                time.sleep(1)  # 1秒轮询
            elif action in ["拆解岗审核通过", "解析挂起"]:
                print(f"检测到'{action}'，将执行特定脚本")
                execute_specific_script()
                break  # 执行完脚本后退出循环
            else:
                print(f"未知action: {action}，5秒后重试")
                break
        
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}，10秒后重试")
            time.sleep(10)
        except json.JSONDecodeError:
            print("JSON解析错误，10秒后重试")
            time.sleep(10)
        except Exception as e:
            print(f"发生未知错误: {e}，10秒后重试")
            time.sleep(10)

if __name__ == "__main__":
    # 替换为实际的URL和cookies
    target_url = "https://qbm.xkw.com/console/paperLogs/3820204168036352"
    
    print("开始监控状态...")
    check_status(target_url, cookies)
    print("处理完成")