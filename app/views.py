from django.shortcuts import render
from django.core.paginator import Paginator

QUESTIONS = [
        {
            'id': i,
            'title': f'Question {i}',
            'votes': f'{i}',
            'answers': f'{i}',
            'views': f'{i}',
            'description': f'vlalalala {i}'
        } for i in range(20)
    ]

ANSWERS = [
    {
        'text': f'Text {i}',
    } for i in range(40)
]


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def index(request):
    return render(request, 'index.html', {'page_obj': paginate(QUESTIONS, request)})

def question(request, question_id):
    if question_id < len(QUESTIONS):
        context = {'page_obj': paginate(ANSWERS, request), 'question': QUESTIONS[question_id]}
        return render(request, 'question.html', context)

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)
