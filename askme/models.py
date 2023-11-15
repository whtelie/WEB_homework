from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.TextField(
        default='https://static.wikia.nocookie.net/jfjfjfjfjfjfjffjjffjjfjfjfj/images/3/33/12.png.png/revision/latest?cb=20230903081729&path-prefix=ru',
        max_length=500
    )

    def __str__(self):
        return self.user.username
