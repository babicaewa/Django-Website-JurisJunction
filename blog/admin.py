from django.contrib import admin
from . import models
admin.site.register(models.Blog)
admin.site.register(models.BlogLikes)


# Register your models here.
