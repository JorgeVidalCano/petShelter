
from .models import Message
from django.forms import ModelForm
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': "Message"}
                
        widgets = {
            'message': forms.Textarea(attrs={'class':'form-control mb-4', 
                                            'placeholder': 'Get in touch with this animal',
                                            'rows':"5"
                                            })}