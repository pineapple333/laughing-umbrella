from django.shortcuts import render
from .models import Publication
from .models import Author
from django.http import HttpResponse
import json
from .parser import search, parse_publication
import math
import time

from .forms import SearchForm

# Create your views here.
max_points = 0
points = 0
numery = []
max_numery = []
cost = 0.0


def rec_choose(publikacje):
    global max_points
    global points
    global numery
    global max_numery
    global cost

    for numer, publikacja in enumerate(publikacje):
        #print(publikacja.cost)
        #print(cost)
        #print("---")
        if publikacja.cost <= (2.0 - cost) and numer not in numery:
            numery.append(numer)
            points = points + publikacja.points
            cost = cost + publikacja.cost
            if max_points < points:
                max_points = points
                max_numery = numery.copy()
            rec_choose(publikacje)
            points = points - publikacja.points
            cost = cost - publikacja.cost
            numery.pop()
        cost=round(cost,5)
    max_points = round(max_points, 2)
    return None


def search_results(request):
    global max_numery
    global max_points
    global points
    global numery
    global cost

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)


        authors = []
        sumOfPoints = 0
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # publikacje = search('Dybiec, Bartłomiej [SAP11018789]', '2018, 2019')
            dates = str(form.cleaned_data['date1'].year) + ', ' + str(form.cleaned_data['date2'].year)
            namesOfAuthors = form.cleaned_data['authors']
            names = namesOfAuthors.split(';')

            #print(names)

            for name in names:
                author = Author()
                max_points = 0
                points = 0
                numery = []
                max_numery = []
                cost = 0.0
                author.name_surname = name
                try:
                    publikacje = search(name, dates)
                except TimeoutError as error:
                    error_page(request, error)
                except:
                    print("UNHANDLED EXCEPTION")

                author.publications = publikacje
                k = 1
                if publikacje[0] is None:
                    publikacje.pop(0)
                for publikacja in publikacje:
                    if len(publikacja.authors) == 0:
                        publikacja.authors.append("PLACEHOLDER")
                    if publikacja.points == 0:
                        publikacja.points = 5
                    if publikacja.points >= 100:
                        punkty = publikacja.points
                    if publikacja.points <= 20:
                        punkty = (k / len(publikacja.authors)) * publikacja.points
                    if publikacja.points < 100 and publikacja.points > 20:
                        punkty = math.sqrt((k / len(publikacja.authors))) * publikacja.points
                    if punkty < publikacja.points / 10:
                        punkty = publikacja.points / 10

                    #Get publication authors from same department
                    # co_department_authors = parse_publication(publikacja.id)

                    k = len(publikacja.affiliated_authors)
                    koszt = (1 / k) * (punkty / publikacja.points)
                    publikacja.points = punkty / k
                    publikacja.cost = koszt
                    publikacja.m = len(publikacja.authors)
                print(f"The total number of publications: {len(publikacje)}")
                start = time.time()
                rec_choose(publikacje)
                end = time.time()
                print(f"Recursive operation took: Seconds: {end - start}. Minutes: {(end - start)/60}")
                best_publications = []
                for numer in max_numery:
                    best_publications.append(publikacje[numer])

                for publikacja in publikacje:
                    publikacja.points = round(publikacja.points, 2)
                    publikacja.cost = round(publikacja.cost, 2)

                sumOfPoints += max_points

                author.max_points = max_points
                author.best_publications = best_publications
                authors.append(author)

                publikacje = best_publications

        result = {'authors' : authors, 'sumOfPoints' : sumOfPoints}
        return render(request, 'search_results.html', result)


def error_page(request, error):
    return render(request, 'search_error_page.html', {'error': error})

def search_index(request):
    form = SearchForm()
    return render(request, 'search.html', {'form': form})
