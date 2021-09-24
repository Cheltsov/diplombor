import numpy as np
import math

from adminer.math.modules.Math import Math


class CountExpert(Math):
    p = 0.05
    E = 0.05
    cheb = (1 - p) * E * E

    def getMinCountExpert(self):
        self.list_max = []
        # Получить всех экспертов
        experts = self.getExperts()
        list_oo = []
        for question in self.questions:
            list_user_answer = self.getUserAnswersRow(id_question=question['id_question_id'], id_category=self.id_category)
            list_cost = []

            list_min_count_expert = []
            for i in range(3, len(experts) + 1):
                list_min_count_expert.append(i)

            for i in range(3, len(experts) + 1):
                list_c = []
                variance = 0
                for item in list_user_answer[:i]:
                    list_c.append(self.floatCost(item.id_answer.cost))
                    variance = np.var(np.array(list_c))
                list_cost.append(math.ceil((variance / self.cheb)))
            list_oo.append(list_cost)

        matrix = np.array(list_oo)

        if len(matrix) < 1:
            return 0
        else:
            new_matrix = matrix.swapaxes(0, 1)
            for item in new_matrix:
                self.list_max.append(max(item))

            if len(self.list_max) < 1:
                return 0
            else:
                arr_min = np.where(self.list_max == np.min(self.list_max))
                self.min_count_expert = np.max(arr_min) + 3
                return self.min_count_expert
