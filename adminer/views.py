import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from adminer.models import *
from django.core import serializers


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


def pattern_edit(request, id):
    if 'admin' in request.session and id:

        if request.method == 'POST':
            request_body = request.POST.get('getdata', None)
            request_pattern = json.loads(request_body)
            list_answer = []
            for question in request_pattern:
                ques = Question(title=question['title'], id_pattern_id=id)
                ques.save()
                for answer in question:
                    list_answer.append(Answer(title=answer, id_question_id=ques.id))

            Answer.objects.bulk_create(list_answer)
            return True

        ques_json = []
        pattern = Pattern.objects.get(id=id)
        questions = pattern.question_set.all()
        for question in questions:
            ques_json.append({
                "id": question.id,
                "title": question.title,
                "answers": question.answer_set.all()
            })
        content = {
            "pattern": pattern,
            "questions": ques_json
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
