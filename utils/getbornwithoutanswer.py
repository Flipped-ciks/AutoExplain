import requests
import certifi

def main(qid, cookies):
    
    url = "https://qbm.xkw.com/console/questions/"+ str(qid) +"/detail"

    response = requests.get(url, cookies=cookies, verify=certifi.where())
    json_str = response.json()

    return json_str['bornWithoutAnswer']