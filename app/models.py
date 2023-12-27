from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=255)

class QuestionManager(models.Manager):
    def get_best_questions(self):
        return self.annotate(like_count=Count('likes')).order_by('-like_count')

    def get_new_questions(self):
        return self.order_by('-created_at')

    def get_questions_by_tag(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-created_at')

class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField('Like', related_name='liked_questions', blank=True)

    objects = QuestionManager()

class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField('Like', related_name='liked_answers', blank=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} likes {self.question or self.answer}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
