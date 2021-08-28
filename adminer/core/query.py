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
            ques = Question(title=question['title'], id_pattern_id=id_pattern)
            ques.save()
            for answer in question['answers']:
                list_answer.append(Answer(title=answer, id_question_id=ques.id))
        Answer.objects.bulk_create(list_answer)
        return True
    except Exception as ex:
        print(ex)
        return False
