import datetime
import json
import math
import os

import pdfkit

import numpy as np
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder

from adminer.core.data import *
from adminer.core.query import *
from adminer.math.modules.CompetenceExpert import CompetenceExpert
from adminer.math.modules.ConsistencyEstimates import ConsistencyEstimates
from adminer.math.modules.CountExpert import CountExpert
from adminer.models import *
from datetime import datetime
import time

def polls(request):
    if 'admin' in request.session:
        content = {
            "polls": Polls.objects.filter(date_start__isnull=True, date_end__isnull=True).order_by('-date_updated'),
            "polls_start": Polls.objects.filter(date_start__isnull=False, date_end__isnull=True).order_by(
                '-date_updated'),
            "polls_end": Polls.objects.filter(date_start__isnull=False, date_end__isnull=False).order_by(
                '-date_updated'),
        }
        return render(request, 'adminer/polls/polls.html', content)
    else:
        return redirect('auth:auth')


def polls_create(request):
    if 'admin' in request.session and id:
        if request.method == 'POST':
            response = 'false'
            request_polls = getPostJson(request, 'getdata')
            lastPoll = Polls.objects.latest('id').id + 1
            obj_polls = Polls.objects.create(id=lastPoll, title=request.POST['polls_title'], description=request.POST['polls_desc'])
            obj_polls.save()
            if createQuestionAnswerByPolls(request_polls, obj_polls.id) and \
                    addCategoryInPolls(getPostJson(request, 'polls_category'), obj_polls.id):
                response = 'true'
            return HttpResponse(response)
        content = {
            "categories": createJsonCategory(Category.objects.all().order_by('-date_created')),
            "patterns": createJsonPattern(Pattern.objects.all().order_by('-date_created')),
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
            "category_polls": createJsonCategory(Category.objects.filter(
                id__in=obj_polls.categorypolls_set.all().values_list('id_category_id', flat=True))),
            "questions": createJsonQuestion(questions),
            "categories": createJsonCategory(Category.objects.all().order_by('-date_created')),
            "patterns": createJsonPattern(Pattern.objects.all().order_by('-date_created')),
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
                'count_user': poll.getCountUserAnswer(),
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
        poll.date_start = datetime.now()
        poll.save()
        return HttpResponse('true')
    else:
        return redirect('auth:auth')


def polls_end(request, id):
    if 'admin' in request.session and id:
        poll = Polls.objects.get(id=id)
        poll.date_end = datetime.now()
        poll.save()
        return HttpResponse('true')
    else:
        return redirect('auth:auth')


def polls_stat(request, id):
    poll = Polls.objects.get(id=id)
    list_category = getCategoryInPoll(id_poll=id)
    content = {
        "poll": poll,
        "count_user": poll.getCountUserAnswer(),
        "list_category": list_category,
        'id_category': int(request.GET['id_category']) if request.GET else None
    }
    return render(request, 'adminer/polls/polls_statistic.html', content)


def stat_ajax(request, id):
    listCategory = json.loads(request.POST['id_category'])
    id_category = listCategory if len(listCategory) > 0 else None

    strCategory = ''
    for item in id_category:
        strCategory = strCategory + str(item) + '_' if item != 0 else ''

    my_file = 'staticfiles/adminer/report/' + str(id) + '_' + strCategory + 'data.json'

    if not os.path.exists(my_file):
        return HttpResponse('false')

    with open(my_file) as f:
        content = json.load(f)

    return JsonResponse(content, safe=False)


def create_pdf(request, id):
    scheme = request.is_secure() and "https" or "http"
    url_site = f'{scheme}://{request.get_host()}/'

    if int(request.POST['id_category']) > 0:
        id_category = request.POST['id_category']
        url = 'staticfiles/adminer/pdf/out_' + str(id) + '_category_' + str(id_category) + '.pdf'
        pdfkit.from_url(str(url_site) + 'admin/polls/statistic/' + str(id) + '/?id_category=' + str(id_category), url)
    else:
        url = 'staticfiles/adminer/pdf/out_' + str(id) + '.pdf'
        pdfkit.from_url(str(url_site) + 'admin/polls/statistic/' + str(id) + '/', url)
    return JsonResponse('/' + url, safe=False)


def refresh_stat_ajax(request, id):
    if getStatAllCategory(id):
        return HttpResponse('true')
    else:
        return HttpResponse('false')


def split_list(a_list):
    half = math.ceil(len(a_list)/2)
    return a_list[:half], a_list[half:]


def getStatAllCategory(id_poll):
    start_time = datetime.now()
    listCategoryByQuestion = getCategoryInPoll(id_poll=id_poll)
    if len(listCategoryByQuestion) == 0:
        return False
    listCategory = listCategoryByQuestion[0] + listCategoryByQuestion[1]

    getStat(id_poll)
    print(datetime.now() - start_time)

    for item in listCategory:
        getStat(id_poll, [item.id])
        print(datetime.now() - start_time)

    newList1, newList2 = split_list(listCategory)
    for item1 in newList1:
        for item2 in newList2:
            getStat(id_poll, [item1.id, item2.id])
            print(datetime.now() - start_time)
    return True


def getStat(id_poll, arr_id_category=None):
    obj_competence_expert = CompetenceExpert(id_poll=id_poll, id_category=arr_id_category)

    if not obj_competence_expert.questions:
        return False

    list_s1, list_s6 = obj_competence_expert.main()

    rank = obj_competence_expert.rank_q
    count_expert = CountExpert(id_poll=id_poll, id_category=arr_id_category)

    min_count_expert = count_expert.getMinCountExpert()

    obj_ser = ConsistencyEstimates(id_poll=id_poll, id_category=arr_id_category)

    list_q_mark = []
    for i, item in enumerate(obj_competence_expert.questions):
        sch = round(obj_competence_expert.getMark(min_count_expert)[i], 2)

        list_other_answer = UserAnswerOther.objects.filter(id_question_id=item['id_question_id']).values_list(
            'other_text')

        list_q_mark.append({
            'question_title': Question.objects.get(id=item['id_question_id']).title,
            's1': round(list_s1[i], 2),
            's6': round(list_s6[i], 2),
            'sch': sch if sch > 0 else 0,
            'other_answer': json.dumps(list(list_other_answer), cls=DjangoJSONEncoder)
        })

    word = coord = "Недостаточно экспертов"
    if min_count_expert != 0:
        word = obj_ser.math4(min_count_expert)
        coord = obj_ser.math5(min_count_expert)
    content = {
        "list_q_mark": list_q_mark,
        "word": word,
        "coord": coord,
        "count_mark": obj_competence_expert.getMatrWord()
    }

    nameCategory = ''
    if arr_id_category:
        for itemC in arr_id_category:
            nameCategory = nameCategory + str(itemC) + '_'

    print(str(id_poll) + '_' + nameCategory)
    with open('staticfiles/adminer/report/' + str(id_poll) + '_' + nameCategory + 'data.json', 'w',
              encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

    return content
