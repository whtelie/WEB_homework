from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta


class QuestionManager(models.Manager):
    def tagged(self, tag_name):
        return self.filter(tags__name=tag_name)

    def get_hot_questions(self):
        today = date.today()
        # first_day = date(today.year, today.month - 1, 1)
        # last_day = date(today.year, today.month, 1)
        first_day = today - timedelta(days=50)
        last_day = today

        return self.filter(created_at__range=[first_day, last_day])

    def get_top_questions(self, count=10):
        return self.order_by('-total_votes')[:count]

    # def count_total_votes(self, question_id):
    #     Vote.objects.filter(question_id=question_id).aggregate(models.Sum('value'))['value__sum'] or 0


# class AnswerManager(models.Manager):
#     def count_total_votes(self, answer_id):
#         Vote.objects.filter(answer_id=answer_id).aggregate(models.Sum('value'))['value__sum'] or 0


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # photo = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return self.user.username


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, null=True, blank=True)
    value = models.IntegerField()

    def __str__(self):
        return f"'{self.user.username}' voted on '{self.question.title}'"


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    content = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='questions')
    created_at = models.DateField(default=date.today())
    # total_votes = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateField(default=date.today())
    # total_votes = models.IntegerField(default=0)

    STATUS_CHOICES = [
        ('c', 'correct'),
        ('i', 'incorrect'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='i')

    # objects = AnswerManager()

    def __str__(self):
        return f"Answer to '{self.question.title}' from '{self.user.username}'"


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name
