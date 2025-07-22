import requests
import certifi

def main(cookies, pointid, courseId):
    
    url = "https://qbm.xkw.com/console/books/catalogs/infer-catalog?courseid=" + str(courseId) + "&kpointids=" + str(pointid)

    response = requests.get(url, cookies=cookies ,verify=certifi.where())
    json_str = response.json()
    return json_str