import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from adminer.core.data import *
from adminer.core.query import *
from adminer.models import *


def home(request):
    if 'admin' in request.session:
        content = {
            "client": 1
        }
        return render(request, 'adminer/index.html', content)
    else:
        return redirect('auth:auth')


def exit(request):
    if 'admin' in request.session:
        del request.session['admin']
        return redirect('auth:auth')
    else:
        return redirect('auth:auth')


def pattern(request):
    if 'admin' in request.session:
        content = {
            "patterns": Pattern.objects.all()
        }
        return render(request, 'adminer/pattern.html', content)
    else:
        return redirect('auth:auth')


def pattern_create(request):
    if 'admin' in request.session and id:
        if request.method == 'POST':
            response = 'false'
            request_pattern = getPostJson(request, 'getdata')
            obj_pattern = Pattern.objects.create(title=request.POST['pattern_title'])
            obj_pattern.save()
            if createQuestionAnswerByPattern(request_pattern, obj_pattern.id):
                response = 'true'
            return HttpResponse(response)
        return render(request, 'adminer/pattern_create.html', {})
    else:
        return redirect('auth:auth')


def pattern_edit(request, id):
    if 'admin' in request.session and id:
        obj_pattern = Pattern.objects.get(id=id)
        questions = obj_pattern.question_set.all()

        if request.method == 'POST':
            response = 'false'
            request_pattern = getPostJson(request, 'getdata')
            obj_pattern.title = request.POST['pattern_title']
            obj_pattern.save()
            if deleteQuestionAnswerByPattern(obj_pattern) and createQuestionAnswerByPattern(request_pattern, id):
                response = 'true'
            return HttpResponse(response)

        content = {
            "pattern": obj_pattern,
            "questions": createJsonQuestion(questions)
        }
        return render(request, 'adminer/pattern_edit.html', content)
    else:
        return redirect('auth:auth')


def pattern_delete(request, id):
    if 'admin' in request.session and id:
        Pattern.objects.get(id=id).delete()
        return redirect('adminer:pattern')
    else:
        return redirect('auth:auth')
