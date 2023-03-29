from datetime import datetime
import json
import os

import requests

URL = 'https://pigparse.azurewebsites.net/api/ServerItem/Green'
page = requests.get(URL)

today = datetime.today().strftime('%Y-%m-%d')
prefix = ".." + os.sep + "price_data" + os.sep
price_file_path = prefix + "pigparsePrices{}.csv".format(today)

spell_price_list = []
item_list = json.loads(page.text)
for item in item_list:
    if item["auctionType"] == 0:
        if item["itemName"].startswith("Spell:"):
            the_date = item["lastSeen"].split("T")[0]
            item_name = item["itemName"]
            count = str(item["totalLast30DaysCount"])
            average = str(item["totalLast30DaysAverage"])
            spell_price_list.append([the_date, item_name, count, average])


with open(price_file_path, "w") as price_file:
    for line in spell_price_list:
        if line[1].startswith("Spell:"):
            price_file.write(','.join(line) + '\n')
