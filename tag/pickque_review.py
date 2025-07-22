import requests
import certifi

"""

    领取解析审核任务
    1. 领取初中信息技术的解析审核任务
    2. 领取高中信息技术的解析审核任务

"""

# 领取初中信息技术的题目
def junior(cookies):
    
    url_junior = "https://qbm.xkw.com/console/question-task-audits/blind-pick?courseid=20"
    response = requests.get(url_junior, cookies=cookies, verify=certifi.where())


# 领取高中信息技术的题目
def high(cookies):

    url_high = "https://qbm.xkw.com/console/question-task-audits/blind-pick?courseid=35"
    requests.get(url_high, cookies=cookies, verify=certifi.where())