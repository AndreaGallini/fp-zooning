# myapp/models.py

from django.db import models
from django_countries.fields import CountryField

class InputData(models.Model):
    GROUP_CHOICES = [
        ('Group 1', 'Group 1'),
        ('Group 2', 'Group 2'),
        ('Group 3', 'Group 3'),
    ]
    
    nation = CountryField()  # Questo campo continuerà a usare CountryField
    nation_name = models.CharField(max_length=100)  # Questo campo memorizzerà il nome completo della nazione
    number = models.IntegerField()
    group = models.CharField(max_length=20, choices=GROUP_CHOICES)

    def __str__(self):
        return f"{self.nation_name} - {self.number}"
