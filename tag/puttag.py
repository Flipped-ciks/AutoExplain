import requests
import certifi
from tag import copytag
from tag import prePointIds
from utils import inferCatlog


# def main(qid, cookies, type):

#     data = {}

#     # 获取年份来源两项参数，共用url
#     url = "https://qbm.xkw.com/console/questions/properties/" + str(qid)
#     response = requests.get(url, cookies=cookies ,verify=certifi.where())
#     json_str = response.json()

#     data['year'] = json_str['year']                                                  # 年份由get请求获取
#     data['source'] = json_str['source']                                              # 来源由get请求获取
#     data['typeId'] = str(json_str['courseId']) + type                                # 题型由参数传入
#     data['difficulty'] = '0.9450000000000001'                                        # 难度默认值
#     data['tagIds'] = ['1']                                                           # 试题分类默认值
#     pointid = prePointIds.main(qid, cookies, str(json_str['courseId']) + type)                                                          
#     data['knowledgePointIds'] = [pointid]                                            # 试题知识点根据学科网接口获取
#     data['catalogIds'] = inferCatlog.main(cookies, pointid, json_str['courseId'])    # 章节目录根据学科网接口获取
#     data['catalogIds'].extend(get_paper_catalogIds(qid, cookies))
#     if(type == '0101'):
#         data['typeFeatureIds'] = ['200101']
#         data['typeFeatureNames'] = ['单选']
#     if(type == '0102'):
#         data['typeFeatureIds'] = ['200102']
#         data['typeFeatureNames'] = ['多选']
#     requests.put(url, cookies=cookies, json=data, verify=certifi.where())


def pretag(qid, cookies, type):

    data = {}

    # 获取年份来源两项参数，共用url
    url = "https://qbm.xkw.com/console/questions/properties/" + str(qid)
    response = requests.get(url, cookies=cookies ,verify=certifi.where())
    json_str = response.json()

    data['year'] = json_str['year']                                                  # 年份由get请求获取
    data['source'] = json_str['source']                                              # 来源由get请求获取
    data['typeId'] = str(json_str['courseId']) + type                                # 题型由参数传入
    data['difficulty'] = '0.9450000000000001'                                        # 难度默认值
    data['tagIds'] = ['1']                                                           # 试题分类默认值
    pointid = prePointIds.main(qid, cookies, str(json_str['courseId']) + type)                                                          
    data['knowledgePointIds'] = [pointid]                                            # 试题知识点根据学科网接口获取
    data['catalogIds'] = inferCatlog.main(cookies, pointid, json_str['courseId'])    # 章节目录根据学科网接口获取
    data['catalogIds'].extend(get_paper_catalogIds(qid, cookies))
    if(type == '0101'):
        data['typeFeatureIds'] = ['200101']
        data['typeFeatureNames'] = ['单选']
    if(type == '0102'):
        data['typeFeatureIds'] = ['200102']
        data['typeFeatureNames'] = ['多选']
    requests.put(url, cookies=cookies, json=data, verify=certifi.where())

def main(qid, cookies, type):
    
    copytag.main(get_similar(qid, cookies), qid, cookies, type)

def get_similar(qid, cookies):
    url = "https://qbm.xkw.com/console/questions/similar"
    json_data = {
        "count": 10,
        "courseId": 20,
        "text": f"{qid}"
    }
    response = requests.post(url, cookies=cookies, json=json_data,verify=certifi.where())
    ids = [q["id"] for q in response.json() if q["status"] == "P4"]
    if(len(ids)):
        return(ids[0])
    else:
        return 0


def orgin(qid, cookies):

    data = {}
    url = "https://qbm.xkw.com/console/questions/properties/" + str(qid)
    response = requests.get(url, cookies=cookies ,verify=certifi.where())
    json_str = response.json()
    data = json_str
    data['catalogIds'].extend(get_paper_catalogIds(qid, cookies))
    requests.put(url, cookies=cookies, json=data, verify=certifi.where())

def orgin_copy(qid, cookies):

    data = {}
    url = "https://qbm.xkw.com/console/questions/properties/" + str(qid)
    response = requests.get(url, cookies=cookies ,verify=certifi.where())
    json_str = response.json()
    data = json_str
    data['typeId'] = '2006'
    requests.put(url, cookies=cookies, json=data, verify=certifi.where())

def get_paper_catalogIds(qid, cookies):

    url = "https://qbm.xkw.com/console/papers/" + qid + "/catalogIds"
    response = requests.get(url, cookies=cookies ,verify=certifi.where())
    json_str = response.json()
    return json_str
