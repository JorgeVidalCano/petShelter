from django.contrib.auth.models import User
from django import forms

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
                
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control mb-4', 
                                            'placeholder': 'Your name.'}),
            'email': forms.EmailInput(attrs={'class':'form-control mb-4', 
                                            'placeholder': 'Your email'
                                            })
            }
