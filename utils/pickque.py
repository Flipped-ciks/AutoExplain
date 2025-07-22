import requests
import certifi
from utils import querytask

# 领取初中题目，至任务池满，任务池大小默认15
def pick_junior_all(cookies):
    url_junior = "https://qbm.xkw.com/console/question-tasks/blind-pick?courseids=20&phase=p3"
    num = 15 - len(querytask.main(cookies)[1])
    for _ in range(num):
        requests.get(url_junior, cookies=cookies, verify=certifi.where())

# 领取高中题目，至任务池满，任务池大小默认15
def pick_high_all(cookies):
    url_high = "https://qbm.xkw.com/console/question-tasks/blind-pick?courseids=35&phase=p3"
    num = 15 - len(querytask.main(cookies)[1])
    for _ in range(num):
        requests.get(url_high, cookies=cookies, verify=certifi.where())

