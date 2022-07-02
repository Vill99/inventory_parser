"""Spell Checker

Open a spellbook text file.
Determine the class based on the spells contained. If not enough spells to
determine the class, just output an error.
A Max level can be specified as a parameter.

Parameters are Name, Level and Era.

If no Name is specified, it will query all spellbooks in the directory.
If no level is specified, it will assume level 60.
If no era is specified, it will assume the latest.

"""

import argparse
import os

from intrange.intrange import IntRange
from spellbooks.P99Spells import p99spells
from spellbooks.spellbook import SpellBook


ERA_LIST = [
    "Classic",
    "Fear",
    "Sky",
    "Paineel",
    "Kunark",
    "Hole",
    "Velious",
    "Warrens",
    "Chardok 2.0",
    "Surefall Glade"
]


def get_args():
    """Get arguments from the command line."""
    parser = argparse.ArgumentParser(
        description='Search spellbook files for missing spells.'
    )
    parser.add_argument(
        "--level",
        "-l",
        help="The level of the toon",
        default=60,
        type=IntRange(1, 60)
    )
    parser.add_argument(
        "--name",
        "-n",
        help="""Name of the toon. If no name is specified, will look at all
        Spellbook files in the current directory"""
    )
    parser.add_argument(
        "--era",
        "-e",
        default="Surefall Glade",
        choices=ERA_LIST,
        help="Latest era to look for spells."
    )
    args = parser.parse_args()
    return args


def determine_class(spell_book):
    """Given a spell_book, determine the class of the owner."""
    for spell in spell_book.spell_list:
        found = 0
        for p99spell in p99spells:
            if spell.name == p99spell["Name"]:
                found += 1
                # print(spell.name)
                # print(p99spell["Class"])
                character_class = p99spell["Class"]
        if found == 1:
            return character_class
    print("Unable to determine class.")
    quit(3)


def find_missing(spell_book, args, character_class):
    """Find all the missing spells."""
    for p99spell in p99spells:
        if p99spell["Class"] == character_class:
            if p99spell["Level"] <= args.level:
                if ERA_LIST.index(p99spell["Era"]) <= ERA_LIST.index(args.era):
                    found = False
                    for spell in spell_book.spell_list:
                        if spell.name == p99spell["Name"]:
                            found = True
                    if not found:
                        print(str(p99spell["Level"]) + " " + p99spell["Name"])


def get_spellbooks(args):
    spell_book_list = []
    file_list = os.listdir(".")
    for filename in file_list:
        if filename.endswith("-Spellbook.txt"):
            args.name = filename[:filename.find('-')]
            print("*" * 80)
            print(args.name)
            print("")
            check_spellbook(args)


def check_spellbook(args):
    spell_book = SpellBook(args)
    character_class = determine_class(spell_book)
    find_missing(spell_book, args, character_class)


def main():
    """Main entry point."""
    args = get_args()
    if args.name:
        check_spellbook(args)
    else:
        spell_book_list = get_spellbooks(args)



if __name__ == "__main__":
    main()
