"""
Find an item on the mules. display which toons have it, and which login
they are on. Rather than post repeats, just show a count too.
"""
import argparse
import glob
import os
import subprocess
import sys
from collections import defaultdict

from mule_list import account_dict


def get_args():
    """Get arguments from the command line.
    retuired args
        - item name

    optional args
        - everquest directory

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "item",
        help="The item you are searching for."
    )
    parser.add_argument(
        "--eqdir", "-e",
        default=".",
        help="The Everquest directory to search inventory files in."
    )
    args = parser.parse_args()
    return args


def find_item(args):
    """
    Find the items in the Inventory files.
    """
    files = glob.glob(args.eqdir + os.sep + "*-Inventory.txt")
    if files:
        result = subprocess.run(
            ["grep", args.item] + files,
            capture_output=True,
            text=True
        )
        if result.returncode:
            print("Return code:", result.returncode)
        #print(result.stdout)
        if result.returncode == 1:
            print("No results were found")
            print("Errors:")
            print(result.stderr)
            sys.exit(1)
        if result.returncode:
            print("Errors:")
            print(result.stderr)
            sys.exit(result.returncode1)
    else:
        print("No files were found")
        print("We are looking for files ending in '-Inventory.txt' here:")
        print(args.eqdir)
        sys.exit(2)
    return result.stdout


def format_results(results):
    """
    Make the output nice, and only show the pertinent info.
    """
    counts = defaultdict(int)
    item_name = None
    for line in results.strip().splitlines():
        parts = line.split("\t")
        # Example parts[0] = /Users/josh/.../Pokewell-Inventory.txt:Bank5-Slot3
        # Extract file name only
        filename = os.path.basename(parts[0])
        char_name = filename.split("-Inventory")[0]
        # Extract item name
        if item_name is None:
            item_name = parts[1]  # "Spell: Heroic Bond"
        if item_name == parts[1]:
            counts[char_name] += 1
    lines = []
    for name, count in counts.items():
        account = lookup(name)
        if account:
            lines.append(f"{name} - ({account}) - {count}")
        else:
            lines.append(f"{name} - {count}")
    return(item_name, lines)


def lookup(name):
    """
    Given a toon name, lookup the account it's on.
    """

    for key, values in account_dict.items():
        if name in values:
            return(key)
            break


def main():
    """Main entry point."""
    args = get_args()
    results = find_item(args)
    # TODO clean up this output
    # currently it's directly the grep output
    item_name, lines = format_results(results)
    print(item_name)
    for line in lines:
        print(line)


if __name__ == '__main__':
    main()
