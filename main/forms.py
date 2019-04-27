''' form docstring '''
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class GenerateRandomUserForm(forms.Form):
    '''doc'''
    total = forms.IntegerField(
        validators=[
            MinValueValidator(50),
            MaxValueValidator(500)
        ]
    )
    mytext = forms.CharField(max_length=50, required=False)
