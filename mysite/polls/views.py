from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import Http404,HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader

from .models import Choice,Question,User
from django.urls import reverse

# import logging

# from django.shortcuts import render
# from .models import Question
#
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)

class IndexView():
    template_name='polls/index.html'
    context_object_name='latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

def index(request):
    last_question_list=Question.objects.order_by('pub_date')[:5]
    # print(last_question_list)
    template=loader.get_template('polls/index.html')
    context={
        'latest_question_list':last_question_list,
    }
    return HttpResponse(template.render(context,request))

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        # logging.info('question=',question)
        print('question=', question)
        # print('choice_set=',question.choice_set)
        # for choice in question.choice_set.all():
        #     print(choice)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def post_info(request):

    try:
        name = request.POST['info']
    except (KeyError, Choice.DoesNotExist):
        return HttpResponse('failed')
    else:
        # new_user=User(name=name)
        new_user=User()
        new_user.name=name
        new_user.save()
    return HttpResponse('success')


