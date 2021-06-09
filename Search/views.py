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
slots = 2.0


def knapSack(W, wt, val, n):
    wynik=[]
    K = [[0 for w in range(W + 1)]
            for i in range(n + 1)]
             
    # Build table K[][] in bottom
    # up manner
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i - 1].cost <= w:
                K[i][w] = max(val[i - 1]
                  + K[i - 1][w - wt[i - 1].cost],
                               K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]
 
    # stores the result of Knapsack
    res = K[n][W]
     
    w = W
    for i in range(n, 0, -1):
        if res <= 0:
            break
        # either the result comes from the
        # top (K[i-1][w]) or from (val[i-1]
        # + K[i-1] [w-wt[i-1]]) as in Knapsack
        # table. If it comes from the latter
        # one/ it means the item is included.
        if res == K[i - 1][w]:
            continue
        else:
 
            # This item is included.
            wynik.append(wt[i-1])
             
            # Since this weight is included
            # its value is deducted
            res = res - val[i - 1]
            w = w - wt[i - 1].cost
    return wynik


def search_results(request):
    global max_numery
    global max_points
    global points
    global numery
    global cost
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
                points = 0
                numery = []
                max_numery = []
                cost = 0.0
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
                W=int(2.0*1000)
                n=len(publikacje)
                val=[]
                wt=[]
                for publikacja in publikacje:
                    val.append(int(publikacja.points*1000))
                    publikacja.cost=int(publikacja.cost*1000)
                    wt.append(publikacja)
                best_publications=knapSack(W, wt, val, n)
                end = time.time()
                print(f"Recursive operation took: Seconds: {end - start}. Minutes: {(end - start)/60}")
                for publikacja in best_publications:
                    publikacja.cost=publikacja.cost/1000
                    max_points=max_points+publikacja.points
                max_points=round(max_points,2)
                for publikacja in publikacje:
                    publikacja.points = round(publikacja.points, 2)
                    publikacja.cost = round(publikacja.cost, 2)

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