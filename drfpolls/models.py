from django.db import models
from django.utils import timezone
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE)
    # migrationを詳しく追ってみる mypy isort black bandit
    
    def __str__(self):
        return self.choice_text

class Comment(models.Model):
    comment_text = models.TextField(max_length=300, null=False,)
    comment_date = models.DateTimeField('date published')
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now