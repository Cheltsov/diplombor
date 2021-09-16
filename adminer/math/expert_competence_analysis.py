import numpy as np
import scipy.stats
from adminer.models import *


def getCompetencyRatio(count_user):
    return 1 / count_user


def floatCost(cost):
    if cost > 0:
        return cost / 100
    else:
        return 0


def getSumAnswer(id_poll):
    list_sum_question = []
    questions = UserAnswer.objects.filter(id_polls_id=id_poll, is_category=False).values('id_question_id').distinct()
    for question in questions:
        sum_question = 0
        if UserAnswer.objects.filter(id_question_id=question['id_question_id'], id_polls_id=id_poll,
                                     is_category=False).exists():
            list_user_answer = UserAnswer.objects.filter(id_question_id=question['id_question_id'], id_polls_id=id_poll,
                                                         is_category=False)
            for user_answer in list_user_answer:
                e1 = floatCost(user_answer.id_answer.cost)
                sum_question = round((sum_question + e1), 2)
            list_sum_question.append(sum_question)
    return list_sum_question


def getAnswerByQuestion(id_poll, id_question):
    list_answer_cost = []
    if UserAnswer.objects.filter(id_question_id=id_question, id_polls_id=id_poll,
                                 is_category=False).exists():
        list_user_answer = UserAnswer.objects.filter(id_question_id=id_question, id_polls_id=id_poll,
                                                     is_category=False)
        for user_answer in list_user_answer:
            e1 = floatCost(user_answer.id_answer.cost)
            list_answer_cost.append(e1)
    return list_answer_cost


def getS1Answer(id_poll):
    list_s1 = []
    questions = UserAnswer.objects.filter(id_polls_id=id_poll, is_category=False).values('id_question_id').distinct()
    for question in questions:
        s1 = 0
        if UserAnswer.objects.filter(id_question_id=question['id_question_id'], id_polls_id=31,
                                     is_category=False).exists():
            list_user_answer = UserAnswer.objects.filter(id_question_id=question['id_question_id'], id_polls_id=31,
                                                         is_category=False)
            for user_answer in list_user_answer:
                e1 = floatCost(user_answer.id_answer.cost)
                s1 = round((s1 + (e1 / len(list_user_answer))), 2)
            list_s1.append(s1)
    return list_s1


def getM(listSum, listS1):
    mo = 0
    for item in range(len(listSum)):
        mo = mo + (listSum[item] * listS1[item])
    return mo


def getAnswerByUser(id_poll, user):
    list_answer = []
    if UserAnswer.objects.filter(id_polls_id=id_poll, user=user, is_category=False).exists():
        user_answers = UserAnswer.objects.filter(id_polls_id=id_poll, user=user, is_category=False)
        for user_answer in user_answers:
            list_answer.append(floatCost(user_answer.id_answer.cost))
    return list_answer


def getQi(listS1, listE1, M):
    return np.sum(listS1 * listE1) / M


def getSAnswer(id_poll, listQ1):
    list_s2 = []
    questions = UserAnswer.objects.filter(id_polls_id=id_poll, is_category=False).values('id_question_id').distinct()
    for question in questions:
        list_e1 = []
        sl_list = []
        if UserAnswer.objects.filter(id_question_id=question['id_question_id'], id_polls_id=31,
                                     is_category=False).exists():
            list_user_answer = UserAnswer.objects.filter(id_question_id=question['id_question_id'], id_polls_id=31,
                                                         is_category=False)
            for user_answer in list_user_answer:
                e1 = floatCost(user_answer.id_answer.cost)
                list_e1.append(e1)

            sr = 0
            for item in range(len(list_e1)):
                sr = sr + (list_e1[item] * listQ1[item])
            list_s2.append(sr)
    return list_s2


def getArrQ(experts, array_sum, array_s1):
    array_q1 = []
    m = getM(listSum=array_sum, listS1=array_s1)
    for expert in experts:
        array_e1 = np.array(getAnswerByUser(id_poll=31, user=expert['user']))
        array_q1.append(getQi(listS1=array_s1, listE1=array_e1, M=m))
    array_s2 = getSAnswer(id_poll=31, listQ1=np.array(array_q1))
    return m, array_q1, array_s2


def mainer():
    array_sum = np.array(getSumAnswer(31))
    array_s = np.array(getS1Answer(31))

    # Получить всех экспертов
    experts = UserAnswer.objects.filter(id_polls_id=31).values('user').distinct()

    list_m = []
    list_q = [[
        getCompetencyRatio(len(experts)),
        getCompetencyRatio(len(experts)),
        getCompetencyRatio(len(experts)),
        getCompetencyRatio(len(experts)),
        getCompetencyRatio(len(experts))
    ]]
    list_s = []

    for expert in range(len(experts) + 1):
        m, array_q1, array_s = getArrQ(experts=experts, array_sum=array_sum, array_s1=array_s)
        list_m.append(m)
        list_q.append(array_q1)
        list_s.append(array_s)
    print(np.array(list_m))
    print(np.array(list_q))
    print(np.array(list_s))

    list_qmin = []
    for item in range(1, len(experts) + 1):
        sum_q = 0

        q_line1 = list_q[item]
        q_line2 = list_q[(item - 1)]

        for i in range(len(q_line1)):
            qsum1 = q_line1[i]
            qsum2 = q_line2[i]
            qmin = abs(qsum1 - qsum2)
            sum_q = sum_q + qmin
        list_qmin.append(sum_q)

    rank_q = scipy.stats.rankdata(list_q[-1])

    exit()
