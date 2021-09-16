from adminer.models import *
import numpy as np


class Math:
    answerRowByIdQuestion = []
    listExperts = []

    def __init__(self, id_poll):
        self.id_poll = id_poll
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
    def existUserAnswers(id_question):
        if UserAnswer.objects.filter(id_question_id=id_question, is_category=False).exist():
            return True
        else:
            return False

    @staticmethod
    def getUserAnswersRow(id_question):
        return UserAnswer.objects.filter(id_question_id=id_question, is_category=False)

    def getExperts(self):
        if not self.listExperts:
            self.listExperts = UserAnswer.objects.filter(id_polls_id=self.id_poll).values('user').distinct()
        return self.listExperts

    def getMatr(self):
        list_math = []
        for question in self.questions:
            list_answers = []
            for answer in self.getUserAnswersRow(id_question=question['id_question_id']):
                list_answers.append(self.floatCost(answer.id_answer.cost))
            list_math.append(list_answers)
        list_math = np.array(list_math)
        return list_math


