import json
from bs4 import BeautifulSoup
import requests
import re
from .models import Publication


def search(names, dates):

    # link = 'https://ruj.uj.edu.pl/xmlui/discover?filtertype_1=author&filter_relational_operator_1=equals&filter_1=Cieśla,+Michał+%5BSAP11018214%5D&filtertype_2=dateIssued&filter_relational_operator_2=equals&filter_2=2019&view=mod1&'
    # correct
    # link = 'https://ruj.uj.edu.pl/xmlui/discover?view=mod3&query=&scope=%2F&filtertype_1=author&filter_relational_operator_1=equals&filter_1=Dybiec%2C+Bart%C5%82omiej+%5BSAP11018789%5D&filtertype_2=dateIssued&filter_relational_operator_2=equals&filter_2=2019&filtertype_3=title&filter_relational_operator_3=contains&filter_3=&submit_apply_filter=Apply'.replace('+', ' ')
    # link='https://ruj.uj.edu.pl/xmlui/discover?view=mod2&query=&scope=%2F&filtertype_1=author&filter_relational_operator_1=equals&filter_1=Barbasz%2C+Jakub+%5BSAP11019396%5D&filtertype_2=dateIssued&filter_relational_operator_2=equals&filter_2=2019&filtertype_4=title&filter_relational_operator_4=contains&filter_4=&submit_apply_filter=Apply&query=&scope=%2F'
    # name = 'Dybiec, Bartłomiej [SAP11018789]'
    # date = '2018, 2019'
    name = names
    date = dates
    link = f'https://ruj.uj.edu.pl/xmlui/discover?view=mod3&query=&scope=/&filtertype_1=author&filter_relational_operator_1=equals&filter_1={name}&filtertype_2=dateIssued&filter_relational_operator_2=contains&filter_2={date}&filtertype_4=title&filter_relational_operator_4=contains&filter_4=&submit_apply_filter=Apply&query=&scope=/'

    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')

    # find all script tags from the source page where there's a 'fields part'
    fields = filter(lambda x: True if 'fields' in x.string else False,
                        soup.find_all('script', type='text/javascript', src=None)
                )

    # there should be only one result so take the first one from the list
    data = list(fields)[0]

    # take all element that are between curly brackets
    elements = re.findall(r"\{(.*?)\}", str(data))

    publications = []
    publication = None

    for element in elements:
        left, right = element.split(':', 1)
        # print(f'Left: {left}, right: {right}')
        # print(len(element.split(':')))
        if left.strip('"') == "dc.id":
            publications.append(publication)
            publication = Publication()
        if left.strip('"') == "dc.contributor.author":
            publication.authors.append(re.sub('[\"\s+]', '', right))
        if left.strip('"') == "dc.title":
            publication.title = right.strip('"')
        if left.strip('"') == "dc.pointsMNiSW":
            publication.points = int(right.strip('"').split(':')[1].strip(' '))
    publications.append(publication)

    print(publications)

    #print(f"Decoded URL: {requests.utils.unquote('https://ruj.uj.edu.pl/xmlui/discover?view=mod3&query=&scope=%2F&filtertype_1=author&filter_relational_operator_1=equals&filter_1=Dybiec%2C+Bart%C5%82omiej+%5BSAP11018789%5D&filtertype_2=dateIssued&filter_relational_operator_2=contains&filter_2=2018%2C+2019&filtertype_4=title&filter_relational_operator_4=contains&filter_4=&submit_apply_filter=Apply&query=&scope=%2F')}")

    return publications
