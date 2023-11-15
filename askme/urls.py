

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('ask', ask, name='ask'),
    path('question/<int:question_id>', question, name='question'),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('tag/<str:tag>', tag_list, name='tag_list'),
]
