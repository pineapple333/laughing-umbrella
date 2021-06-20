import json
from bs4 import BeautifulSoup
import requests
import re
from .models import Publication


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


def parse_publication(pubId, target_person):

    clean_target_person = ""
    if "[" in target_person:
        clean_target_person = f"{target_person.split()[0].replace(',', '') } {' '.join(target_person.split()[1:-1])}"
    else:
        clean_target_person = f"{target_person.split()[0].replace(',', '') } {' '.join(target_person.split()[1:])}"

    # create the link
    link = f'https://ruj.uj.edu.pl/xmlui/handle/{pubId}/pbn'
    # get raw text
    r = requests.get(link)
    # parse the text
    soup = BeautifulSoup(r.text, 'html.parser')


    # initialize the dictionary
    person_status = []

    person_department = {}
    number_department = {}

    affiliated_people = []  # people who are affiliated with the author

    # the table to parse from PBN
    table = soup.find("table", {"id": "aspect_pbn_PBNItemViewer_table_affiliated_tab"})

    # if the table exists
    if table:
        # get all rows
        table_rows = table.find_all('tr')

        for tr in table_rows:

            td = tr.find_all('th') + tr.find_all('td')
            row = [classifier(i) for i in td]

            print(row)

            if row[0] == 'autor/redaktor':
                for number, cell in enumerate(row[1:]):
                    number_department[number] = cell.rstrip()
            else:
                for number, cell in enumerate(row[1:]):
                    # get the right cell and dig inside untill the checkbox is found.
                    # Then get the checkbox
                    # if 'checked' is one of the attributes. Then it's checked. (found out empirically)
                    if cell:
                        clean_name = row[0].rstrip().replace(',','')
                        person_department[clean_name] = number_department[number]

        # assign status to each person
        target_department = person_department[clean_target_person]

        for person, dept in person_department.items():
            if dept == target_department:
                affiliated_people.append(person)
    else:
        # at least the author must be affiliated
        affiliated_people.append(('the_author', True))

    return affiliated_people


def search(names, dates):

    name = names
    date = dates

    date_from, date_to = dates.split(',')
    dates_range = []
    try:
        date_from = int(date_from)
        date_to = int(date_to) + 1
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
    front += f'&filtertype_{cnt+1}=doctype&filter_relational_operator_{cnt+1}=equals&filter_{cnt+1}=JournalArticle'
    link = front

 
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
        if left.strip('"') == "dc.id":
            publication = Publication()
            publication.id = right.replace('\"', '').replace(' ', '')
            publications.append(publication)
            publication.affiliated_authors = parse_publication(publication.id, name)
        if left.strip('"') == "dc.contributor.author":
            publication.authors.append(right.replace('\"', ''))
        if left.strip('"') == "dc.title":
            publication.title = right.replace('\"', '')
        if left.strip('"') == "dc.pointsMNiSW":
            publication.points = int(right.replace('\"', '').split(':')[1].strip(' '))
        if left.strip('"') == "dc.date.issued":
            publication.year = right.replace('\"', '')


    return publications