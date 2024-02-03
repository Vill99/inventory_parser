from datetime import datetime
import json
import os

import requests

URL = 'https://pigparse.azurewebsites.net/api/item/getall/Green'
page = requests.get(URL)

today = datetime.today().strftime('%Y-%m-%d')
prefix = ".." + os.sep + "price_data" + os.sep
price_file_path = prefix + "pigparsePrices{}.csv".format(today)

spell_price_list = []
item_list = json.loads(page.text)
#print(item_list)
for item in item_list:
    if item["t"] == 0:
        if item["n"].startswith("Spell:"):
            the_date = item["l"].split("T")[0]
            item_name = item["n"]
            count = str(item["t30"])
            average = str(item["a30"])
            spell_price_list.append([the_date, item_name, count, average])
            #print(item)


with open(price_file_path, "w") as price_file:
    for line in spell_price_list:
        if line[1].startswith("Spell:"):
            price_file.write(','.join(line) + '\n')
