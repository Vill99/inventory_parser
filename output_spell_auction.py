"""
Step 1.
Create the pigparsePricesYYYY-MM-DD.csv
You will need to pip install:
requests

cd into the scraper directory
python get_pigparse_data.py

You could do this step manually:
as follows:
go to:
https://pigparse.azurewebsites.net/ServerIndex/Green

Filter by "Spell:"
You'll have to manually create a csv from the 4 columns:
    Last Seen (Just the date, don't need the time)
    Item
    30d Count
    30d Avg

Step 2.
Create the spell_counts file using python parse_spell_mules.py -o -c

Step 3.
You can duplicate the most recent spell_prices file with today's date.

Step 4.
You can use update_spell_prices.py to see what adjustments
to pricing might be made.
Update the spell_prices-YYYY-MM-DD.py accordingly

Step 5.
Run this script
python output_spell_auction.py external
And copy paste the output to discord auction channels

Future:
Eventual work would be combining the info in the
spell_counts file and the pigparse pricing to create
spell prices on the fly. Also use previous spell prices.
Basically, make update_spell_prices.py more proactive.

1. If we have no copies, just leave the price unadjusted
since it's irrelevant, we output the ones that are being undercut
2. If our prices are higher than the pigparse, reduce the
price if we have more than 1 copy. 
3. If we have copies, but the prices are set to None
update the price to the pigparse price.
4. If we are pricing too low compared to pigparse, raise the price
unless we have more than 5 copies.
5. Log any price update.

"""
from datetime import datetime
import os
import sys

import class_spells
import parse_spell_mules

today = datetime.today().strftime('%Y-%m-%d')
price_file = "spell_prices-{}.py".format(today)

class Spell:
    def __init__(self, name, external, internal):
        self.name = name
        self.external = external
        self.internal = internal
    def __str__(self):
        if self.external and self.internal:
            return self.name + self.external
        return ""


def get_price(spell, spell_list):
    for a_spell in spell_list:
        if spell.replace("`", "'") == a_spell.name.strip('\"'):
            return a_spell.external, a_spell.internal
    return None, None


def print_spell(spell, price, min_price):
    if price and price != "None":
        if int(price) > min_price:
            print(spell.replace("`", "'") + " - " + price + "p")


def main():
    try:
        auction = sys.argv[1]
    except:
        auction = None
    try:
        min_price = int(sys.argv[2])
    except:
        min_price = 0
    if auction not in ["internal", "external"]:
        print("first parameter should be internal or external")
        quit()

    spell_dict = parse_spell_mules.create_spell_dict()
    spell_count = parse_spell_mules.spell_count(spell_dict)
    spell_list = []
    try:
        with open("price_data" + os.sep + price_file) as spell_prices:
            for spell in spell_prices:
                name = spell.split(",")[0]
                external = spell.split(",")[1]
                internal = spell.split(",")[2].strip()
                spell_list.append(Spell(name, external, internal))
    except FileNotFoundError as e:
        print(e)
        print("ERROR: Did you create new pricing files for today?")
        quit(1)

    for class_name in class_spells.classes:
        print("")
        print("**{} Spells**".format(class_name.capitalize()))
        for spell in spell_dict:
            external, internal = get_price(spell, spell_list)
            if spell in class_spells.classes[class_name]:
                if auction == "internal":
                    print_spell(spell, internal, min_price)
                else:
                    print_spell(spell, external, min_price)

        print("")


if __name__ == '__main__':
    main()
