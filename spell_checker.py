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
from spellbooks.P99Spells import spells





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
        choices=["Classic", "Kunark", "Velious", "Chardok 2.0"],
        help="Latest era to look for spells."
    )
    args = parser.parse_args()
    return args


def main():
    """Main entry point."""
    args = get_args()
    #SpellChecker(args)
    print(args)


if __name__ == "__main__":
    main()
