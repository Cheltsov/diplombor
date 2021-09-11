from django.http import HttpResponse
from django.shortcuts import render, redirect

from adminer.core.data import *
from adminer.core.query import *
from adminer.models import *


def category(request):
    if 'admin' in request.session:
        content = {
            "categories": Category.objects.all()
        }
        return render(request, 'adminer/category/category.html', content)
    else:
        return redirect('auth:auth')


def category_create(request):
    if 'admin' in request.session and id:
        if request.method == 'POST':
            response = 'false'
            request_category = getPostJson(request, 'getdata')
            obj_category = Category.objects.create(title=request.POST['category_title'])
            obj_category.save()
            if createQuestionAnswerByCategory(request_category, obj_category.id):
                response = 'true'
            return HttpResponse(response)
        return render(request, 'adminer/category/category_create.html', {})
    else:
        return redirect('auth:auth')


def category_edit(request, id):
    if 'admin' in request.session and id:
        obj_category = Category.objects.get(id=id)
        questions = obj_category.question_set.all()

        if request.method == 'POST':
            response = 'false'
            request_category = getPostJson(request, 'getdata')
            obj_category.title = request.POST['category_title']
            obj_category.save()
            if deleteQuestionAnswerByCategory(obj_category) and createQuestionAnswerByCategory(request_category, id):
                response = 'true'
            return HttpResponse(response)

        content = {
            "category": obj_category,
            "questions": createJsonQuestion(questions)
        }
        return render(request, 'adminer/category/category_edit.html', content)
    else:
        return redirect('auth:auth')


def category_delete(request, id):
    if 'admin' in request.session and id:
        Category.objects.get(id=id).delete()
        return redirect('adminer:category')
    else:
        return redirect('auth:auth')
