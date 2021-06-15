from django import forms
from django.conf import settings


DISPLAY_VIEW= [
    (1, 'Wyniki pracowników'),
    (2, 'Wyniki pracowników z rozdzieleniem na najlepsze publikacje'),
    (3, 'Wyniki pracowników wraz z informacjami o publikacjach'),
    ]

class SearchForm(forms.Form):
    authors = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'input-field', 'id': 'addNew', 'hidden':'true'}))
    date1 = forms.DateField(label="Od", widget=forms.DateTimeInput(attrs={'class': 'date-field'}), input_formats=settings.DATE_INPUT_FORMATS)
    date2 = forms.DateField(label="Do", widget=forms.DateTimeInput(attrs={'class': 'date-field'}), input_formats=settings.DATE_INPUT_FORMATS)
    slots = forms.IntegerField(label="Liczba slotów", widget=forms.TextInput(attrs={'class': 'input-field', 'id': 'slots', 'value':2}))
    display_type = forms.CharField(label='Typ wyświetlenia', widget=forms.Select(choices=DISPLAY_VIEW, attrs={'class': 'choose-input'}))