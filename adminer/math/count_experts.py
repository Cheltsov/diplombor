from adminer.models import *
import numpy as np
import math


p = 0.05
E = 0.05
cheb = (1 - p) * E * E


def floatCost(cost):
    if cost > 0:
        return cost / 100
    else:
        return 0


def getQ(id_poll):
    # Получить всех экспертов
    experts = UserAnswer.objects.filter(id_polls_id=32).values('user').distinct()
    questions = UserAnswer.objects.filter(id_polls_id=id_poll, is_category=False).values('id_question_id').distinct()

    list_oo = []
    for question in questions:
        if UserAnswer.objects.filter(id_question_id=question['id_question_id'], id_polls_id=id_poll,is_category=False).exists():
            list_user_answer = UserAnswer.objects.filter(id_question_id=question['id_question_id'], id_polls_id=id_poll, is_category=False)
            list_cost = []

            for i in range(3, len(experts)+1):
                list_c = []
                variance = 0
                for item in list_user_answer[:i]:
                    list_c.append(floatCost(item.id_answer.cost))
                    variance = np.var(np.array(list_c))
                list_cost.append(math.ceil((variance / cheb)))
            list_oo.append(list_cost)

    matrix = np.array(list_oo)
    new_matrix = matrix.swapaxes(0, 1)

    list_max = []
    for item in new_matrix:
        list_max.append(max(item))

    return list_max


def mainer():
    r = getQ(32)
    exit()
