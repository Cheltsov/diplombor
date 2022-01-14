from adminer.models import *
import numpy as np
from collections import Counter
from django.db.models import Sum
from statistics import mean


class Math:
    listUserAnswer = []

    answerRowByIdQuestion = []
    listExperts = []

    list_m = []
    list_q = []
    list_s = []
    rank_q = []
    list_max = []
    list_cost = []

    min_count_expert = 0

    def __init__(self, id_poll, id_category=None):
        self.id_poll = id_poll
        self.id_category = id_category
        if self.id_category:
            self.questions = UserAnswer.objects.filter(id_polls_id=id_poll, id_category_id=id_category,
                                                       is_category=False).values('id_question_id').distinct()
        else:
            self.questions = UserAnswer.objects.filter(id_polls_id=id_poll, is_category=False).values(
                'id_question_id').distinct()

    @staticmethod
    def getCompetencyRatio(count_user):
        return 1 / count_user

    @staticmethod
    def floatCost(cost):
        decCost = 0
        if cost > 0:
            decCost = cost / 100
        return decCost

    @staticmethod
    def existUserAnswers(id_question, id_category=None):
        if id_category:
            if UserAnswer.objects.filter(id_question_id=id_question, id_category_id=id_category, is_category=False).exist():
                return True
            else:
                return False
        else:
            if UserAnswer.objects.filter(id_question_id=id_question, is_category=False).exist():
                return True
            else:
                return False

    def getUserAnswersRow(self, id_question, id_category=None):
        if id_category:
            self.listUserAnswer = UserAnswer.objects.filter(id_question_id=id_question, id_category_id=id_category,
                                                            is_category=False).order_by('id')
        else:
            self.listUserAnswer = UserAnswer.objects.filter(id_question_id=id_question, is_category=False) \
                .order_by('id')
        return self.listUserAnswer

    def getCostUserAnswersRow(self, id_question, id_category=None, limit=None):
        if id_category:

            if limit:
                result = UserAnswer.objects.values_list('answer_cost', flat=True).filter(id_question_id=id_question,
                                                                                         id_category_id=id_category,
                                                                                         is_category=False).order_by(
                    'id')[:limit]
            else:
                result = UserAnswer.objects.values_list('answer_cost', flat=True).filter(id_question_id=id_question,
                                                                                         id_category_id=id_category,
                                                                                         is_category=False).order_by(
                    'id')
        else:
            if limit:
                result = UserAnswer.objects.values_list('answer_cost', flat=True).filter(id_question_id=id_question,
                                                                                         is_category=False) \
                             .order_by('id')[:limit]

            else:
                result = UserAnswer.objects.values_list('answer_cost', flat=True).filter(id_question_id=id_question,
                                                                                         is_category=False) \
                    .order_by('id')
        return list(result)

    def getSumUserAnswersRow(self, id_question, id_category=None):
        if id_category:
            result = UserAnswer.objects.filter(id_question_id=id_question, id_category_id=id_category,
                                                            is_category=False).aggregate(Sum('answer_cost'))
        else:
            result = UserAnswer.objects.filter(id_question_id=id_question, is_category=False) \
                .aggregate(Sum('answer_cost'))
        return result['answer_cost__sum']


    def getExperts(self):
        if self.id_category:
            if not self.listExperts:
                self.listExperts = UserAnswer.objects.filter(id_polls_id=self.id_poll, id_category_id=self.id_category).values('user').distinct()
            return self.listExperts
        else:
            if not self.listExperts:
                self.listExperts = UserAnswer.objects.filter(id_polls_id=self.id_poll).values('user').distinct()
            return self.listExperts

    def getMatr(self):
        list_math = []
        list_s1 = []
        if self.id_category:
            for question in self.questions:
                list_cost = self.getCostUserAnswersRow(id_question=question['id_question_id'],
                                                       id_category=self.id_category)
                list_s1.append(round(mean(list_cost), 2))
                list_math.append(list_cost)
            list_math = np.array(list_math)
        else:
            for question in self.questions:
                list_cost = self.getCostUserAnswersRow(id_question=question['id_question_id'],
                                                       id_category=self.id_category)

                list_s1.append(round(mean(list_cost), 2))
                list_math.append(list_cost)
            list_math = np.array(list_math)

        return list_math, list_s1

    def getMatrWord(self):
        list_math = []
        if self.id_category:
            for question in self.questions:
                list_answers = []
                for answer in self.getUserAnswersRow(id_question=question['id_question_id'],
                                                     id_category=self.id_category):
                    list_answers.append(answer.id_answer.title)
                list_math.append(Counter(list_answers))
        else:
            for question in self.questions:
                list_answers = []
                for answer in self.getUserAnswersRow(id_question=question['id_question_id']):
                    list_answers.append(answer.id_answer.title)
                list_math.append(Counter(list_answers))

        return list_math
