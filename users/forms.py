from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django import forms

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_active']

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control mb-4',
                                            'placeholder': 'Write a username.'}),
            'first_name': forms.TextInput(attrs={'class':'form-control mb-4',
                                            'placeholder': 'First name.'}),
            'last_name': forms.TextInput(attrs={'class':'form-control mb-4',
                                            'placeholder': 'Last name.'}),                                                                                    
            'email': forms.EmailInput(attrs={'class':'form-control mb-4', 
                                            'placeholder': 'Your e-mail.',}),
            'password1': forms.PasswordInput(attrs={'class':'form-control mb-4',
                                                    'placeholder':'Password'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control mb-4',
                                                    'placeholder':'Repeat Password'}),
            'is_active': forms.CheckboxInput(attrs={'class':'form-control',
                                                    'checked': ""})
        }
        labels = {
            "Username":"Username",
            "first_name":"First name",              
            "last_name":"Last name",
            "email":"Email",
            "password1":"Password",
            "password2":"Confirm Password",
            "is_active": ""
        }