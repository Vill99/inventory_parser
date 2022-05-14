"""Spell Checker

Open a spellbook text file.
Determine the class based on the spells contained. If not enough spells to
determine the class, just output an error.
Up to the max level spell in the book, show all the missing spells.
A Max level to check for can be specified as a parameter.

For a batch, do the same routine against either all Spellbook text files, or
specify a list on the command line.

"""

import argparse

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
    "Chardok 2.0"
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
        default="Chardok 2.0",
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
            found = False
            for spell in spell_book.spell_list:
                if spell.name == p99spell["Name"]:
                    found = True
            if not found:
                print(p99spell["Name"])
    # print(args)

def main():
    """Main entry point."""
    args = get_args()
    spell_book = SpellBook(args)
    character_class = determine_class(spell_book)
    find_missing(spell_book, args, character_class)


if __name__ == "__main__":
    main()
