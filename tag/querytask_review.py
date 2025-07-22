import requests
import certifi

def main(cookies):

    ids = []
    qids = []
    url = "https://qbm.xkw.com/console/question-task-audits?searchstate=my-auditing"
    response = requests.get(url, cookies=cookies, verify=certifi.where())

    json_str = response.json()
    for task in json_str['items']:

        ids.append(task['id'])
        qids.append(task['qid'])
        
    return ids, qids
