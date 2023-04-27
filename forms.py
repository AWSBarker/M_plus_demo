from django import forms
from django.core import validators

class ImeiForm(forms.Form):
    imei = forms.CharField(required=True, max_length=16,min_length=15,
                           strip=' ', label='IMEI',
                           help_text='15 digit IMEI, type or paste'
                           )
    #                          validators =[len15])