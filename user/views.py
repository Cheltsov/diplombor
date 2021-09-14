from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render

from adminer.core.data import createJsonPolls, getPostJson
from adminer.models import Polls, UserAnswer


def index(request, id):
    if Polls.objects.filter(id=id, date_start__isnull=False, date_end__isnull=True).exists():
        polls = [Polls.objects.get(id=id)]
        content = {
            'polls': createJsonPolls(polls)
        }
        return render(request, 'user/index.html', content)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def create_user_answer(request, id):
    if request.method == 'POST':
        response = 'false'
        request_user_answer = getPostJson(request, 'getdata')
        list_user_answer = []
        for item in request_user_answer:
            list_user_answer.append(UserAnswer(id_polls_id=id,
                                               id_question_id=item['id_question'],
                                               id_answer_id=item['id_answer'],
                                               ip=item['ip']))
        if UserAnswer.objects.bulk_create(list_user_answer):
            response = 'true'
        return HttpResponse(response)
    return HttpResponseNotFound('<h1>Page not found</h1>')
