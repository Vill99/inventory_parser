# parse inventory
import re
import sys

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
           "Hand Made Backpack",
           "Large Box"
           ]

def main():
    try:
        toon = sys.argv[1]
    except:
        print("Give the name of the character to parse")
        quit()

    inventory = get_inventory(toon)
    if inventory:
        print(toon)
        print(inventory)
        for item in inventory:
            print(item)
    else:
        print("Nothing to see here")


def get_inventory(mule_name):
    file_name = mule_name + "-Inventory.txt"
    item_list = []
    try:
        with open(file_name) as inventory:
            for line in inventory:
                split_line = re.split(r'\t+', line.rstrip('\t'))
                if split_line[1] not in garbage:
                    item_list.append(split_line[1])
    except:
        print(mule_name + " not found.")
        pass
    return item_list


if __name__ == '__main__':
    main()
