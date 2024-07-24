from django.db import models
from core.models import *
from accounts.models import *

class Province(models.Model):
    province = models.CharField(max_length=255)

    def __str__(self):
        return self.province

class ForumQuestion(models.Model):
    asker_email = models.EmailField()
    forum_question_title = models.CharField(max_length=300)
    forum_question = models.TextField()
    view_count = models.IntegerField()
    topics = models.ManyToManyField(Specialties)
    location = models.ForeignKey(Province, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_status = models.BooleanField()

    def __str__(self):
        return self.forum_question_title

class ForumAnswers(models.Model):
    forum_question = models.ForeignKey(ForumQuestion, on_delete=models.CASCADE)
    professional_answered = models.ForeignKey(Professional, on_delete=models.CASCADE)
    response = models.TextField()
    

    def __str__(self):
        return f"{self.professional_answered} - {self.forum_question}"




    