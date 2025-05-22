# check the raid requirement items given an inventory dump file
# GENERAL
# Thurg pot
# CT Pot
# Idol
# Reaper
# Cap
# Invis Rings
# Larrikan's mask
# Box
# Batteries
# ST Key
# Vp Key
# OT Hammer
# Seb Key
# Lev Cloak
# JBoots
# WR Bags, 
# LBS = Light Burlap Sack
# LSB = Large Soiled Bag
# EE = Evil Eye Bag
# SP = Shralock Pack
# TP = Traveler's Pack
# AK = Box of Abukar
# LH = Lionhide Backpack
# NS = Box of Nil Space
# Wort Pots
# Shrink Pots

# CLERIC
# Emeralds
# Cleric Epic
# Peridots
# Thurg Armor
# Thurg Armor pieces
# Growth Armor
# Skyshrine Armor
# Kael Armor
# Weight of the Gods

# MAGE
# Pearls
# Malachite
# DA Ring
# DA Ear

# WIZ
# Portal Fragments
# Food Water

# NECRO
# Bone Chips

# SHAMAN
# Shaman Epic

# BARD
# DE Mask


# Tell me the age of the Inventory file if it's older than 1 day
# 

# Some features that take more thought
# 6 necks all have diff names
# Custom vs non custom helms
# Some countable things aren't needed on every toon
# Like Bark Potions
# Or Shrink Pots
# Earring of the Frozen Skull doesn't belong on every class
# nor does Larrikan's Mask

# Default is to check all toons
# Optionally, specify a single name to check
# Not yet working:
# Get the class from spellbook, or optional set class on command line
# other options check all bots, or all of a class of bots

import argparse

import bot_list
from parse_inventory import get_counts


items_to_check = [
    "Larrikan's Mask",
    'Earring of the Frozen Skull',
    'Leatherfoot Raider Skullcap',
    'Reaper of the Dead',
    'Pegasus Feather Cloak',
    'Worker Sledgemallet',
    'Vial of Velium Vapors',
    'Box of the Void',
    "Journeyman's Boots",
    'Shiny Brass Idol',
]
items_to_count = [
    # intentionally misspelled
    "Veluim Vial",
    'Lizard Blood Potion',
    'Golem Metal Wand',
    'Ring of Shadows',
    "10 Dose Ant's Potion",
    '10 Dose Potion of Stinging Wort',
    '10 Dose Blood of the Wolf',
    '10 Dose Greater Null Potion',
    'Forlorn Totem of Rolfron Zek',
]
weight_bags = [
    'Large Soiled Bag',
    'Darkwood Trunk',
    'Box of Abu-Kar',
    'Bag of the Tinkerers',
    'Light Burlap Sack',
    'Bag of Sewn Evil-Eye',
    'Shralok Pack',
    "Travelers Pack",
    "Lionhide Backpack",
    "Box of Nil Space",
    'Deluxe Toolbox',
    'Hand Made Backpack',
    'Backpack',
    'Lexicon',
    'Large Sewing Kit',
]
keys = [
    'Key to Charasis',
    'Key of Veeshan',
    'Shrine Key',
    'Trakanon Idol',
    'Tooth of the Cobalt Scar',
    "Sleeper's Key",
]
flowers = [
    'Green Flower of Functionality',
    'Black Flower of Functionality',
    'Blue Flower of Functionality',
    'White Flower of Functionality',
    'Red Flower of Functionality',
]
cleric_gear = [
    "Circlet of the Falinkan",
    'Earring of Cleansing',
    'Earring of Purity',
    "Ayillish's Talisman",
    "Iksar Hide Cape",
    "Coldain Skin Gloves",
    "Coldain Skin Boots",
    "Ring of Di`zok",
]
cleric_items_to_check = [
    'Weight of the Gods',
    'Water Sprinkler of Nem Ankh',
    'Necklace of Resolution',
]
cleric_items_to_count = [
    'Mana Battery - Class Three',
    'Mana Battery - Class Four',
    'Stalking Probe',
    'Emerald',
    'Peridot',
]
cleric_thurg = [
    "Vambraces of Forbidden Rites",
    "Bracers of Forbidden Rites",
    "Breastplate of Forbidden Rites",
    "Greaves of Forbidden Rites",
    "Gauntlets of Forbidden Rites",
    "Custom Crown of Forbidden Rites",
    "Crown of Forbidden Rites",
    "Boots of Forbidden Rites"
]
mage_items_to_check = [
    'Duennan Shielding Ring',
    'Earring of the Frozen Skull',
    'Box of the Void',
    'Clay Bracelet',
]
mage_items_to_count = [
    'Pearl',
    'Malachite',
    'Mana Battery - Class Five',
    'Bark Potion',
]
wiz_items_to_count = [
    'Small Portal Fragments',
    'Peridot',
]
necro_items_to_count = [
    'Bone Chips',
]
shaman_items_to_check = [
    'Black Fur Boots',
    'Spear of Fate',
]
soulfire_parts = [
    'Bog Juice',
    'Edible Goo',
    "Drom's Champagne",
    'Bunker Cell #1',
    'H.K. 102',
    'A Sealed Note',
    'A Spider Venom Sac',
    'Cloth Shirt',
    'Token of Generosity',
    'Token of Bravery',
    'Token of Truth',
    'Testimony',
    'Glowing Sword Hilt',
    'Testimony of Truth',
    'Brilliant Sword of Faith',
    'unsealed note',
    'SoulFire',
]


def get_args():
    """Get arguments from the command line."""
    parser = argparse.ArgumentParser(
        description='Search inventory files for raid requirements.'
    )
    parser.add_argument(
        "-n",
        "--name",
        help="""Name of the toon. If no name is specified, will look at all
        Inventory files in the current directory"""
    )
    parser.add_argument(
        "-c",
        choices=["cleric", "mage", "necro", "wiz", "druid", "shaman"],
        help="""Class requirements to check."""
    )
    parser.add_argument(
        "--ok",
        "-o",
        action='store_true',
        help="""Also print the items that are OK."""
    )
    parser.add_argument(
        "--keys",
        "-k",
        action='store_true',
        help="""Print out the keys."""
    )
    parser.add_argument(
        "--bags",
        "-b",
        action='store_true',
        help="""Print out the weight bags."""
    )
    parser.add_argument(
        "--gear",
        "-g",
        action='store_true',
        help="""Print out general gear items."""
    )
    parser.add_argument(
        "--flowers",
        "-f",
        action='store_true',
        help="""Print out pom flowers."""
    )
    parser.add_argument(
        "--thurg",
        "-t",
        action='store_true',
        help="""Print out thurg gear items."""
    )
    parser.add_argument(
        "--soulfire",
        "-s",
        action='store_true',
        help="""Print out items for soulfire quest."""
    )
    args = parser.parse_args()
    # if args.c is None:
    #     args.c = "None"    
    return args

def check_class_bots(args):
    """Check all the bots of a specific class."""
    if args.c.lower() == "cleric":
        for bot in bot_list.cleric:
            args.name = bot
            check_requirements(args)
    if args.c.lower() == "mage":
        for bot in bot_list.mage:
            args.name = bot
            check_requirements(args)
    if args.c.lower() == "druid":
        for bot in bot_list.druid:
            args.name = bot
            check_requirements(args)
    if args.c.lower() == "wiz":
        for bot in bot_list.wiz:
            args.name = bot
            check_requirements(args)
    if args.c.lower() == "necro":
        for bot in bot_list.necro:
            args.name = bot
            check_requirements(args)
    if args.c.lower() == "shaman":
        for bot in bot_list.shaman:
            args.name = bot
            check_requirements(args)


def check_item(args, item, counts):
    """Check if a particular item is in the inventory."""
    items = [it[0] for it in counts]
    if item in items:
        if args.ok:
            print(item.ljust(40, ' ') + ": OK")
    else:
        print(item.ljust(40, ' ') + ": MISSING")

def count_item(item, counts):
    """Count number of items they have."""
    total = 0
    for it in counts:
        if it[0] == item:
            total += int(it[1])
    print(item.ljust(40, ' ') + ": {}".format(str(total)))


def check_requirements(args):
    """Check the requirements for a toon."""
    counts = get_counts(args.name)
    print('-'.center(45, '-'))
    print(args.name.center(45, ' '))
    print("GENERAL".center(45, ' '))
    for item in items_to_check:
        check_item(args, item, counts)
    
    for item in items_to_count:
        count_item(item, counts)
    if args.bags:
        print("WEIGHT BAGS".center(45, ' '))
        for item in weight_bags:
            count_item(item, counts)
    if args.keys:
        print("KEYS".center(45, ' '))
        for item in keys:
            check_item(args, item, counts)
    if args.flowers:
        print("FLOWERS".center(45, ' '))
        for item in flowers:
            check_item(args, item, counts)
    if args.soulfire:
        print("SOULFIRE".center(45, ' '))
        for item in soulfire_parts:
            check_item(args, item, counts)
    if args.c.lower() == "cleric":
        print("CLERIC".center(45, ' '))
        for item in cleric_items_to_check:
            check_item(args, item, counts)
        for item in cleric_items_to_count:
            count_item(item, counts)
        if args.gear:
            print("GEAR".center(45, ' '))
            for item in cleric_gear:
                check_item(args, item, counts)
        if args.thurg:
            print("THURG ARMOR".center(45, ' '))
            for item in cleric_thurg:
                check_item(args, item, counts)
    if args.c.lower() == "mage":
        print("MAGE".center(45, ' '))
        for item in mage_items_to_check:
            check_item(args, item, counts)
        for item in mage_items_to_count:
            count_item(item, counts)
    if args.c.lower() == "wiz":
        print("WIZ".center(45, ' '))
        for item in wiz_items_to_count:
            count_item(item, counts)
    if args.c.lower() == "necro":
        print("NECRO".center(45, ' '))
        for item in necro_items_to_count:
            count_item(item, counts)
    if args.c.lower() == "shaman":
        print("SHAMAN".center(45, ' '))
        for item in shaman_items_to_check:
            count_item(item, counts)


def main():
    args = get_args()
    if args.name:
        check_requirements(args)
    else:
        if args.c:
            check_class_bots(args)
        else:
            print("Specify a name or a class, otherwise I have nothing to do.")
            quit(1)
            

if __name__ == '__main__':
    main()
