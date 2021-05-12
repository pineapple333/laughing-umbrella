from django.shortcuts import render
from .models import Publication
from django.http import HttpResponse
import json
from .parser import search
import math

from .forms import SearchForm
# Create your views here.
max_points=0
points=0
numery=[]
max_numery=[]
cost=0.0

def rec_choose(publikacje):
	global max_points
	global points
	global numery
	global max_numery
	global cost
	for numer, publikacja in enumerate(publikacje):
		if publikacja.cost<=(2.0-cost) and numer not in numery :
			numery.append(numer)
			points=points+publikacja.points
			cost=cost+publikacja.cost
			if(max_points<points):
				max_points=points
				max_numery=numery.copy()
			rec_choose(publikacje)
			points=points-publikacja.points
			cost=cost-publikacja.cost
			numery.pop()
	return None
			
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
			global max_numery
			global max_points
			publikacje = search(form.cleaned_data['authors'], dates)
			k=1
			if publikacje[0]==None:
				publikacje.pop(0)
			for publikacja in publikacje:
				if len(publikacja.authors)==0:
					publikacja.authors.append("PLACEHOLDER")
				if publikacja.points==0:
					publikacja.points=5
				if(publikacja.points>=100):
					punkty=publikacja.points
				if(publikacja.points<=20):
					punkty=(k/len(publikacja.authors))*publikacja.points
				if(publikacja.points<100) and (publikacja.points>20):
					punkty=math.sqrt((k/len(publikacja.authors)))*publikacja.points
				if punkty<publikacja.points/10:
					punkty=publikacja.points/10
				koszt=(1/k)*(punkty/publikacja.points)
				publikacja.points=punkty/k
				publikacja.cost=koszt
				publikacja.m=len(publikacja.authors)
			rec_choose(publikacje)
			publikacjetmp=[]
			for numer in max_numery:
				publikacjetmp.append(publikacje[numer])
			publikacje=publikacjetmp.copy()
			
		result = {'publikacje': publikacje,}
		return render(request, 'search_results.html', result)


def search_index(request):
	form = SearchForm()
	return render(request, 'search.html', {'form': form})
