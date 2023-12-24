import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv

url = 'https://www.value.today/world-top-companies-by-business-sector'

def parser(text):
    soup = BeautifulSoup(text, 'html.parser')

    mainDiv = soup.find('div', class_ = 'view-content')
    if mainDiv is not None:
        sectorDivs = mainDiv.find_all('div', class_ = 'col-md-4 col-sm-6 btn btn-default views-row')
        if len(sectorDivs) != 0:
            for sectorDiv in sectorDivs:
                sectord = sectorDiv.find('div', class_ = 'views-field views-field-name')
                if sectord is not None:
                    sector = sectord.find('a').text
                    sector = sector.strip()

                    with open('sectors.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([sector])
                else:
                    print('sector not found')
        else:
            print('sectorDivs not found')
    else:
        print('mainDiv not found')


req = requests.get(url)
parser(req.text)