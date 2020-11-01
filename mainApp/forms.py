from django.forms import ModelForm
from .models import Shelter, Image, Pet, Feature
from django import forms

# Create the form class.
class ShelterForm(forms.ModelForm):
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

class PetForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = ['name', 'about', 'sex', 'kind', 'weight', 'age', 'status', 'color']
        SEX = (
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Unknown', 'Unknown')
        )
        STATE = (
            ("Adoption", "Adoption"),
            ("Adopted", "Adopted"),
            ("Urgent", "Urgent")
        )
        TYPE = [
            ("Cat", "Cat"),
            ("Dog", "Dog"),
            ("Guinea pig", "Guinea pig"),
            ("Rabbit", "Rabbit"),
            ("Other", "Other")
        ]
        COLOR = [
            ("#fbfbfa", "White"),
            ("000", "Black"),
            ("#800000", "Brown"),
            ("#808080", "Gray"),
        ]
    
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control mb-4', 
                                            'placeholder': 'Pet\'s name.'}),
            'about': forms.Textarea(attrs={'class':'form-control mb-4', 
                                            'placeholder': 'Tell us something the pet.',
                                            'rows':"5"}),
            'age': forms.TextInput(attrs={'type':'number',
                                          'class':'form-control mb-4'}),
            'weight': forms.TextInput(attrs={'type':'number',
                                            'class':'form-control mb-4'}),
            'sex': forms.Select(choices=TYPE, attrs={'class':'form-control mb-4'}),
            'kind': forms.Select(choices=TYPE, attrs={'class':'form-control mb-4'}),
            'status': forms.Select(choices=TYPE, attrs={'class':'form-control mb-4'}),
            'color': forms.Select(choices=TYPE, attrs={'class':'form-control mb-4'}),
            #'features': forms.ModelMultipleChoiceField(queryset=Feature)
            #'features': forms.CheckboxSelectMultiple(attrs = {'class':'checkbox-tag'}, queryset=Feature.objects.all, label="", required=False)
            'features': forms.ModelChoiceField(queryset=Feature.objects.all(), label="", required=False)
        }
        i still need to add the features and the imgs
        