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

import requests                             # 请求库
import certifi                              # 证书库
# import pickque                      # 领取题目
# import pickque_review               # 领取审核题目
# import querytask                    # 查询任务
# import querytask_review             # 查询解析任务
# import judgetype                  # 判断题目类型（目前只做了选择题的判断）
# import getdetail_choice             # 获取选择题的题干、选项、答案
# import getdetail_judge              # 获取判断题的题干、答案
# import getdetail_blank              # 获取填空题的题干、答案
# import getdetail_short              # 获取简答题的题干、答案
# import getbornwithoutanswer         # 获取题目是否有答案 

# import gptapi_choice                # 调用grok-beta解答选择题
# import gptapi_judge                 # 调用grok-beta解答判断题
# import gptapi_blank                 # 调用grok-beta解答填空题
# import gptapi_short                 # 调用grok-beta解答简答题

# import doubao_choice                # 调用Doubao-pro解答选择题
# import doubao_judge                 # 调用Doubao-pro解答判断题
# import doubao_blank                 # 调用Doubao-pro解答填空题
# import doubao_short                 # 调用Doubao-pro解答简答题

# import getdetail_choice_review      # 获取选择题的题干、选项、答案、解析、题型、章节目录、知识点
# import getdetail_judge_review       # 获取判断题的题干、答案、解析、题型、章节目录、知识点
# import getdetail_blank_review       # 获取填空题的题干、答案、解析、题型、章节目录、知识点
# import getdetail_short_review       # 获取简答题的题干、答案、解析、题型、章节目录、知识点

# import doubao_choice_review         # 审核选择题
# import doubao_judge_review          # 审核判断题
# import doubao_blank_review          # 审核填空题
# import doubao_short_review          # 审核简答题

# import putanswer                    # 将API的结果处理并提交
# import puttag                       # 修改题目标签
# import copytag                      # 复制题目标签
import submit                       # 提交整个题目
# import submit_review                # 提交审核题目
# import trainmodel                 # 模型微调
import random                       # 随机数字生成
import time                         # 时间统计
import logging                      # 日志
import re                           # 正则表达式
import tkinter as tk                # 应用程序包
from tkinter import ttk             # 样式包
from tkinter import messagebox      # 用于弹出消息框

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

# # cookies是全局变量，每次登录之后获取一下，感觉可以改成环境变量
# cookies = {
#     "SESSION": "OGE3MmY1YzQtZTIyMS00ODQyLWIwNTYtZTAwNGQ1OWU4NmI2"
# }

# 目前已经领取的题号列表，后续是希望能更改为一个字典的形式
# tasks = []


# 领取初中题目，直到任务池满，任务池大小默认15
# TODO：动态获取任务池大小
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


# # 领取初中审核题目，直到任务池满，任务池大小默认15
# def pick_junior_review_all():

#     start_time = time.time()  # 记录开始时间
#     num = 1

#     for _ in range(num):
#         pickque_review.junior(cookies)

#     end_time = time.time()  # 记录结束时间
#     duration = end_time - start_time  # 计算花费的时间
#     logging.info(f"pick_junior_review_all 完成，花费时间: {duration:.2f}秒")

# # 领取高中审核题目，直到任务池满，任务池大小默认15
# def pick_high_review_all():
    
#     start_time = time.time()  # 记录开始时间

#     # qids = querytask.main(cookies)[1]
#     # num = 15 - len(qids)
#     num = 10

#     for _ in range(num):
#         pickque_review.high(cookies)
    
#     end_time = time.time()  # 记录结束时间
#     duration = end_time - start_time  # 计算花费的时间
#     logging.info(f"pick_high_review_all 完成，花费时间: {duration:.2f}秒")



# 一键提交所有题目
def all_submit():
    ids = querytask.main(cookies)[0]
    for id in ids:
        submit.main(id, cookies)

# def all_review_submit():
#     ids = querytask_review.main(cookies)[0]
#     for id in ids:
#         submit_review.main(id, cookies)


# 我们拿到一个题号之后，需要首先判断其类型，因为答案时有时无，我们在此考虑暂时使用stem去判断题目的类型
# 这里开始写处理选择题的代码，我们无法提前得知该题目是单选还是多选，因此在这里先统一按照单选去处理
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
        # if bornwithoutanswer:
        #     # 这里需要进行答案填充
        #     if type == '0101' or type == '0102':
        #         putanswer.put_answer_choice(qid, cookies, type)
        #     elif type == '02':
        #         putanswer.put_answer_blank(qid, cookies, type)
        #     elif type == '03':
        #         putanswer.put_answer_judge(qid, cookies, type)
        #     elif type == '04':
        #         print(f'目前暂不支持，类型为操作题')
        #     elif type == '05':
        #         print(f'目前暂不支持，类型为简答题')
        #     else:
        #         print(f'目前暂不支持，类型为综合题')
        # else:

        puttag.main(qid, cookies, type)
    # tag_all(3768454354354176)
    # end_time = time.time()  # 记录结束时间
    # duration = end_time - start_time  # 计算花费的时间
    # logging.info(f"solve_all 完成，花费时间: {duration:.2f}秒")

# def tag_all():
#     qids = query_task()[1]
#     # indices = [0]
#     # qids = [qids[i] for i in indices]
#     for qid in qids:
#         type = judgetype.main(qid, cookies)
#         if type == '01':
#             type = judgetype.choice(qid, cookies)[2:]
#         puttag.main(qid, cookies, type)

# def tag_all(sour_qid):
#     qids = query_task()[1]
#     # qids = [qids[i] for i in indices]
#     for qid in qids:
#         type = judgetype.main(qid, cookies)
#         if type == '01':
#             type = judgetype.choice(qid, cookies)[2:]
#         copytag.main(sour_qid, qid, cookies, type)

# def channel():

#     loop_count = 1  # 初始化循环次数

#     while True:

#         loop_start_time = time.time()
#         logging.info(f"第 {loop_count} 次循环开始，时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(loop_start_time))}")

#         pick_junior_all()

#         solve_all()           # 串行处理

#         random_number = random.randint(100, 999)
#         print(f"系统生成的三位数是：{random_number}")
#         user_input_start_time = time.time()

#         user_input = input("请在完成所有题目的检查之后，输入上面系统生成的三位数：")

#         while user_input != str(random_number):
#             user_input = input("输入错误，请重新输入：")

#         user_input_end_time = time.time()
#         user_input_duration = user_input_end_time - user_input_start_time
#         logging.info(f"用户检查修正，花费时间: {user_input_duration:.2f}秒")

#         all_submit()

#         loop_end_time = time.time()
#         loop_duration = loop_end_time - loop_start_time
#         logging.info(f"第 {loop_count} 次循环结束，耗时: {loop_duration:.2f}秒")

#         continue_input = input("是否继续下一轮？(yes/no): ").strip().lower()
#         if continue_input == 'no':
#             print("解题结束，快去愉快的享受生活吧。")
#             break  # 如果用户输入no，退出循环

#         loop_count += 1

# def verify_session(session):

#     cookies = {
#         "SESSION": session
#     }

#     url = "https://qbm.xkw.com/console/account/userinfo"
#     response = requests.get(url, cookies=cookies, verify=certifi.where())
#     if 'application/json' in response.headers['Content-Type'] and response.json()['info']['authc']['principal']['login']['id'] == 61883486:
#         return True
#     else:
#         return False

# 点击按钮时的事件处理函数
# def on_submit():
#     session_input = entry_session.get("1.0", "end-1c")  # 获取用户输入的SESSION
#     global cookies
#     if verify_session(session_input):  # 验证SESSION
#         messagebox.showinfo("验证通过", "SESSION正确")
#         cookies['session'] = session_input
#         # 在这里可以放置继续后续操作的代码，比如打开新的窗口或执行其他函数
#     else:
#         messagebox.showerror("验证失败", "SESSION不正确，请重新输入。")

# def review_choice(qid):
#     question = getdetail_choice_review.main(qid, cookies)
#     result = doubao_choice_review.main(question)
#     print(f'题目{qid}的审核结果是{result}')
# def review_blank(qid):
#     question = getdetail_blank_review.main(qid, cookies)
#     result = doubao_blank_review.main(question)
#     print(f'题目{qid}的审核结果是{result}')
# def review_judge(qid):
#     question = getdetail_judge_review.main(qid, cookies)
#     result = doubao_judge_review.main(question)
#     print(f'题目{qid}的审核结果是{result}')
# def review_short(qid):
#     question = getdetail_short_review.main(qid, cookies)
#     result = doubao_short_review.main(question)
#     print(f'题目{qid}的审核结果是{result}')
    
# def auto_review():
#     # 首先，有可能没有当前的catalogid，需要加一下
#     ids = querytask_review.main(cookies)[0]
#     qids = querytask_review.main(cookies)[1]
#     for id in ids:
#         print(f"{id}正在人工智能审核中")
#     for qid in qids:
#         type = judgetype.gettype(qid, cookies)
#         if type == '200101' or type == '200102' or type == '350101' or type == '350102':
#             review_choice(qid)
#         elif type == '2002' or type == '3502':
#             review_blank(qid)
#         elif type == '2003' or type == '3503':
#             review_judge(qid)
#         elif type == '2005' or type == '3505':
#             review_short(qid)
#         else:
#             print(f'题目{qid}目前暂不支持')
#         puttag.orgin(qid, cookies)             # 添加可能没有添加的那个标签

if __name__ == '__main__':


    # pick_high_all()
    # channel()

    # all_review_submit()
    # pick_high_review_all()
    # auto_review()

    # all_review_submit()
    # pick_junior_review_all()
    # auto_review()

    # all_submit()
    # pick_high_all()
    # solve_all()

    # all_submit()
    # pick_junior_all()
    solve_all()
    # tag_all()

    # print(judgetype.main(3783987290005504, cookies))

    # tag_all(3768570181066752)

    # qid = 3727539247685632
    # answer_text = """本题考查物联网的相关知识。在门铃远程通知系统中，输入模块是门铃端，作为发布者；输出模块是用户端，作为订阅者；计算模块是 MQTT 服务器，作为连接两者的桥梁，实现对输入和输出模块的控制。如果门铃被按下，则向MQTT服务器的主题发送消息，所以门铃按下是数据传递的触发条件。故答案为触发。"""
    # putanswer.main(qid, cookies, answer_text)

    # qid = 3640915508764672
    # question = getdetail_choice.main(qid, cookies)
    # print(question)


    # pick_high_all()
    # solve_all()

    # root = tk.Tk()
    # # 设置窗口大小
    # width = 800
    # height = 600
    # root.geometry(f"{width}x{height}")
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()
    # position_top = int((screen_height - height) / 2)
    # position_left = int((screen_width - width) / 2)
    # root.geometry(f"{width}x{height}+{position_left}+{position_top}")
    # root.title("学科网自动答题脚本")

    # root.configure(bg="#f0f0f0")

    # style = ttk.Style()

    # style.configure("TLabel", font=("Arial", 20))  # 设置字体和大小

    # # 配置按钮字体大小
    # style.configure("TButton", font=("Arial", 20, "bold"))  # 设置字体和大小

    # frame = ttk.Frame(root)
    # frame.pack(expand=True)  # 让框架充满窗口，控件将相对于框架居中

    # label = ttk.Label(frame, text="请输入SESSION：", style="TLabel", background="#f0f0f0")
    # label.pack(pady=10)

    # entry_session = tk.Text(frame, font=("Arial", 20), height=3, width=30)  # 设置字体、行高和列宽
    # entry_session.pack(pady=13)

    # btn_solve_all = ttk.Button(frame, text="提交", style="TButton", command=on_submit)
    # btn_solve_all.pack(pady=10)

    # root.mainloop()



