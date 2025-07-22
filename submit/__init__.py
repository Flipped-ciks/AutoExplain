import requests
import certifi

def main(id, cookies):
    
    url = "https://qbm.xkw.com/console/question-tasks/"+str(id)+"/submit"
    requests.post(url, cookies=cookies, verify=certifi.where())