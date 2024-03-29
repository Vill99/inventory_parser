"""
Questions this script intends to answer:
How many copies of a particular research item do we have?
Which research items do we have less than 1 stack?
Which research items do we have less than x copies?
How many copies of a spell do we have and how many could we craft?
How many copies of each spell do we have?
"""
import argparse

import bot_list
from parse_inventory import get_counts
from research_items.necro_research import necro_spells


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

def main():
    """Main entry point."""
    args = get_args()
    print(args)
    display_resarch(args)
    print(necro_spells)


if __name__ == '__main__':
    main()
