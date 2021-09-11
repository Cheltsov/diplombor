import json


def getPostJson(request, key):
    request_body = request.POST.get(key, None)
    list_json = json.loads(request_body)
    return list_json


def createJsonQuestion(questions):
    ques_json = []
    for question in questions:
        ques_json.append({
            "id": question.id,
            "title": question.title,
            "answers": question.answer_set.all(),
            'is_verbal': question.is_verbal,
        })
    return ques_json
