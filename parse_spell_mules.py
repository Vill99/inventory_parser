# parse inventory
import os
import re

import mule_list

garbage = ["Short Sword*",
           "A Worn Candle",
           "Skin of Milk",
           "Bread Cakes*",
           "Empty",
           "Name",
           "Song: Chant of Battle*",
           "A tattered note",
           "Tome of Order and Discord",
           "Club*",
           "Backpack",
           "Large Sewing Kit",
           "Colorfully Patched Tunic*"
           ]

inventory_path = ".." + os.sep + "equi" + os.sep
min_number_to_sell = 3

class Inventory:
    def __init__(self, name):
        self.name = name
        self.inventory = []

    def add_inventory(self, inventory):
        for item in inventory:
            self.inventory.append(item)

    # def __str__(self):
    #     output = self.name
    #     for item in self.inventory:
    #         output += ",{}".format(item)
    #     return output
    #     #return "{}\n{}".format(self.name, self.inventory)


def main():
    master_spell_list = []
    spell_dict = {}
    for mule in mule_list.spellmules:
        spells = get_spells(mule)
        if spells:
            master_spell_list.extend(spells)
    # for spell in master_spell_list:
    #     print spell
    for counter in range(len(master_spell_list)):
        spell_dict[master_spell_list[counter]] = master_spell_list.count(
            master_spell_list[counter]
            )
    print spell_dict
    sell_list = []
    for spell in spell_dict:
        if spell_dict[spell] >= min_number_to_sell:
            sell_list.append(spell)
    sell_list.sort()
    for spell in sell_list:
        print spell


def get_spells(mule_name):
    file_name = inventory_path + mule_name + "-Inventory.txt"
    spell_list = []
    try:
        with open(file_name) as inventory:
            for line in inventory:
                split_line = re.split(r'\t+', line.rstrip('\t'))
                if split_line[1] not in garbage:
                    if split_line[1].startswith("Spell: "):
                        spell_name = split_line[1].split("Spell: ")
                        spell_list.append(spell_name[1])
    except:
        pass
    return spell_list


if __name__ == '__main__':
    main()
