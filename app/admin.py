from django.contrib import admin
from .models import Tag, Profile, Like, Answer, Question

admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Answer)
admin.site.register(Question)
