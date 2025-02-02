# -*- coding: utf-8 -*-
# @Time : 2021/11/2 16:34
# @Author : Melon
# @Site : 
# @Note : 
# @File : workMain.py
# @Software: PyCharm
import json
import logging
import random
import time

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = 'https://mooc.icve.com.cn'

# 获取我加入的所有课程
GET_MY_COURSE_URL = BASE_URL + '/portal/Course/getMyCourse'

# 获取本课程 作业/测验/考试 ID api
GET_WORK_EXAM_LIST_URL = BASE_URL + '/study/workExam/getWorkExamList'

# 做作业 api
WORK_EXAM_PREVIEW_URL = BASE_URL + '/study/workExam/workExamPreview'

# 提交作业/测验 api
WORK_EXAM_SAVE_URL = BASE_URL + '/study/workExam/workExamSave'

# 提交考试 api
ONLINE_EXAM_SAVE_URL = BASE_URL + '/study/workExam/onlineExamSave'

# 查看答案
WORK_EXAM_HISTORY_URL = BASE_URL + '/study/workExam/history'

# 查看作答列表
WORK_EXAM_DETAIL_URL = BASE_URL + '/study/workExam/detail'

# 填题目
ONLINE_HOMEWORK_ANSWER = BASE_URL + '/study/workExam/onlineHomeworkAnswer'

# 填题目(填空题)
ONLINE_HOMEWORK_CHECK_SPACE = BASE_URL + '/study/workExam/onlineHomeworkCheckSpace'

# 退出课程
COURSE_WITHDRAW_COURSE = BASE_URL + '/portal/Course/withdrawCourse'

# 获取该课程所有开课信息(一般最新的开课可以加入)
GET_ALL_COURSE_CLASS_URL = BASE_URL + '/portal/Course/getAllCourseClass'

# 用 courseOpenId 去添加课程
ADD_MY_MOOC_COURSE = BASE_URL + '/study/Learn/addMyMoocCourse'


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}


def getMyCourse(cookies):  # 1 我的课程列表
    time.sleep(0.25)
    get = requests.get(url=GET_MY_COURSE_URL, params={'isFinished': 0, 'pageSize': 1000000}, cookies=cookies, headers=HEADERS)
    return get.json()


def getWorkExamList(cookies, course_open_id, work_exam_type):  # 2 获取作业 考试 测验
    time.sleep(0.25)
    params = {
        'pageSize': 50000,
        'courseOpenId': course_open_id,
        'workExamType': work_exam_type  # 0是作业，1是测验，2是考试
    }
    get = requests.get(url=GET_WORK_EXAM_LIST_URL, params=params, cookies=cookies, headers=HEADERS)
    return get.json()  # 添加课程成功返回


def workExamPreview(cookies, work_exam_id):  # 3 做作业
    time.sleep(0.25)
    params = {
        'workExamId': work_exam_id,
    }
    post = requests.post(url=WORK_EXAM_PREVIEW_URL, params=params, cookies=cookies, headers=HEADERS)
    return post.json()


def workExamSave(cookies, unique_id, work_exam_id, work_exam_type):  # 4 交作业
    time.sleep(0.5)
    params = {
        'uniqueId': unique_id,
        'workExamType': work_exam_type,
        'useTime': random.randint(300, 1000)  # 答题时间随机
    }
    if work_exam_type == 2:
        params['examId'] = work_exam_id
        post = requests.post(url=ONLINE_EXAM_SAVE_URL, params=params, cookies=cookies, headers=HEADERS)
    else:
        params['workExamId'] = work_exam_id
        post = requests.post(url=WORK_EXAM_SAVE_URL, params=params, cookies=cookies, headers=HEADERS)
    return post.json()


def workExamDetail(cookies, work_exam_id, course_open_id):  # 5 查看作答列表
    time.sleep(0.25)
    params = {
        'workExamId': work_exam_id,
        'courseOpenId': course_open_id
    }
    post = requests.post(url=WORK_EXAM_DETAIL_URL, params=params, cookies=cookies, headers=HEADERS)
    return post.json()


def onlineHomeworkAnswer(cookies, question_id, answer, question_type, unique_id):  # 6 填答题卡
    time.sleep(0.5)
    params = {
        'questionId': question_id,
        'answer': answer,
        'questionType': question_type,
        'uniqueId': unique_id
    }
    post = requests.post(url=ONLINE_HOMEWORK_ANSWER, data=params, cookies=cookies, headers=HEADERS)
    return post.json()


def onlineHomeworkCheckSpace(cookies, question_id, answer, question_type, unique_id):  # 6 填答题卡
    time.sleep(0.5)
    params = {
        'questionId': question_id,
        'answer': "",
        'answerJson': str([{"Content": answer}]),
        'questionType': question_type,
        'uniqueId': unique_id
    }
    post = requests.post(url=ONLINE_HOMEWORK_CHECK_SPACE, params=params, cookies=cookies, headers=HEADERS)
    return post.json()


def workExamHistory(cookies, work_exam_id, student_work_id, course_open_id):  # 7 获取答案
    time.sleep(0.25)
    params = {
        'workExamId': work_exam_id,
        'studentWorkId': student_work_id,
        'courseOpenId': course_open_id
    }
    post = requests.post(url=WORK_EXAM_HISTORY_URL, params=params, cookies=cookies, headers=HEADERS)
    return post.json()


def withdrawCourse(cookies, course_open_id, user_id):  # 8 退出课程
    time.sleep(0.25)
    params = {
        'courseOpenId': course_open_id,
        'userId': user_id
    }
    post = requests.post(url=COURSE_WITHDRAW_COURSE, params=params, cookies=cookies, headers=HEADERS)
    return post.json()


def addMyMoocCourse(cookies, course_open_id, verify_code=None, vc_ck=None):  # 3 添加到我的课程
    time.sleep(0.25)
    params = {
        'courseOpenId': course_open_id,
        'courseId': ''
    }
    if verify_code:
        params['verifycode'] = verify_code
        cookies['verifycode'] = vc_ck
    get = requests.post(url=ADD_MY_MOOC_COURSE, params=params, cookies=cookies, headers=HEADERS)
    return get.json()  # 添加课程成功返回


work_exam_type_map = {0: '作业', 1: '测验', 2: '考试'}
question_type_type_map = {
    1: '单选题',
    2: '多选题',
    3: '判断题',
    4: '填空题',
    5: '填空题',
    6: '问答题',
    7: '匹配题',
    8: '阅读理解',
    9: '完形填空',
    10: '文件作答',
    11: '视听题',
}


def run_start_work(ck1, ck2, work_exam_type, course_open_id, is_work_score):
    exam_list = getWorkExamList(ck1, course_open_id, work_exam_type)
    for exam_item in exam_list['list']:
        if exam_item['getScore'] > is_work_score:
            print('\t1. 当前{%s}: \t分数:%s \t大于预设分数: %s \t不答题 \t【%s】' % (
                work_exam_type_map[work_exam_type], exam_item['getScore'], is_work_score, exam_item['Title']))
            continue
        print('\t1. 当前{%s}:【%s】' % (work_exam_type_map[work_exam_type], exam_item['Title']))
        work_exam_answer_map = run_get_answer(ck2, work_exam_type, course_open_id, exam_item['Id'])
        work_exam_preview = workExamPreview(ck1, exam_item['Id'])
        work_exam_questions = json.loads(work_exam_preview['workExamData'])['questions']
        answer_count = 0
        # 循环题目
        for i in work_exam_questions:
            # 查找答案
            answer_map = work_exam_answer_map.get(i['questionId'], None)
            if answer_map:
                if not answer_map['Answer']:
                    print('\t\t\t3. 作答中... 结果: 找到答案，但答案为空！ \t类型 %s \t题目: %s' % (
                        question_type_type_map.get(answer_map['questionType'], '未知'), i['TitleText']))
                    continue
                # TODO: 填空题的特殊处理 (大学生创业基础 黄河水利职业技术学院 所属专业: 公共基础课)
                if answer_map['questionType'] == 5:
                    if len(i['answerList']) > 1:
                        print('\t\t\t3. 作答中... 结果: 多个填空，暂不支持，输出答案请注意提取！ \t类型 %s \t题目: %s \t答案: %s' % (
                            question_type_type_map.get(answer_map['questionType'], '未知'), i['TitleText'],
                            answer_map['Answer']))
                        continue
                    answer_res = onlineHomeworkCheckSpace(ck1, i['questionId'], answer_map['Answer'],
                                                          answer_map['questionType'], work_exam_preview['uniqueId'])
                # TODO: 匹配题的特殊处理 暂时没有处理（毛泽东思想和中国特色社会主义 课程负责人：张小兰 开课名称：第八次开课 作业：第一章作业
                elif answer_map['questionType'] == 7:
                    print('\t\t\t3. 作答中... 结果: 匹配题暂不支持，输出答案请注意提取！ \t类型 %s \t题目: %s \t答案: %s' % (
                        question_type_type_map.get(answer_map['questionType'], '未知'), i['TitleText'],
                        answer_map['Answer']))
                    continue
                # TODO: 阅读理解题的特殊处理 暂时没有处理（毛泽东思想和中国特色社会主义 课程负责人：张小兰 开课名称：第八次开课 作业：第一章作业
                elif answer_map['questionType'] == 8:
                    print('\t\t\t3. 作答中... 结果: 阅读理解题暂不支持，输出答案请注意提取！ \t类型 %s \t题目: %s \t答案: %s' % (
                        question_type_type_map.get(answer_map['questionType'], '未知'), i['TitleText'],
                        answer_map['Answer']))
                    continue
                else:
                    answer_res = onlineHomeworkAnswer(ck1, i['questionId'], answer_map['Answer'],
                                                      answer_map['questionType'], work_exam_preview['uniqueId'])
                if answer_res['code'] == 1:
                    answer_count += 1

                if answer_map['questionType'] == 1:
                    answer_map['Answer'] = chr(97 + int(answer_map['Answer'].replace(",", ""))).upper()
                if answer_map['questionType'] == 2:
                    answer_map['Answer'] = ', '.join(
                        [chr(97 + int(x)).upper() for x in answer_map['Answer'].split(",") if x is not ''])
                if answer_map['questionType'] == 3:
                    answer_map['Answer'] = '正确' if answer_map['Answer'] == '1' else '错误'
                print('\t\t\t3. 作答中... 结果: %s \t类型: %s \t答案: %s \t题目: %s' % (
                    answer_res.get('allDo', answer_res.get('msg', answer_res['code'])),
                    question_type_type_map[answer_map['questionType']],
                    answer_map['Answer'], i['TitleText']))
            else:
                print('\t\t\t3. 作答中... 结果: 未找到答案！ \t类型 %s \t题目: %s' % (
                    question_type_type_map[i['questionType']], i['TitleText']))
        if len(work_exam_questions) == answer_count:
            work_exam_save_res = workExamSave(ck1, work_exam_preview['uniqueId'], exam_item['Id'], work_exam_type)
            print('\t\t\t\t4. ^v^ 提交作业... 【%s】\t 状态: %s' % (exam_item['Title'], work_exam_save_res['msg']))
        else:
            print('\t\t\t\t4. ~_~ 提交作业... 【%s】\t 状态: 未提交！请前往网页手动提交！注意作答时长！' % (exam_item['Title']))


def run_get_answer(cookies, work_exam_type, course_open_id, work_exam_id):
    work_exam_answer_map = {}
    work_exam_list = getWorkExamList(cookies, course_open_id, work_exam_type)
    for work_exam in [i for i in work_exam_list['list'] if i['Id'] == work_exam_id]:
        # 如果没有答案 ID 就进行做作业
        if work_exam['stuWorkExamId'] == '':
            # 通过作业ID去交作业(必须先点做作业)
            work_exam_preview = workExamPreview(cookies, work_exam['Id'])
            work_exam_save_res = workExamSave(cookies, work_exam_preview['uniqueId'], work_exam['Id'], work_exam_type)
            msg = work_exam_save_res['msg']
        else:
            msg = '当前作业已存在作答记录!'
        # 作业提交成功后，获取我做的所有作业记录，取第一条里面有答案ID
        work_exam_detail = workExamDetail(cookies, work_exam['Id'], course_open_id)
        if not work_exam_detail['list']:
            continue
        work_exam_history = workExamHistory(cookies, work_exam['Id'], work_exam_detail['list'][0]['Id'], course_open_id)
        for i in json.loads(work_exam_history['workExamData'])['questions']:
            work_exam_answer_map[i['questionId']] = {
                'questionType': i['questionType'],
                'Answer': i['Answer'],
            }
        print('\t\t2. 生成题库中...\t当前{%s}: 【%s】 \t%s' % (work_exam_type_map[work_exam_type], work_exam['Title'], msg))
    return work_exam_answer_map
