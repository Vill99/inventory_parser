"""
Questions this script intends to answer:
How many copies of a particular research item do we have?
Which research items do we have less than 1 stack?
Which research items do we have less than x copies?
How many copies of a spell do we have and how many could we craft?
How many copies of each spell do we have?
"""
import argparse
import os
import re

import mule_list
from parse_inventory import get_counts
from parse_spell_mules import create_spell_dict
from research_items.necro_research import necro_spells


inventory_path = ".." + os.sep + "equi" + os.sep


def get_args():
    """Get arguments from the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--item", "-i",
        help="Count a particular item"
    )
    parser.add_argument(
        "--spell", "-s",
        help="Count a particular spell, and calclulate how many we can craft."
    )
    parser.add_argument(
        "--number", "-n",
        action='store_true',
        help="Count every spell"
    )
    parser.add_argument(
        "-c",
        choices=["all", "enchanter", "mage", "necro", "wiz"],
        default="all",
        help="Limit to one class"
    )
    parser.add_argument(
        "--low_inventory", "-l",
        default=3,
        type=int,
        help="Display all the research items that are low."
    )
    args = parser.parse_args()
    return args


def display_item(item):
    """
    Display the count of a particular item.
    """
    
    print()

def display_spell(spell):
    """
    Display the count of a particular spell.
    Determine how many copies could be researched from materials.
    """
    print()

def display_spell_counts(character_class):
    """
    Display the counts for each research spell.
    """
    print()

def display_low_inventory(minimum, character_class):
    """
    Display any research items with less than the minimum.
    """
    print()


def display_resarch(args):
    """
    Conditionally display the research inventory info based on the
    arguments provided.
    """
    if args.item is not None:
        display_item(args.item)
    if args.spell is not None:
        display_spell(args.spell)
    if args.number:
        display_spell_counts(args.c)
    display_low_inventory(args.low_inventory, args.c)

def build_counts():
    """
    Need to count up all the research items and spells available on 
    the bots.
    """
    master_research_list = []
    research_dict = {}
    for mule in mule_list.research_mules:
        research_items = get_items(mule, master_research_list)
        
    return research_dict

def is_research(item, research_list):
    """Returns True if the item is a research item."""


    return False

def get_items(mule_name, research_list):
    """
    Get the research items from a particular mule and add them to 
    the research_list.
    """
    file_name = inventory_path + mule_name + "-Inventory.txt"
    research_list = []
    try:
        with open(file_name) as inventory:
            for line in inventory:
                split_line = re.split(r'\t+', line.rstrip('\t'))

                
                if is_research(split_line[1], research_list):
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
    return research_list

def main():
    """Main entry point."""
    args = get_args()
    #print(args)
    spell_dict = create_spell_dict()
    research_dict = build_counts()
    display_resarch(args)


if __name__ == '__main__':
    main()
