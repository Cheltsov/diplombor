import json


def getPostJson(request, key):
    request_body = request.POST.get(key, None)
    list_json = json.loads(request_body)
    return list_json


def createJsonQuestion(questions, answer=False):
    ques_json = []
    for question in questions:
        list_answer = question.answer_set.all()
        if answer:
            list_answer = createJsonAnswer(list_answer)
        ques_json.append({
            "id": question.id,
            "title": question.title,
            "answers": list_answer,
            "is_verbal": question.is_verbal,
            "id_category": question.id_category_id
        })
    return ques_json


def createJsonAnswer(answers):
    ans_json = []
    for answer in answers:
        ans_json.append({
            "id": answer.id,
            "title": answer.title,
            "cost": answer.cost,
        })
    return ans_json


def createJsonCategory(categories):
    category_json = []
    for category in categories:
        category_json.append({
            "id": category.id,
            "title": category.title,
            "questions": createJsonQuestion(category.question_set.all(), True)
        })
    return category_json


def createJsonPattern(patterns):
    pattern_json = []
    for pattern in patterns:
        pattern_json.append({
            "id": pattern.id,
            "title": pattern.title,
            "questions": createJsonQuestion(pattern.question_set.all(), True)
        })
    return pattern_json


def createJsonPolls(polls):
    polls_json = []
    for poll in polls:
        status = "Не начат"
        if poll.date_start and poll.date_end:
            status = "Завершен"
        elif poll.date_start and not poll.date_end:
            status = "Начат"

        polls_json.append({
            "id": poll.id,
            "title": poll.title,
            "description": poll.description,
            "questions": createJsonQuestion(poll.question_set.all(), True),
            "date_start": poll.date_start,
            "date_end": poll.date_end,
            "date_created": poll.date_created,
            "date_updated": poll.date_updated,
            "status": status,
            "answer_user": poll.useranswer_set.count()
        })
    return polls_json


