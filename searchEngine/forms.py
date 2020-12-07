from mainApp.models import Pet
from django import forms
    
# IT is unused
SEX = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Unknown', 'Unknown')
)
STATE = (
    ("Adoption", "Adoption"),
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
class petSearchForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = ['name', 'sex', 'kind',  'status']
      
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control mb-4', 
                                            'placeholder': 'Pet\'s name.'}),
            'sex': forms.Select(choices=SEX, attrs={'class':'form-control mb-4'}),
            'kind': forms.Select(choices=TYPE, attrs={'class':'form-control mb-4'}),
            'status': forms.Select(choices=STATE, attrs={'class':'form-control mb-4'})
        }