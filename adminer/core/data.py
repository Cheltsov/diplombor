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
        polls_json.append({
            "id": poll.id,
            "title": poll.title,
            "description": poll.description,
            "questions": createJsonQuestion(poll.question_set.all(), True)
        })
    return polls_json


