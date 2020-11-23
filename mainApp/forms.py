from django.core.exceptions import ValidationError
from .models import Shelter, Images, Pet, Feature
from django.forms import ModelForm
from django import forms

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
            'image': forms.FileInput(attrs={'class':'form-control-file'})
            }

class PetForm(forms.ModelForm):
    
    class Meta:
        model = Pet
        fields = ['name', 'about', 'sex', 'kind', 'weight', 'age', 'status', 'color', 'features']
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
            'sex': forms.Select(choices=SEX, attrs={'class':'form-control mb-4'}),
            'kind': forms.Select(choices=TYPE, attrs={'class':'form-control mb-4'}),
            'status': forms.Select(choices=STATE, attrs={'class':'form-control mb-4'}),
            'color': forms.Select(choices=COLOR, attrs={'class':'form-control mb-4'}),
            'features':forms.CheckboxSelectMultiple(attrs={"queryset": Feature.objects.all(), 
                                                            "required":False,
                                                            "class": ""}),
        }

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get("age")
        weight = cleaned_data.get("weight")

        if age is not None:
            if age < 0:
                raise ValidationError("The age cannot be negative.")
        if weight is not None:
            if weight < 0:
                raise ValidationError("The weight cannot be negative.")


class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ["mainPic", "image"]
        
        widgets={
            'mainPic': forms.CheckboxInput(attrs={'class': 'form-check-label'}),
            'image': forms.FileInput(attrs={'class':'form-control-file'}),
        },
        labels={"mainPic": "Main image", "image": ""}
