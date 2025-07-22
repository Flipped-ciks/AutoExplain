import requests
import certifi

def main(id, cookies):

    url = "https://qbm.xkw.com/console/question-task-audits/" + str(id)
    requests.post(url, cookies=cookies, json=[] ,verify=certifi.where())