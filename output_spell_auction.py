import os
import sys

import class_spells
import parse_spell_mules


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


def print_spell(spell, price):
    if price and price != "None":
        print(spell.replace("`", "'") + " - " + price + "p")


def main():
    try:
        auction = sys.argv[1]
    except:
        auction = None
    if auction not in ["internal", "external"]:
        print("first parameter should be internal or external")
        quit()

    spell_dict = parse_spell_mules.create_spell_dict()
    spell_count = parse_spell_mules.spell_count(spell_dict)
    spell_list = []
    price_file = "spell_prices-2021-12-18.py"
    with open("pricing_work" + os.sep + price_file) as spell_prices:
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
                    print_spell(spell, internal)
                else:
                    print_spell(spell, external)
        print("")


if __name__ == '__main__':
    main()
