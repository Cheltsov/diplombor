import datetime

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from adminer.core.data import *
from adminer.core.query import *
from adminer.models import *


def polls(request):
    if 'admin' in request.session:
        content = {
            "polls": Polls.objects.filter(date_start__isnull=True, date_end__isnull=True).order_by('-date_updated'),
            "polls_start": Polls.objects.filter(date_start__isnull=False, date_end__isnull=True).order_by('-date_updated'),
            "polls_end": Polls.objects.filter(date_start__isnull=False, date_end__isnull=False).order_by('-date_updated'),
        }
        return render(request, 'adminer/polls/polls.html', content)
    else:
        return redirect('auth:auth')


def polls_create(request):
    if 'admin' in request.session and id:
        if request.method == 'POST':
            response = 'false'
            request_polls = getPostJson(request, 'getdata')
            obj_polls = Polls.objects.create(title=request.POST['polls_title'], description=request.POST['polls_desc'])
            obj_polls.save()
            if createQuestionAnswerByPolls(request_polls, obj_polls.id) and \
                    addCategoryInPolls(getPostJson(request, 'polls_category'), obj_polls.id):
                response = 'true'
            return HttpResponse(response)
        content = {
            "categories": createJsonCategory(Category.objects.all()),
            "patterns": createJsonPattern(Pattern.objects.all()),
        }
        content["categories_json"] = json.dumps(content['categories'])
        return render(request, 'adminer/polls/polls_create.html', content)
    else:
        return redirect('auth:auth')


def polls_edit(request, id):
    if 'admin' in request.session and id:
        obj_polls = Polls.objects.get(id=id)
        questions = obj_polls.question_set.all()

        if request.method == 'POST':
            response = 'false'
            request_polls = getPostJson(request, 'getdata')
            obj_polls.title = request.POST['polls_title']
            obj_polls.description = request.POST['polls_desc']
            obj_polls.save()
            if deleteQuestionAnswerByPatternOrPolls(obj_polls) and \
                    createQuestionAnswerByPolls(request_polls, id) and \
                    addCategoryInPolls(getPostJson(request, 'polls_category'), obj_polls.id):
                response = 'true'
            return HttpResponse(response)

        content = {
            "polls": obj_polls,
            "category_polls": createJsonCategory(Category.objects.filter(id__in=obj_polls.categorypolls_set.all().values_list('id_category_id', flat=True))),
            "questions": createJsonQuestion(questions),
            "categories": createJsonCategory(Category.objects.all()),
            "patterns": createJsonPattern(Pattern.objects.all()),
        }

        content["categories_json"] = json.dumps(content['categories'])
        content["patterns_json"] = json.dumps(content['patterns'])
        return render(request, 'adminer/polls/polls_edit.html', content)
    else:
        return redirect('auth:auth')


def polls_delete(request, id):
    if 'admin' in request.session and id:
        Polls.objects.get(id=id).delete()
        return redirect('adminer:polls')
    else:
        return redirect('auth:auth')


def polls_copy(request, id):
    if 'admin' in request.session and id:
        obj = Polls.objects.get(id=id)
        obj.title = obj.title + " - Копия"
        obj.copy()
        return redirect('adminer:polls')
    else:
        return redirect('auth:auth')


def polls_show(request, id):
    if 'admin' in request.session and id:
        if Polls.objects.filter(id=id).exists():
            list_category_id = []
            poll = Polls.objects.get(id=id)
            categories = poll.categorypolls_set.all()
            for item_category in categories:
                list_category_id.append(item_category.id_category_id)
            list_question = createJsonQuestion(Question.objects.filter(id_category_id__in=list_category_id))
            content = {
                'poll': createJsonPolls([poll])[0],
                'categories_question': list_question
            }
            return render(request, 'adminer/polls/polls_show.html', content)
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return redirect('auth:auth')


def polls_start(request, id):
    if 'admin' in request.session and id:
        poll = Polls.objects.get(id=id)
        poll.date_start = datetime.datetime.now()
        poll.save()
        return HttpResponse('true')
    else:
        return redirect('auth:auth')


def polls_end(request, id):
    if 'admin' in request.session and id:
        poll = Polls.objects.get(id=id)
        poll.date_end = datetime.datetime.now()
        poll.save()
        return HttpResponse('true')
    else:
        return redirect('auth:auth')
