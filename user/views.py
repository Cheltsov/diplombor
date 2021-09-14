from django.http import HttpResponseNotFound
from django.shortcuts import render

from adminer.core.data import createJsonPolls
from adminer.models import Polls


def index(request, id):
    if Polls.objects.filter(id=id).exists():
        polls = [Polls.objects.get(id=id)]
        content = {
            'polls': createJsonPolls(polls)
        }
        return render(request, 'user/index.html', content)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def create_user_answer(request):
    pass
