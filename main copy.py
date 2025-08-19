from utils import querytask                 # 查询我的任务池中的题目
from utils import pickque                   # 题目领取，包含初中和高中
from utils import judgetype                 # 题目类型判断
from utils import getbornwithoutanswer      # 判断是否初始无答案

from getdetail import getdetail_choice      # 获取选择题的题干、选项、答案
from getdetail import getdetail_judge       # 获取判断题的题干、答案
from getdetail import getdetail_blank       # 获取填空题的题干、答案
from getdetail import getdetail_short       # 获取简答题的题干、答案

from doubaoapi import doubao_choice         # 调用Doubao-pro解答选择题
from doubaoapi import doubao_judge          # 调用Doubao-pro解答判断题
from doubaoapi import doubao_blank          # 调用Doubao-pro解答填空题
from doubaoapi import doubao_short          # 调用Doubao-pro解答简答题

from submit import putanswer                # 答案填充
from submit import putanalysis              # 解析填充
from submit import submit

from tag import puttag

import submit                       # 提交整个题目
import random                       # 随机数字生成
import time                         # 时间统计
import logging                      # 日志
import re                           # 正则表达式

from dotenv import load_dotenv
import os

load_dotenv()  # 默认会读取 .env 文件
cookies = {
    "SESSION": os.getenv("SESSION")
}

# 设置日志记录
logging.basicConfig(
    filename='task_log.txt',  # 日志文件名
    level=logging.INFO,       # 设置日志级别为INFO
    format='%(asctime)s - %(message)s',  # 日志格式
)


# 领取初中题目，直到任务池满，任务池大小默认15

def pick_junior_all():

    # start_time = time.time()  # 记录开始时间

    pickque.pick_junior_all(cookies)

    # end_time = time.time()  # 记录结束时间
    # duration = end_time - start_time  # 计算花费的时间
    # logging.info(f"pick_junior_all 完成，花费时间: {duration:.2f}秒")

# 领取高中题目，直到任务池满，任务池大小默认15
def pick_high_all():
    
    # start_time = time.time()  # 记录开始时间

    qids = querytask.main(cookies)[1]
    num = 15 - len(qids)

    for _ in range(num):
        pickque.pick_high(cookies)
    
    # end_time = time.time()  # 记录结束时间
    # duration = end_time - start_time  # 计算花费的时间
    # logging.info(f"pick_high_all 完成，花费时间: {duration:.2f}秒")

# 一键提交所有题目
def all_submit():
    ids = querytask.main(cookies)[0]
    for id in ids:
        submit.main(id, cookies)

# 下面处理选择题
def solve_choice(qid):

    question = getdetail_choice.main(qid, cookies)
    answer_text = doubao_choice.main(question)
    putanalysis.main(qid, cookies, answer_text)

# 下面处理判断题
def solve_judge(qid):

    question = getdetail_judge.main(qid, cookies)
    answer_text = doubao_judge.main(question)
    putanalysis.main(qid, cookies, answer_text)

# 下面处理填空题
def solve_blank(qid):

    question = getdetail_blank.main(qid, cookies)
    answer_text = doubao_blank.main(question)
    putanalysis.main(qid, cookies, answer_text)

# 下面处理简答题
def solve_short(qid):

    question = getdetail_short.main(qid, cookies)
    answer_text = doubao_short.main(question)
    putanalysis.main(qid, cookies, answer_text)


# 下面处理综合题，有难度，待定
# def solve_compre(qid):

#     question = getdetail_compre.main(qid, cookies)
#     answer_text = doubao_short.main(question)
#     putanswer.main(qid, cookies, answer_text)

# 一次处理所有题目
def solve_all():

    # start_time = time.time()  # 记录开始时间
    qids = querytask.main(cookies)[1]
    for qid in qids:

        bornwithoutanswer = getbornwithoutanswer.main(qid ,cookies) # 判断题是否无答案
        type = judgetype.main(qid, cookies)
        if type == '01':
            solve_choice(qid)
            type = judgetype.choice(qid, cookies)[2:]
            putanswer.choice(qid, cookies, bornwithoutanswer)
        elif type == '02':
            solve_blank(qid)
            putanswer.blank(qid, cookies, bornwithoutanswer)
        elif type == '03':
            solve_judge(qid)
            putanswer.judge(qid, cookies, bornwithoutanswer)
        elif type == '04':
            print(f'题目{qid}目前暂不支持，类型为操作题')
            print(f'题目{qid}目前暂不支持，类型为操作题')
        elif type == '05':
            solve_short(qid)
            print(f'题目{qid}目前暂不支持，类型为简答题')
        else:
            print(f'题目{qid}目前暂不支持，类型为综合题')
            print(f'题目{qid}目前暂不支持，类型为综合题')

        puttag.main(qid, cookies, type)

    # end_time = time.time()  # 记录结束时间
    # duration = end_time - start_time  # 计算花费的时间
    # logging.info(f"solve_all 完成，花费时间: {duration:.2f}秒")

def tag_all():

    qids = querytask.main(cookies)[1]
    for qid in qids:
        type = judgetype.main(qid, cookies)
        if type == '01':
            type = judgetype.choice(qid, cookies)[2:]
        puttag.main(qid, cookies, type)

if __name__ == '__main__':

    # all_submit()
    # pick_junior_all()
    # solve_all()
    tag_all()
