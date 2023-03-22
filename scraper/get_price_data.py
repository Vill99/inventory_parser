from datetime import datetime
import os

import requests
from bs4 import BeautifulSoup


URL = 'https://unixgeek.com/last-week-P1999Green.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

today = datetime.today().strftime('%Y-%m-%d')
prefix = ".." + os.sep + "price_data" + os.sep
price_file_path = prefix + "unixgeekPrices{}.csv".format(today)

spell_price_list = []
tables = soup.find_all('table', class_='columnar')
for table in tables:
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if (columns != []):
            last_seen = columns[0].text.strip()
            item = columns[1].text.strip()
            count = columns[2].text.strip()
            average = columns[3].text.strip()
            spell_price_list.append([last_seen, item, count, average])

print(spell_price_list)
with open(price_file_path, "w") as price_file:
    for line in spell_price_list:
        if line[1].startswith("Spell:"):
            price_file.write(','.join(line) + '\n')
