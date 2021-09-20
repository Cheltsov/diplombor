import numpy as np
import scipy.stats
import pandas as pd

from adminer.math.modules.Math import Math
from adminer.models import *


class CompetenceExpert(Math):

    def getSumAnswer(self):
        list_sum_question = []
        for question in self.questions:
            sum_question = 0
            list_user_answer = self.getUserAnswersRow(id_question=question['id_question_id'], id_category=self.id_category)
            for user_answer in list_user_answer:
                e1 = self.floatCost(user_answer.id_answer.cost)
                sum_question = round((sum_question + e1), 2)
            list_sum_question.append(sum_question)
        return list_sum_question

    def getAnswerByQuestion(self, id_question):
        list_answer_cost = []
        list_user_answer = self.getUserAnswersRow(id_question=id_question, id_category=self.id_category)
        for user_answer in list_user_answer:
            e1 = self.floatCost(user_answer.id_answer.cost)
            list_answer_cost.append(e1)
        return list_answer_cost

    def getS1Answer(self):
        list_s1 = []
        questions = self.questions
        for question in questions:
            s1 = 0
            list_user_answer = self.getUserAnswersRow(id_question=question['id_question_id'], id_category=self.id_category)
            for user_answer in list_user_answer:
                e1 = self.floatCost(user_answer.id_answer.cost)
                s1 = round((s1 + (e1 / len(list_user_answer))), 2)
            list_s1.append(s1)
        return list_s1

    @staticmethod
    def getM(listSum, listS1):
        mo = 0
        for item in range(len(listSum)):
            mo = mo + (listSum[item] * listS1[item])
        return mo

    def getAnswerByUser(self, user):
        list_answer = []
        if self.id_category:
            if UserAnswer.objects.filter(id_polls_id=self.id_poll, user=user, is_category=False, id_category=self.id_category).exists():
                user_answers = UserAnswer.objects.filter(id_polls_id=self.id_poll, user=user, is_category=False, id_category=self.id_category)
                for user_answer in user_answers:
                    list_answer.append(self.floatCost(user_answer.id_answer.cost))
        else:
            if UserAnswer.objects.filter(id_polls_id=self.id_poll, user=user, is_category=False).exists():
                user_answers = UserAnswer.objects.filter(id_polls_id=self.id_poll, user=user, is_category=False)
                for user_answer in user_answers:
                    list_answer.append(self.floatCost(user_answer.id_answer.cost))
        return list_answer

    @staticmethod
    def getQi(listS1, listE1, M):
        return np.sum(listS1 * listE1) / M

    def getSAnswer(self, listQ1):
        list_s2 = []
        questions = self.questions
        for question in questions:
            list_e1 = []
            list_user_answer = self.getUserAnswersRow(id_question=question['id_question_id'], id_category=self.id_category)
            for user_answer in list_user_answer:
                e1 = self.floatCost(user_answer.id_answer.cost)
                list_e1.append(e1)
            sr = 0
            for item in range(len(list_e1)):
                sr = sr + (list_e1[item] * listQ1[item])
            list_s2.append(sr)
        return list_s2

    def getArrQ(self, experts, array_sum, array_s1):
        array_q1 = []
        m = self.getM(listSum=array_sum, listS1=array_s1)
        for expert in experts:
            array_e1 = np.array(self.getAnswerByUser(user=expert['user']))
            array_q1.append(self.getQi(listS1=array_s1, listE1=array_e1, M=m))
        array_s2 = self.getSAnswer(listQ1=np.array(array_q1))
        return m, array_q1, array_s2

    def main(self):
        # Вывод входных данных
        self.list_cost = self.getMatr()

        array_sum = np.array(self.getSumAnswer())
        array_s = np.array(self.getS1Answer())
        list_s1 = array_s

        # Получить всех экспертов
        experts = self.getExperts()

        self.list_q = [[
            self.getCompetencyRatio(len(experts)),
            self.getCompetencyRatio(len(experts)),
            self.getCompetencyRatio(len(experts)),
            self.getCompetencyRatio(len(experts)),
            self.getCompetencyRatio(len(experts))
        ]]

        for expert in range(len(experts) + 1):
            m, array_q1, array_s = self.getArrQ(experts=experts, array_sum=array_sum, array_s1=array_s)
            self.list_m.append(m)
            self.list_q.append(array_q1)
            self.list_s.append(array_s)

        list_qmin = []
        for item in range(1, len(experts) + 1):
            sum_q = 0

            q_line1 = self.list_q[item]
            q_line2 = self.list_q[(item - 1)]

            for i in range(len(q_line1)):
                if len(q_line1) > i and len(q_line2) > i:
                    qsum1 = q_line1[i]
                    qsum2 = q_line2[i]
                    qmin = abs(qsum1 - qsum2)
                    sum_q = sum_q + qmin
            list_qmin.append(sum_q)

        S1 = pd.Series(self.list_q[-1])
        self.rank_q = list(S1.rank())

        list_s6 = self.getSAnswer(self.list_q[-1])
        return list_s1, list_s6

    def getMark(self):
        rezult = []
        for question in self.questions:
            sum_answer = 0
            for i, answer in enumerate(self.getUserAnswersRow(id_question=question['id_question_id'])):
                sum_answer = sum_answer + (self.floatCost(answer.id_answer.cost) * self.list_q[-1][i])
            rezult.append(sum_answer)
        return np.array(rezult)
