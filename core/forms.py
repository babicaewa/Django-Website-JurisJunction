from django import forms
from django.forms import ModelForm
from .models import Professional, Review

class reviewForm():
        reviewer_name = forms.CharField(max_length=50)
        rating = forms.RadioSelect
        reviewer_email = forms.EmailField()
        message = forms.TextInput()
        class Meta:
             model = Review
             fields = ['reviewer_name', 'rating', 'reviewer_email', 'message']
    
        