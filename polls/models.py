import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # 以下は管理ユーザーのユーザーIDを紐付ける
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # 画像のパスを登録する
    image_url = models.ImageField(upload_to='polls')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text




