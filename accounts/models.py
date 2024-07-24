from django.db import models
from django.contrib.auth.models import User
from .utils import *
import uuid


class Specialties(models.Model):
    specialty = models.CharField(max_length=255)

    def __str__(self):
        return self.specialty

class Languages(models.Model):
    language = models.CharField(max_length = 20)

    def __str__(self):
        return self.language
    
class Designations(models.Model):
    designation = models.CharField(max_length=10)

    def __str__(self):
        return self.designation

def generate_unique_id():
    return uuid.uuid4().hex + uuid.uuid4().hex  # 48 characters long #default=generate_unique_id, unique=True

class Professional(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=48, default=generate_unique_id, unique=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    firm_name = models.CharField(null=True, max_length=255)
    contact_number = models.CharField(null=True, max_length=20)
    school_studied_at = models.CharField(null=True, max_length=255)
    designations = models.ManyToManyField(Designations)
    experience_years = models.PositiveIntegerField(null=True) #might delete
    fee_structure = models.TextField(null=True)
    num_of_reviews = models.IntegerField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    specialties = models.ManyToManyField(Specialties)
    languages = models.ManyToManyField(Languages)
    description = models.TextField(null=True)
    location = models.CharField(null=True, max_length=255)
    location_lat = models.FloatField(null=True, blank=True)
    location_long = models.FloatField(null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True, default = '/main/default-pfp.jpg', upload_to='profile_pictures/')
    background_picture = models.ImageField(null=True, blank=True, default = '/main/default-background.png', upload_to='profile_pictures/background_photos/')
    subscription_status = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.location:
            try:
                # Call nearby_professional_locations to get latitude and longitude
                self.location_lat, self.location_long = nearby_professional_locations(self.location)
            except Exception as e:
                print(f"Error occurred while geocoding: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name + self.last_name + self.email
    
class SpecialtiesAccountant(models.Model):
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialties, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.professional.user.email} - {self.specialty}"

class SpecialtiesLawyer(models.Model):
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialties, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.professional.user.email} - {self.specialty}"


class Subscription(models.Model):
    user = models.ForeignKey(Professional, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user
# Create your models here.
