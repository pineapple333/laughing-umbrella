import json
from bs4 import BeautifulSoup
import requests
import re
from .models import Publication
from lxml import etree
import time

def classifier(element):
    checkbox = element.find_all('input')
    if checkbox:
        cb = checkbox[0]
        if 'checked' in cb.attrs.values():
            return True
        else:
            return False
    else:
        return element.text

# this function receives an ID and returns a tuple 
# structure:
#   (author_name, is_affiliated)
def parse_publication(pubId, target_person):

    clean_target_person = f"{target_person.split()[0].replace(',','')} {target_person.split()[1]}"

    # create the link 
    link = f'https://ruj.uj.edu.pl/xmlui/handle/{pubId}/pbn'
    # get raw text
    r = requests.get(link)
    # parse the text
    soup = BeautifulSoup(r.text, 'html.parser')

    # print(link)

    # initialize the dictionary
    person_status = []

    person_department = {}
    number_department = {}

    affiliated_people = [] # people who are affiliated with the author

    # the table to parse from PBN
    table = soup.find("table", {"id":"aspect_pbn_PBNItemViewer_table_employed_tab"})
    
    # if the table exists
    if table:
        # get all rows
        table_rows = table.find_all('tr')

        for tr in table_rows:

            td = tr.find_all('th') + tr.find_all('td')
            row = [classifier(i) for i in td]
            # print(row)

            if row[0] == 'autor/redaktor':
                for number, cell in enumerate(row[1:]):
                    number_department [number] = cell.rstrip()
            else:
                for number, cell in enumerate(row[1:]):
                    # get the right cell and dig inside untill the checkbox is found. 
                    # Then get the checkbox
                    # if 'checked' is one of the attributes. Then it's checked. (found out empirically)
                    if cell:
                        clean_name = row[0].rstrip()
                        person_department [ clean_name ] = number_department [number]

        # assign status to each person
        target_department = person_department [ clean_target_person ]

        for person, dept in person_department.items():
            if dept == target_department:
                affiliated_people.append(person)
    else:
        # at least the author must be affiliated
        affiliated_people.append(('the_author', True))

    # print(f"Person -> department: {person_department}")

    # print(f"Person -> status: {affiliated_people}")
    
    return affiliated_people

def search(names, dates):

    start = time.time()

    # link = 'https://ruj.uj.edu.pl/xmlui/discover?filtertype_1=author&filter_relational_operator_1=equals&filter_1=Cieśla,+Michał+%5BSAP11018214%5D&filtertype_2=dateIssued&filter_relational_operator_2=equals&filter_2=2019&view=mod1&'
    # correct
    # link = 'https://ruj.uj.edu.pl/xmlui/discover?view=mod3&query=&scope=%2F&filtertype_1=author&filter_relational_operator_1=equals&filter_1=Dybiec%2C+Bart%C5%82omiej+%5BSAP11018789%5D&filtertype_2=dateIssued&filter_relational_operator_2=equals&filter_2=2019&filtertype_3=title&filter_relational_operator_3=contains&filter_3=&submit_apply_filter=Apply'.replace('+', ' ')
    # link='https://ruj.uj.edu.pl/xmlui/discover?view=mod2&query=&scope=%2F&filtertype_1=author&filter_relational_operator_1=equals&filter_1=Barbasz%2C+Jakub+%5BSAP11019396%5D&filtertype_2=dateIssued&filter_relational_operator_2=equals&filter_2=2019&filtertype_4=title&filter_relational_operator_4=contains&filter_4=&submit_apply_filter=Apply&query=&scope=%2F'
    # name = 'Dybiec, Bartłomiej [SAP11018789]'
    # date = '2018, 2019'
    name = names
    date = dates
    # if not date:
    #     link = f'https://ruj.uj.edu.pl/xmlui/discover?view=mod1&query=&scope=/&filtertype_1=author&filter_relational_operator_1=equals&filter_1={name}&filtertype_4=title&filter_relational_operator_4=contains&filter_4=&submit_apply_filter=Apply&query=&scope=/'
    # else:
    #     link = f'https://ruj.uj.edu.pl/xmlui/discover?view=mod3&query=&scope=/&filtertype_1=author&filter_relational_operator_1=equals&filter_1={name}&filtertype_2=dateIssued&filter_relational_operator_2=contains&filter_2={date}&filtertype_4=title&filter_relational_operator_4=contains&filter_4=&submit_apply_filter=Apply&query=&scope=/'

    date_from, date_to = dates.split(',')
    dates_range = []
    try:
        date_from = int(date_from)
        date_to = int(date_to)+1
        dates_range = str(list(range(date_from, date_to)))[1:-1]
        if not dates_range:
            dates_range = date_from
    except ValueError:
        publication = Publication()
        publication.title = 'Can\'t parse one of the dates'
        return [publication]
    front = 'https://ruj.uj.edu.pl/xmlui/discover?view=mod1&query=&scope=/'
    splited_names = names.split(';')
    cnt = 1
    for name in splited_names:
        front += f'&filtertype_{cnt}=author&filter_relational_operator_{cnt}=equals&filter_{cnt}={name}'
        cnt += 1
    if date:
        front += f'&filtertype_{cnt}=dateIssued&filter_relational_operator_{cnt}=contains&filter_{cnt}={dates_range}'
    link = front

    # print(link)
    # print(f'Dates: {dates}')
# 'https://ruj.uj.edu.pl/xmlui/handle/item/82915?view=mod1&search-result=true&query=&current-scope=&filtertype_0=author&filtertype_1=title&filter_relational_operator_1=contains&filter_relational_operator_0=equals&filter_1=&filter_0=Cie%C5%9Bla%2C+Micha%C5%82+%5BSAP11018214%5D&rpp=50&sort_by=score&order=desc'
# Cieśla, Michał [SAP11018214]
# Dybiec, Bartłomiej [SAP11018789]
# https://ruj.uj.edu.pl/xmlui/discover?view=mod1&query=&scope=/&filtertype_1=author&filter_relational_operator_1=equals&filter_1=Cieśla,+Michał+[SAP11018214]&filtertype_3=author&filter_relational_operator_3=equals&filter_3=Dybiec,+Bartłomiej+[SAP11018789]&submit_apply_filter=Apply&query=&scope=/
# https://ruj.uj.edu.pl/xmlui/discover?view=mod1&query=&scope=/&filtertype_1=author&filter_relational_operator_1=equals&filter_1=Cieśla,+Michał+[SAP11018214]&filtertype_2=author&filter_relational_operator_2=equals&filter_2=Dybiec,+Bartłomiej+[SAP11018789]&filtertype_3=author&filter_relational_operator_3=equals&filter_3=Capała,+Karol+[USOS176576]&submit_apply_filter=Apply&query=&scope=/
    
    print(link)
    
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')

    # find all script tags from the source page where there's a 'fields part'
    fields = list(filter(lambda x: True if 'fields' in x.string else False,
                        soup.find_all('script', type='text/javascript', src=None)
                ))

    # there should be only one result so take the first one from the list
    data = fields[0] if len(fields) > 0 else []

    # take all element that are between curly brackets
    elements = re.findall(r"\{(.*?)\}", str(data))

    publications = []
    same_department_list = []
    publication = None

    for element in elements:
        try:
            left, right = element.split(':', 1)
        except ValueError:
            continue
        # print(f'Left: {left}, right: {right}')
        # print(len(element.split(':')))
        if left.strip('"') == "dc.id":
            publication = Publication()
            publication.id = right.replace('\"', '').replace(' ', '')
            publications.append(publication)
            publication.affiliated_authors = parse_publication(publication.id, name)
        # if left.strip('"') == "dc.contributor.author" or left.strip('"') == "dc.contributor.editor":
        if left.strip('"') == "dc.contributor.author":    
            publication.authors.append(right.replace('\"',''))
        if left.strip('"') == "dc.title":
            publication.title = right.replace('\"','')
        if left.strip('"') == "dc.pointsMNiSW":
            publication.points = int(right.replace('\"','').split(':')[1].strip(' '))
        if left.strip('"') == "dc.date.issued":
            publication.year = right.replace('\"','')
    # publications.append(publication)

    # print(publications)

    #print(f"Decoded URL: {requests.utils.unquote('https://ruj.uj.edu.pl/xmlui/discover?view=mod3&query=&scope=%2F&filtertype_1=author&filter_relational_operator_1=equals&filter_1=Dybiec%2C+Bart%C5%82omiej+%5BSAP11018789%5D&filtertype_2=dateIssued&filter_relational_operator_2=contains&filter_2=2018%2C+2019&filtertype_4=title&filter_relational_operator_4=contains&filter_4=&submit_apply_filter=Apply&query=&scope=%2F')}")

    end = time.time()

    print(f"Parsing took: Seconds: {end - start}. Minutes: {(end - start) / 60}")

    # for number, publication in enumerate(publications):
    #     print(f"{number} : {publication.id} : {publication.title}")

    return publications
