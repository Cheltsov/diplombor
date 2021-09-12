from django.http import HttpResponse
from django.shortcuts import render, redirect

from adminer.core.data import *
from adminer.core.query import *
from adminer.models import *


def polls(request):
    if 'admin' in request.session:
        content = {
            "polls": Polls.objects.all()
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
            "categories": createJsonCategory(Category.objects.all())
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
        }

        content["categories_json"] = json.dumps(content['categories'])
        return render(request, 'adminer/polls/polls_edit.html', content)
    else:
        return redirect('auth:auth')


def polls_delete(request, id):
    if 'admin' in request.session and id:
        Polls.objects.get(id=id).delete()
        return redirect('adminer:polls')
    else:
        return redirect('auth:auth')
