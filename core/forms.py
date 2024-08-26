# myapp/forms.py

from django import forms
from .models import InputData

class InputDataForm(forms.ModelForm):
    class Meta:
        model = InputData
        fields = ['nation', 'number']
        labels = {
            'nation': 'Nazione',  # Etichetta personalizzata per il campo 'nation'
            'number': 'Numero',   # Etichetta personalizzata per il campo 'number'
        }
