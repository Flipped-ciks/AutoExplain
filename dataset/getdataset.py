import requests
import certifi
import judgetype
import xkwautosolve.getdetail_choice_withexplain as getdetail_choice_withexplain
import gptapi_choice
import pymysql
import json
from datetime import datetime, timedelta

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "abc123",
    "database": "xkwdatabase",
    "charset": "utf8mb4"
}

# 创建数据库连接
def connect_to_database():
    try:
        connection = pymysql.connect(**db_config)
        print("Database connection established.")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        return None
    
def close_database_connection(connection):
    if connection:
        connection.close()
        print("Database connection closed.")

# 插入数据函数
def insert_question(connection, qid, stem, options, answer, original, final):
    # 将选项转换为 JSON 字符串
    options_json = json.dumps(options, ensure_ascii=False)
    
    # 构建 SQL 插入语句
    sql = """
        INSERT INTO questions (qid, stem, options, answer, original, final)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            stem = VALUES(stem),
            options = VALUES(options),
            answer = VALUES(answer),
            original = VALUES(original),
            final = VALUES(final);
    """
    
    try:
        # 创建游标并执行插入
        with connection.cursor() as cursor:
            cursor.execute(sql, (qid, stem, options_json, answer, original, final))
        connection.commit()  # 提交事务
        print(f"Question {qid} inserted/updated successfully.")
        
    except pymysql.MySQLError as e:
        print(f"Error inserting/updating question {qid}: {e}")

def time_pre(time):

    date_obj = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    new_date_obj = date_obj - timedelta(days=1)
    return new_date_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")



# 每一次循环处理一天的数据

maxendtime = "2024-11-15T16:00:00.000Z"
# maxendtime = time_pre(maxendtime)

minendtime = "2024-11-14T16:00:00.000Z"
# minendtime = time_pre(minendtime)

db_connection = connect_to_database()


cookies = {
    "SESSION": "NjdlNmEzYWMtYTFiOS00MjI3LTljY2ItYWE1MjcwNzE4NDg4"
}

for i in range(365):

    url = "https://qbm.xkw.com/console/question-tasks/completed?maxendtime=" + maxendtime + "&minendtime=" + minendtime + "&onlymistake=false"

    response = requests.get(url, cookies=cookies, verify=certifi.where())
    questions = response.json()

    if questions:
        for question in questions:
            if question['courseId'] == 20 and judgetype.main(int(question['qid']), cookies) == '200101':
                problem, _ ,final  = getdetail_choice_withexplain.main(int(question['qid']), cookies)
                original = gptapi_choice.main(problem)
                insert_question(db_connection, int(question['qid']), problem['stem'], problem['options'], problem['answer'], original, final)

    maxendtime = time_pre(maxendtime)
    minendtime = time_pre(minendtime)

    print(i)

close_database_connection(db_connection)
