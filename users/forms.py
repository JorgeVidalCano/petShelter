from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django import forms


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control', "placeholder":"Username",}), label="Username")
    email = forms.EmailField(widget=forms.EmailInput(attrs = {'class':'form-control', "placeholder":"Email",}), label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'form-control',"placeholder": "Password", }), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'form-control',"placeholder": "Repeat password",}), label="Repeat password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']