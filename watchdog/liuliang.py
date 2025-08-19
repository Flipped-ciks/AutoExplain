import requests
import json

def calculate_request_size(request):
    """计算请求的总大小（请求头 + 请求体）"""
    # 计算请求头大小
    headers_size = 0
    for key, value in request.headers.items():
        # 每个请求头的格式是 "Key: Value\r\n"
        headers_size += len(f"{key}: {value}\r\n")
    
    # 计算请求行大小（例如: "GET /path HTTP/1.1\r\n"）
    request_line = f"{request.method} {request.url} {request.headers.get('User-Agent', '').split(' ')[-1]}\r\n"
    headers_size += len(request_line)
    
    # 计算请求体大小
    body_size = len(request.body) if request.body else 0
    
    return headers_size + body_size

def calculate_response_size(response):
    """计算响应的总大小（响应头 + 响应体）"""
    # 计算响应头大小
    headers_size = 0
    for key, value in response.headers.items():
        headers_size += len(f"{key}: {value}\r\n")
    
    # 计算状态行大小（例如: "HTTP/1.1 200 OK\r\n"）
    status_line = f"HTTP/1.1 {response.status_code} {response.reason}\r\n"
    headers_size += len(status_line)
    
    # 计算响应体大小
    body_size = len(response.content)
    
    return headers_size + body_size

def check_status(target_url, cookies):
    try:
        # 创建一个会话
        session = requests.Session()
        
        # 准备请求
        request = requests.Request('GET', target_url, cookies=cookies)
        prepared_request = session.prepare_request(request)
        
        # 发送请求
        response = session.send(prepared_request)
        response.raise_for_status()  # 检查是否有HTTP错误
        
        # 计算流量大小
        request_size = calculate_request_size(prepared_request)
        response_size = calculate_response_size(response)
        total_size = request_size + response_size
        
        # 转换为更易读的单位
        def format_size(size):
            for unit in ['B', 'KB', 'MB']:
                if size < 1024.0:
                    return f"{size:.2f} {unit}"
                size /= 1024.0
            return f"{size:.2f} GB"
        
        print(f"请求大小: {format_size(request_size)}")
        print(f"响应大小: {format_size(response_size)}")
        print(f"总流量: {format_size(total_size)}")
        
        return response
    
    except Exception as e:
        print(f"请求发生错误: {str(e)}")
        return None

# 使用示例
if __name__ == "__main__":
    # 替换为实际的URL和cookies
    target_url = "https://qbm.xkw.com/console/question-tasks?courseid=35&currentpage=1&pagesize=50&status=0"
    cookies = {
        "SESSION": "M2Y0MDI0OTMtNGI0NS00MDg4LWI2YjctNTVkMWNhZTk2ZDAy"
    }
    
    print("开始监控状态...")
    check_status(target_url, cookies)
    print("处理完成")