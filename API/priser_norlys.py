import requests
from bs4 import BeautifulSoup

#response = requests.get("https://norlys.dk/kundeservice/el/flexel-prisudvikling/")
response = requests.get("https://data.nordpoolgroup.com/auction/day-ahead/prices?deliveryDate=latest&currency=DKK&aggregation=Hourly&deliveryAreas=DK1")

print(response.status_code)

import re

soup = BeautifulSoup(response.content, 'html.parser')

print(soup.prettify())

s = soup.find('div')
#print(s.prettify())
content = soup.find_all('tbody')

print(content)
    

for line in soup.prettify():
    #print(line)

    pass
