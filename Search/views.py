from django.shortcuts import render
from .models import Publication
from django.http import HttpResponse
import json
from .parser import search

from .forms import SearchForm

# Create your views here.

def search_results(request):
    print("REQ BODY")

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #publikacje = search('Dybiec, Bartłomiej [SAP11018789]', '2018, 2019')
            dates = str(form.cleaned_data['date1'].year)+', '+str(form.cleaned_data['date2'].year)
            print(dates)
            publikacje = search(form.cleaned_data['authors'], dates)
            result = {'publikacje': publikacje,}
            return render(request, 'search_results.html', result)


def search_index(request):
    form = SearchForm()
    return render(request, 'search.html', {'form': form})
