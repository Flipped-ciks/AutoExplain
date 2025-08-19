import requests
import certifi
# import prePointIds
# import inferCatlog


# cookies = {
#   "SESSION": "OGJjY2E3OWMtZTNiMy00NTFjLWFlNjktZTIyNjNkYTM5MjIw"
# }

# 由于有两项，年份以及来源是从get请求获取的，因此我们在发put请求之前，先拉去一下这两个参数

def main(sour_qid, dest_qid, cookies, type):

    if(sour_qid):

        url = "https://qbm.xkw.com/console/questions/properties/" + str(sour_qid)
        response = requests.get(url, cookies=cookies ,verify=certifi.where())
        json_sour = response.json()

        url = "https://qbm.xkw.com/console/questions/properties/" + str(dest_qid)
        response = requests.get(url, cookies=cookies ,verify=certifi.where())
        json_dest = response.json()

        predict_url = f"https://qbm.xkw.com/console/question-aigc/ai-predict-kpoint?questionid={dest_qid}&repredict=true&toptypeid={(str(json_dest['courseId']) + type[:2])}"
        res = requests.get(predict_url, cookies=cookies)

        data = {}
        data['year'] = json_dest['year']                                                 # 年份由get请求获取
        data['source'] = json_dest['source']                                             # 来源由get请求获取
        data['typeId'] = str(json_dest['courseId']) + type                               # 题型由参数传入
        data['difficulty'] = json_sour['difficulty']                                     # 难度默认值
        data['tagIds'] = ['1']                                                           # 试题分类默认值
        data['knowledgePointIds'] = res.json()['predictedPointIds']                      # 试题知识点根据学科网预测获取
        # data['knowledgePointIds'] = [59025, 59055]                      # 试题知识点根据学科网预测获取
        data['catalogIds'] = json_sour['catalogIds']                                     # 章节目录根据学科网接口获取
        # data['catalogIds'].append(285613)
        if(type == '0101'):
            data['typeFeatureIds'] = ['200101']
            data['typeFeatureNames'] = ['单选']
            data['difficulty']  = 0.9000000000000001
        elif(type == '0102'):
            data['typeFeatureIds'] = ['200102']
            data['typeFeatureNames'] = ['多选']
            data['difficulty']  = 0.8500000000000001
        elif(type == '02' or type == '03'):
            data['difficulty'] = 0.8500000000000001
        else:
            data['difficulty'] = 0.6500000000000001
        res = requests.put(url, cookies=cookies, json=data, verify=certifi.where())
