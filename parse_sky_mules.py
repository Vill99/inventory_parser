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

def main():
    mule_inventory_list = []
    for mule in mule_list.skymules:
        inventory = get_inventory(mule)
        if inventory:
            mule_inventory = Inventory(mule)
            mule_inventory.add_inventory(inventory)
            mule_inventory.inventory.sort()
            mule_inventory_list.append(mule_inventory)
            #print(mule_inventory)
    for inventory in mule_inventory_list:
        print(inventory)


def get_inventory(mule_name):
    file_name = ".." + os.sep + mule_name + "-Inventory.txt"
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


if __name__ == '__main__':
    main()
