"""
Update the price_file to the latest version.

Create the unixgeekSpellPricesYYYY-MM-DD.csv
as follows:
go to:
https://unixgeek.com/last-week-P1999Green.html

Highlight all the columns that have "Spell:" at the
start, copy and paste those 4 columns into a new
google sheet

Do a file -> Download -> .csv

Save that file in price_data, named accordingly.

Create the spell_counts file using parse_spell_mules.py --count,
capture the output.

At this point, update this script with the new spell_prices file.

Update the update_spell_prices.py with all 3 files.

You can use update_spell_prices.py to see what adjustments
to pricing might be made.
Update the spell_prices-YYYY-MM-DD.py accordingly

Eventual work would be comining the info in the
spell_counts file and the unixgeek pricing to create
spell prices on the fly. Also use previous spell prices.

1. If we have no copies, set the prices to None
2. If our prices are higher than the unixgeek, just
output that info.
3. If we have copies, but the prices are set to None
output the unixgeek info.

"""

import os
import sys

import class_spells
import parse_spell_mules


price_file = "spell_prices-2022-07-14.py"

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
    with open("price_data" + os.sep + price_file) as spell_prices:
        for spell in spell_prices:
            name = spell.split(",")[0]
            external = spell.split(",")[1]
            internal = spell.split(",")[2].strip()
            spell_list.append(Spell(name, external, internal))

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
