from django import forms
from django.conf import settings


class SearchForm(forms.Form):
    authors = forms.CharField(label="Autorzy")
    date1 = forms.DateField(label="Data 1", input_formats=settings.DATE_INPUT_FORMATS)
    date2 = forms.DateField(label="Data 2", input_formats=settings.DATE_INPUT_FORMATS)
