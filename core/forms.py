# myapp/forms.py

from django import forms
from .models import InputData

class InputDataForm(forms.ModelForm):
    class Meta:
        model = InputData
        fields = ['nation', 'number']
