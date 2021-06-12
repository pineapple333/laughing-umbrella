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
slots = 2.0


def rec_choose(sloty, publikacje):
    n=len(publikacje)
    wynik=[]
    K = [[0 for w in range(sloty + 1)]
            for i in range(n + 1)]
    for i in range(n + 1):
        for w in range(sloty + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif publikacje[i - 1].cost <= w:
                K[i][w] = max(publikacje[i - 1].points
                  + K[i - 1][w - publikacje[i - 1].cost],
                               K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]
 
    res = K[n][sloty]
     
    w = sloty
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == K[i - 1][w]:
            continue
        else:
            wynik.append(publikacje[i-1])
            res = res - publikacje[i - 1].points
            w = w - publikacje[i - 1].cost
    return wynik


def search_results(request):
    global slots

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

            numOfSlots = form.cleaned_data['slots']

            slots = numOfSlots

            display_type = form.cleaned_data['display_type']
            print("display type ", display_type)

            #print(names)

            for name in names:
                author = Author()
                max_points = 0
                author.name_surname = name
                publikacje = search(name, dates)
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
                    publikacja.P = round(punkty, 2)
                    publikacja.cost = koszt
                    publikacja.m = len(publikacja.authors)
                print(f"The total number of publications: {len(publikacje)}")
                start = time.time()
                slots=int(slots*1000)
                for publikacja in publikacje:
                    publikacja.points=int(publikacja.points*1000)
                    publikacja.cost=int(publikacja.cost*1000)
                best_publications=rec_choose(slots, publikacje)
                end = time.time()
                slots=slots/1000
                print(f"Recursive operation took: Seconds: {end - start}. Minutes: {(end - start)/60}")
                for publikacja in publikacje:
                    publikacja.cost=publikacja.cost/1000
                    publikacja.points=publikacja.points/1000
                    publikacja.points = round(publikacja.points, 2)
                    publikacja.cost = round(publikacja.cost, 2)
                for publikacja in best_publications:
                    max_points=max_points+publikacja.points
                max_points=round(max_points,2)

                sumOfPoints += max_points

                author.max_points = max_points
                author.best_publications = best_publications
                authors.append(author)

                publikacje = best_publications

        result = {'authors' : authors, 'sumOfPoints' : sumOfPoints}

        print("display type = ", display_type)
        if(display_type == "1"):
            return render(request, 'search_result_type_1.html', result)
        elif(display_type == "2"):
            return render(request, 'search_results.html', result)
        else:
            return render(request, 'search_result_type_3.html', result)

def search_index(request):
    form = SearchForm()
    return render(request, 'search.html', {'form': form})