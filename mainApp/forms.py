from django.forms import ModelForm
from .models import Shelter, Image, Pet
from django import forms

# Create the form class.
class ShelterForm(ModelForm):
    class Meta:
        model = Shelter
        fields = ['name', 'about', 'location', 'image']
        labels = {
            'name': "",
            'about': "",
            'location': "",
            'image': ""
        }    
        help_texts = {'about': ""}
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control mb-4', 
                                            'placeholder': 'The name of your shelter.'}),
            'about': forms.Textarea(attrs={'class':'form-control mb-4', 
                                            'placeholder': 'Tell us something about your shelter.',
                                            'rows':"5"
                                            }),
            'location': forms.TextInput(attrs={ 'class':'form-control mb-4', 
                                            'placeholder': 'Where is your shelter?'}
                    ),
            #'image': forms.ImageField()
            }