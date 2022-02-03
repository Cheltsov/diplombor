from adminer.models import *
from itertools import groupby


def deleteQuestionAnswerByPatternOrPolls(pattern):
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
        QuestionI = 1
        for question in request_pattern:
            lastIdQuestion = Question.objects.latest('id').id + QuestionI
            ques = Question(id=lastIdQuestion,
                            title=question['title'],
                            id_pattern_id=id_pattern,
                            is_verbal=question['is_verbal'],
                            sort=question['sort'])
            ques.save()
            QuestionI = QuestionI + 1
            list_answer = []
            if ques.is_verbal == '1':
                AnswerI = 1
                for answer in question['answers']:
                    lastIdAnswer = Answer.objects.lastest('id').id + AnswerI
                    list_answer.append(Answer(id=lastIdAnswer, title=answer['title'], sort=answer['sort'], id_question_id=ques.id))
                    AnswerI = AnswerI + 1
            else:
                AnswerI = 1
                for answer in range(int(question['answers'][0])):
                    lastIdAnswer = Answer.objects.lastest('id').id + AnswerI
                    list_answer.append(Answer(id=lastIdAnswer, title=(answer + 1), id_question_id=ques.id))
                    AnswerI = AnswerI + 1

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


def deleteQuestionAnswerByCategory(category):
    try:
        questions = category.question_set.all()
        for question in questions:
            question.answer_set.all().delete()
        questions.delete()
        return True
    except Exception as ex:
        print(ex)
        return False


def createQuestionAnswerByCategory(request_category, id_category):
    try:
        QuestionI = 1
        for question in request_category:
            lastQuestion_id = Question.objects.latest('id').id + QuestionI
            ques = Question(id=lastQuestion_id, title=question['title'], id_category_id=id_category)
            ques.save()
            QuestionI = QuestionI + 1
            list_answer = []
            i = 1
            for answer in question['answers']:
                last_id = Answer.objects.latest('id').id + i
                list_answer.append(Answer(id=last_id, title=answer, id_question_id=ques.id))
                i = i + 1
            Answer.objects.bulk_create(list_answer)
            if not calculateAnswer(id_question=ques.id):
                return False
        return True
    except Exception as ex:
        print(ex)
        return False


def addCategoryInPattern(request_category, id_pattern):
    try:
        CategoryPattern.objects.filter(id_pattern_id=id_pattern).delete()
        list_category_pattern = []
        for item in request_category:
            list_category_pattern.append(CategoryPattern(id_category_id=item, id_pattern_id=id_pattern))
        CategoryPattern.objects.bulk_create(list_category_pattern)
        return True
    except Exception as ex:
        print(ex)
        return False


def createQuestionAnswerByPolls(request_polls, id_polls):
    try:
        for question in request_polls:
            ques = Question(title=question['title'], id_polls_id=id_polls, is_verbal=question['is_verbal'], sort=question['sort'])
            ques.save()
            list_answer = []
            if ques.is_verbal == '1':
                for answer in question['answers']:
                    list_answer.append(Answer(title=answer['title'], sort=answer['sort'], id_question_id=ques.id))
            else:
                for answer in range(int(question['answers'][0])):
                    list_answer.append(Answer(title=(answer + 1), sort=answer, id_question_id=ques.id))

            Answer.objects.bulk_create(list_answer)
            if not calculateAnswer(id_question=ques.id):
                return False
        return True
    except Exception as ex:
        print(ex)
        return False


def addCategoryInPolls(request_category, id_polls):
    try:
        CategoryPolls.objects.filter(id_polls_id=id_polls).delete()
        list_category_polls = []
        for item in request_category:
            list_category_polls.append(CategoryPolls(id_category_id=item, id_polls_id=id_polls))
        CategoryPolls.objects.bulk_create(list_category_polls)
        return True
    except Exception as ex:
        print(ex)
        return False


def getCategoryInPoll(id_poll):
    list_category = []
    for item in UserAnswer.objects.filter(id_polls_id=id_poll, is_category=True).values('id_question_id')\
            .distinct().order_by('id_question_id'):
        list_answer = []
        for itemAnswer in UserAnswer.objects.filter(id_polls_id=id_poll,
                                                    is_category=True, id_question_id=item['id_question_id'])\
                .values('id_answer_id').distinct().order_by('id_answer_id'):
            list_answer.append(Answer.objects.get(id=itemAnswer['id_answer_id']))
        list_category.append([el for el, _ in groupby(list_answer)])
    return list_category
