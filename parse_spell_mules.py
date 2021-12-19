# parse inventory
import os
import re
import sys

import class_spells
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
           "Colorfully Patched Tunic*",
           "Elemental Grimoire"
           ]


inventory_path = ".." + os.sep + "equi" + os.sep


class Inventory:
    def __init__(self, name):
        self.name = name
        self.inventory = []

    def add_inventory(self, inventory):
        for item in inventory:
            self.inventory.append(item)


def main():
    min_number_to_sell, max_number_to_sell = get_sell_ranges()
    spell_dict = create_spell_dict()
    spell_counts = spell_count(spell_dict)
    for spell in spell_counts:
        print(spell)
    for class_name in class_spells.classes:
        print("")
        print("**{} Spells**".format(class_name.capitalize()))
        for spell in spell_dict:
            if spell in class_spells.classes[class_name]:
                if spell_dict[spell] >= min_number_to_sell:
                    if spell_dict[spell] <= max_number_to_sell:
                        print_spell(spell)
        print("")

    for spell in spell_dict:
        found = False
        for class_name in class_spells.classes:
            if spell in class_spells.classes[class_name]:
                found = True
        if not found:
            print("Did not find {}".format(spell))


def get_sell_ranges():
    try:
        min_number_to_sell = int(sys.argv[1])
    except:
        min_number_to_sell = 3
    try:
        max_number_to_sell = int(sys.argv[2])
    except:
        max_number_to_sell = 99
    return min_number_to_sell, max_number_to_sell


def create_spell_dict():
    master_spell_list = []
    spell_dict = {}
    for mule in mule_list.spellmules:
        spells = get_spells(mule)
        if spells:
            master_spell_list.extend(spells)
    # Count all the spells
    for counter in range(len(master_spell_list)):
        spell_dict[master_spell_list[counter]] = master_spell_list.count(
            master_spell_list[counter]
            )
    return spell_dict


def spell_count(spell_dict):
    """Print the spell and number in alphabetical order."""
    spell_counts = []
    for key in sorted(spell_dict.keys()):
        #print(key, spell_dict[key])
        spell_counts.append([key, spell_dict[key]])
    return spell_counts

def print_spell(spell):
    print(spell.replace("`", "'"))


def is_spell_or_song(scroll):
    if scroll.startswith("Spell: "):
        return True
    if scroll.startswith("Song: "):
        return True
    return False


def get_spells(mule_name):
    file_name = inventory_path + mule_name + "-Inventory.txt"
    spell_list = []
    try:
        with open(file_name) as inventory:
            for line in inventory:
                split_line = re.split(r'\t+', line.rstrip('\t'))

                if split_line[1] not in garbage:
                    if is_spell_or_song(split_line[1]):
                        try:
                            spell_name = split_line[1].split("Spell: ")
                            spell_list.append(spell_name[1])
                        except:
                            pass
                        try:
                            song_name = split_line[1].split("Song: ")
                            spell_list.append(song_name[1])
                        except:
                            pass
    except:
        pass
    return spell_list


if __name__ == '__main__':
    main()
