from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.db.models import Sum

from app.forms import LoginForm, RegisterForm
from app.models import Question


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        raise Http404("Page not found")
    return page_obj


@login_required(login_url='login/', redirect_field_name='continue')
def index(request):
    # questions = Question.objects.all()
    questions = Question.objects.annotate(totaly_votes=Sum('vote__value'))

    context = {
        'page_obj': paginate(questions, request),
        # 'question_votes': {question.id: Question.objects.count_total_votes(question.id) for question in questions},
    }
    return render(request, 'index.html', context)


@csrf_protect
def log_in(request):
    print(request.GET)
    print(request.POST)
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            print(user)
            if user is not None:
                login(request, user)
                print('Successfully logged in')
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, 'Wrong password or user does not exist')
    return render(request, 'login.html', context={'form': login_form})


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@login_required(login_url='login/', redirect_field_name='continue')
def ask(request):
    return render(request, 'ask.html')


@csrf_protect
def signup(request):
    print(request.GET)
    print(request.POST)
    if request.method == 'GET':
        register_form = RegisterForm()
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            print(user)
            if user is not None:
                # login(request, user)
                print('Successfully signed up')
                return redirect(reverse('index'))
            else:
                register_form.add_error(None, 'Registration error')
    return render(request, 'signup.html', context={'form': register_form})


@login_required(login_url='login/', redirect_field_name='continue')
def settings(request):
    return render(request, 'settings.html')


@login_required(login_url='login/', redirect_field_name='continue')
def hot(request):
    # questions = Question.objects.all()
    questions = Question.objects.get_hot_questions().annotate(totaly_votes=Sum('vote__value'))

    context = {
        'page_obj': paginate(questions, request),
    }
    return render(request, 'hot.html', context)


@login_required(login_url='login/', redirect_field_name='continue')
def top(request):
    questions = Question.objects.get_top_questions().annotate(totaly_votes=Sum('vote__value'))

    context = {
        'page_obj': paginate(questions, request, 10),
    }
    return render(request, 'top.html', context)


@login_required(login_url='login/', redirect_field_name='continue')
def tag(request, tag_name):
    questions = Question.objects.tagged(tag_name).annotate(totaly_votes=Sum('vote__value'))
    context = {
        'tag': tag_name,
        'page_obj': paginate(questions, request),
    }
    return render(request, 'tag.html', context)


@login_required(login_url='login/', redirect_field_name='continue')
def question(request, question_id):
    if question_id > len(Question.objects.all()):
        raise Http404("Question does not exist")
    my_question = Question.objects.filter(pk=question_id).annotate(totaly_votes=Sum('vote__value')).first()
    context = {
        'question': my_question,
        'page_obj': paginate(my_question.answers.all(), request),
    }
    return render(request, 'question.html', context)
