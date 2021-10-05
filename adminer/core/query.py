from adminer.models import *


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
        for question in request_pattern:
            ques = Question(title=question['title'], id_pattern_id=id_pattern, is_verbal=question['is_verbal'])
            ques.save()
            list_answer = []
            if ques.is_verbal == '1':
                for answer in question['answers']:
                    list_answer.append(Answer(title=answer['title'], sort=answer['sort'], id_question_id=ques.id))
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
        for question in request_category:
            ques = Question(title=question['title'], id_category_id=id_category)
            ques.save()
            list_answer = []
            for answer in question['answers']:
                list_answer.append(Answer(title=answer, id_question_id=ques.id))
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
            ques = Question(title=question['title'], id_polls_id=id_polls, is_verbal=question['is_verbal'])
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
    list_category = UserAnswer.objects.filter(id_polls_id=id_poll, is_category=True)[0].id_question.answer_set.all()
    return list_category
