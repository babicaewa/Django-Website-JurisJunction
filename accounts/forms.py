from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Professional

class SignupForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'placeholder': 'Username', 'class':'form-control', 'id':'floatingUsername', 'type':'email'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class':'form-control', 'id':'floatingPassword1'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class':'form-control', 'id':'floatingPassword2'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

PROFESSIONAL_CHOICES = (
        ("accountant", "Accountant"),
        ("lawyer", "Lawyer"),
)

class EditProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['firm_name'].required = False
        self.fields['contact_number'].required = False
        self.fields['school_studied_at'].required = False
        self.fields['experience_years'].required = False
        self.fields['fee_structure'].required = False
        self.fields['description'].required = False
        self.fields['location'].required = False

        # Add the 'form-control' class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Professional
        fields = ('profile_picture', 'email', 'first_name', 'last_name', 
                  'firm_name', 'contact_number', 'school_studied_at', 
                  'experience_years', 'fee_structure', 'description', 'location', 'background_picture')
        
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'onchange': 'getImagePreview(event)'}),
            'background_picture': forms.FileInput(attrs={'class': 'form-control', 'onchange': 'getImagePreview(event)'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'id': 'autocomplete'}),
            'fee_structure': forms.Textarea(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

        


          