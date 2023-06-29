"""
Look up a spell. Show the count, price data and which toons are 
holding it.

"""
import datetime
import os
import re
import sys
from collections import Counter

from parse_spell_mules import get_spells, is_spell_or_song

PRICE_DATA_DIR = "price_data"
INVENTORY_DIR = ".." + os.sep + "equi" + os.sep
inventory_path = INVENTORY_DIR

def find_newest_file(prefix):
    """Find the latest copy of a file, given the prefix."""
    dir_list = os.listdir(PRICE_DATA_DIR)
    files = []
    for afile in dir_list:
        if afile.startswith(prefix):
            files.append(afile[len(prefix):])
    dates = []
    for afile in files:
        if afile.endswith(".py"):
            afile = afile[:-3]
            dates.append(afile)
    return prefix + max(dates) + ".py"

def lookup_count(spell):
    """Given a spell name, look up the count."""
    recent_count_file = find_newest_file("spell_counts-")
    with open(PRICE_DATA_DIR + os.sep + recent_count_file) as counts:
        for line in counts:
            try:
                result = re.search("\'(.*)\'", line)
                spell_name = result.group(1)
            except:
                spell_name = None
            try:
                count = line.strip().split(',')[1].strip('\]').strip()
            except:
                count = None
            if spell_name:
                if spell_name.lower() == spell.lower():
                    print(spell + ": " + count + " copies")
                    return
    print("No copies of: " + spell)


def lookup_price(spell):
    """Given a spell name, look up the pricing info."""
    recent_price_file = find_newest_file("spell_prices-")
    with open(PRICE_DATA_DIR + os.sep + recent_price_file) as prices:
        for line in prices:
            try:
                spell_name = line.split(',')[0].strip('\"')
            except:
                spell_name = None
            if spell_name.lower() == spell.lower():
                try:
                    external = line.split(',')[1].strip()
                except:
                    external = None
                try:
                    internal = line.split(',')[2].strip()
                except:
                    internal = None
                if spell_name:
                    print("External price: " + external)
                    print("Internal price: " + internal)
                return
        print("No pricing info for: " + spell)


def find_spell(spell):
    """Given a spell, find all the toons that have it in their inventory."""
    dir_list = os.listdir(INVENTORY_DIR)
    toon_count_list = []
    for afile in dir_list:
        if afile.endswith("-Inventory.txt"):
            get_spells(afile[:-14])
            with open(INVENTORY_DIR + os.sep + afile) as inventory:
                for line in inventory:
                    try:
                        split_line = re.split(r'\t+', line.rstrip('\t'))
                        if is_spell_or_song(split_line[1]):
                            try:
                                spell_name = split_line[1].split("Spell: ")
                                if spell_name[1] == spell:
                                    toon_count_list.append(afile[:-14])
                            except:
                                pass
                            try:
                                song_name = split_line[1].split("Song: ")
                                if song_name[1] == spell:
                                    toon_count_list.append(afile[:-14])
                            except:
                                pass
                    except:
                        pass
    toon_count_dict = Counter(toon_count_list)
    for toon in toon_count_dict:
        print(toon + ": "+ str(toon_count_dict[toon]))


def main():
    try:
        spell = sys.argv[1]
    except:
        print("You need to provide a spell name to look up.")
        quit()    
    lookup_count(spell)
    lookup_price(spell)
    find_spell(spell)


if __name__ == '__main__':
    main()
