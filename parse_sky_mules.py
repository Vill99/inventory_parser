# parse inventory
import os
import re
import sys

import mule_list

garbage = [
    "Short Sword*",
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
    "Large Sewing Kit"
]


class Inventory:
    def __init__(self, name):
        self.name = name
        self.inventory = []

    def add_inventory(self, inventory):
        for item in inventory:
            self.inventory.append(item)

    def __str__(self):
        output = self.name
        for item in self.inventory:
            output += ",{}".format(item)
        return output
        #return "{}\n{}".format(self.name, self.inventory)


def set_inventory():
    try:
        arg_one = sys.argv[1]
        inventory_path = ".." + os.sep + arg_one + os.sep
    except:
        inventory_path = ".." + os.sep
    return inventory_path


def get_inventory(mule_name, inventory_path):
    file_name = inventory_path + mule_name + "-Inventory.txt"
    item_list = []
    try:
        with open(file_name) as inventory:
            for line in inventory:
                split_line = re.split(r'\t+', line.rstrip('\t'))
                if split_line[1] not in garbage:
                    item_list.append(split_line[1])
    except:
        pass
    return item_list


def main():
    inventory_path = set_inventory()
    mule_inventory_list = []
    for mule in mule_list.skymules:
        inventory = get_inventory(mule, inventory_path)
        if inventory:
            mule_inventory = Inventory(mule)
            mule_inventory.add_inventory(inventory)
            mule_inventory.inventory.sort()
            mule_inventory_list.append(mule_inventory)
            #print(mule_inventory)
    for inventory in mule_inventory_list:
        print(inventory)


if __name__ == '__main__':
    main()
