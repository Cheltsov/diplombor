from adminer.models import *


def deleteQuestionAnswerByPattern(pattern):
    try:
        questions = pattern.question_set.all()
        for question in questions:
            question.answer_set.all().delete()
        questions.delete()
        return True
    except Exception as ex:
        print(ex)
        return False


def createQuestionAnswerByPattern(request_pattern, id_pattern):
    try:
        list_answer = []
        for question in request_pattern:
            ques = Question(title=question['title'], id_pattern_id=id_pattern, is_verbal=question['is_verbal'])
            ques.save()

            if ques.is_verbal == '1':
                for answer in question['answers']:
                    list_answer.append(Answer(title=answer, id_question_id=ques.id))
            else:
                for answer in range(int(question['answers'][0])):
                    list_answer.append(Answer(title=(answer + 1), id_question_id=ques.id))

            Answer.objects.bulk_create(list_answer)
            if not calculateAnswer(id_question=ques.id):
                return False
        return True
    except Exception as ex:
        print(ex)
        return False


def calculateAnswer(id_question):
    list_answer = Answer.objects.filter(id_question_id=id_question)
    count_answer = len(list_answer)
    for index, answer in enumerate(list_answer):
        step = 100 / (count_answer - 1)
        answer.cost = step * index
        answer.save()
    return True
