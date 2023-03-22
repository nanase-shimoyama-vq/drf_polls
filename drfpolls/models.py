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
    votes = models.IntegerField()
    question_id = models.IntegerField()
    
    def __str__(self):
        return self.choice_text

class Comment(models.Model):
    comment_text = models.TextField(max_length=300)
    comment_date = models.DateTimeField('date published')

    def __str__(self):
        return self.comment_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now