import requests
import certifi

def main(cookies):

    ids = []
    qids = []
    url = "https://qbm.xkw.com/console/question-tasks/my-task-overview"
    response = requests.get(url, cookies=cookies, verify=certifi.where())

    json_str = response.json()
    for task in json_str['questionTasks']:
        ids.append(task['id'])
        qids.append(task['qid'])
            
    return ids, qids
