import math
import pandas as pd
import scipy.stats

from adminer.math.modules.ListPearcon import getListPearson
from adminer.math.modules.Math import Math
from adminer.models import *
import numpy as np


class ConsistencyEstimates(Math):

    sumTi = 0
    S = 0
    W = 0
    word_cost = ''
    A = 0
    word_coord = ''

    def RepetitionsAssessments(self):
        first_question = Question.objects.get(id=self.questions[0]['id_question_id'])
        list_answer_cost = first_question.answer_set.order_by('id').all().values_list('cost', flat=True)
        return list_answer_cost

    def CountingNumberRepetitions(self):
        list_answer_cost = self.RepetitionsAssessments()
        sumTi_def = 0
        list_ex = self.getExperts()
        for user in self.getExperts():
            sum_cube = 0
            for answer_cost in list_answer_cost:
                cost_expert = UserAnswer.objects.filter(id_polls_id=self.id_poll, user=user['user'], answer_cost=(answer_cost/100), is_category=False).count()
                if cost_expert > 1:
                    sum_cube = sum_cube + ((math.pow(cost_expert, 3) - cost_expert) / 12)
            sumTi_def = sumTi_def + sum_cube
        self.sumTi = sumTi_def

    def CountingRanks(self):
        list_rank = []
        for user in self.getExperts():
            list_answer = UserAnswer.objects.filter(id_polls_id=self.id_poll, user=user['user'], is_category=False).values_list('answer_cost', flat=True)
            S1 = pd.Series(list_answer)
            r = list(S1.rank())
            list_rank.append(r)

        matrix = np.array(list_rank)
        matrix_rank = matrix.swapaxes(0, 1)

        list_question_sum_rank = []
        all_sum_rank = 0
        for item_rank in matrix_rank:
            sum_rank = 0
            for rank in item_rank:
                sum_rank = sum_rank + rank
            list_question_sum_rank.append(sum_rank)
            all_sum_rank = all_sum_rank + sum_rank

        middle_rank = all_sum_rank / len(matrix_rank)

        for item in list_question_sum_rank:
            d = math.pow((item - middle_rank), 2)
            self.S = self.S + d

        count_expert = len(self.getExperts())
        count_question = len(self.questions)

        self.W = self.S / ((1/12) * math.pow(count_expert, 2) * (math.pow(count_question, 3) - count_question) - (count_expert * self.sumTi))
        self.W = round(self.W, 2)

    def getWordCost(self):
        if self.W < 0.2:
            self.word_cost = 'Очень низкая'
        elif 0.2 < self.W < 0.35:
            self.word_cost = 'Низкая'
        elif 0.35 < self.W < 0.64:
            self.word_cost = 'Средняя'
        elif 0.64 < self.W < 0.8:
            self.word_cost = 'Высокая'
        elif 0.8 < self.W <= 1:
            self.word_cost = 'Очень высокая'

    def math4(self):
        self.CountingNumberRepetitions()
        self.CountingRanks()
        self.getWordCost()
        return self.word_cost

    def math5(self):

        count_expert = len(self.getExperts())
        count_question = len(self.questions)

        self.A = self.S/((1/12) * count_expert * count_question * (count_question + 1) + (1 / (count_question - 1)) * self.sumTi)
        percent_sens = 20
        countWord = count_question - 1

        k_pearson = getListPearson()[countWord - 1]

        if self.A > k_pearson:
            self.word_coord = 'Не случайно'
        else:
            self.word_coord = 'Случайно'

        return self.word_coord


