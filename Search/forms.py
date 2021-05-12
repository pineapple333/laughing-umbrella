from django import forms
from django.conf import settings


class SearchForm(forms.Form):
    authors = forms.CharField(label="Autorzy", widget=forms.TextInput(attrs={'class': 'input-field', 'id': 'addNew'}))
    date1 = forms.DateField(label="Data 1", widget=forms.DateTimeInput(attrs={'class': 'date-field'}), input_formats=settings.DATE_INPUT_FORMATS)
    date2 = forms.DateField(label="Data 2", widget=forms.DateTimeInput(attrs={'class': 'date-field'}), input_formats=settings.DATE_INPUT_FORMATS)
