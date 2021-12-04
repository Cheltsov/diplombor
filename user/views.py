from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render

from adminer.core.data import createJsonPolls, getPostJson, createJsonQuestion
from adminer.models import Polls, UserAnswer, Question, Answer, UserAnswerOther

from adminer.math.expert_competence_analysis import mainer


# from adminer.math.count_experts import mainer


def index(request, id):
    if Polls.objects.filter(id=id, date_start__isnull=False, date_end__isnull=True).exists():
        poll = Polls.objects.get(id=id)

        list_category_id = []
        categories = poll.categorypolls_set.all()
        for item_category in categories:
            list_category_id.append(item_category.id_category_id)

        list_question = createJsonQuestion(Question.objects.filter(id_category_id__in=list_category_id))

        content = {
            'poll': createJsonPolls([poll])[0],
            'categories_question': list_question
        }
        return render(request, 'user/base.html', content)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def create_user_answer(request, id):
    if request.method == 'POST':
        response = 'false'
        request_user_answer = getPostJson(request, 'getdata')
        list_user_answer = []
        for item in request_user_answer:
            answer = Answer.objects.get(id=item['id_answer'])
            list_user_answer.append(UserAnswer(id_polls_id=id,
                                               id_question_id=item['id_question'],
                                               id_answer_id=item['id_answer'],
                                               user=item['user'],
                                               is_category=item['is_category'],
                                               id_category_id=item['id_category'],
                                               answer_cost=answer.cost / 100))
        if UserAnswer.objects.bulk_create(list_user_answer):
            response = 'true'

        request_user_answer_other = getPostJson(request, 'data_other')
        list_user_answer_other = []
        for item in request_user_answer_other:
            list_user_answer_other.append(UserAnswerOther(id_question_id=item['id_question'],
                                                          user=item['user'],
                                                          other_text=item['other_text']))
        UserAnswerOther.objects.bulk_create(list_user_answer_other)

        return HttpResponse(response)
    return HttpResponseNotFound('<h1>Page not found</h1>')


def thank(request):
    return render(request, 'user/thank.html', {})


def main(request):
    mainer()
    return HttpResponse('true')
