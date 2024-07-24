from django.db import models
from accounts.models import *
from forum.models import *

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=300)
    blog_text = models.TextField()
    blog_len = models.IntegerField()
    blog_views = models.IntegerField()
    topic = models.ForeignKey(Specialties, on_delete=models.CASCADE)
    location = models.ForeignKey(Province, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    photo_path = models.ImageField(default=get_random_blog_photo)

    def __str__(self):
        return f"{self.author}- {self.blog_title}"
    
    @property
    def blog_likes_count(self):
        return self.bloglikes_set.count()
    
class BlogLikes(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()


# Create your models here.

