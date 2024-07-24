from django.db import models
from django.contrib.auth.models import User
from .utils import *
from accounts.models import *

# Create your models here.

class Review(models.Model):
    reviewer_name = models.CharField(max_length=255)
    reviewer_email = models.EmailField()
    reviewer_ip = models.GenericIPAddressField()
    rating = models.IntegerField()
    comment = models.TextField()
    reviewed_professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_professional_average_rating()
        if self.reviewed_professional.num_of_reviews is None: self.reviewed_professional.num_of_reviews = 1
        else: self.reviewed_professional.num_of_reviews += 1
        self.reviewed_professional.save(update_fields=['num_of_reviews'])

    def update_professional_average_rating(self):
        professional = self.reviewed_professional
        if professional:
            average_rating = professional.review_set.aggregate(avg_rating=Avg('rating'))['avg_rating']
            professional.average_rating = round(average_rating, 1) if average_rating else None
            professional.save(update_fields=['average_rating'])

    def __str__(self):
        return f"{self.reviewed_professional}: {self.reviewer_email}"
    
