from django.contrib import admin
from . import models

admin.site.register(models.ForumQuestion)
admin.site.register(models.ForumAnswers)
admin.site.register(models.Province)
