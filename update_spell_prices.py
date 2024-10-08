# Give info on updating spell prices.

import argparse
from datetime import datetime
import os
import re
import sys

today = datetime.today().strftime('%Y-%m-%d')

def get_args():
    """Get arguments from the command line.
    You can update the defaults here, as new versions of these files are
    created, or simply put them on the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prices", "-p",
        default="spell_prices-{}.py".format(today),
        help="The spell prices file from last month"
    )
    parser.add_argument(
        "--counts", "-c",
        default="spell_counts-{}.py".format(today),
        help="The spell counts file, current"
    )
    parser.add_argument(
        "--pigparse", "-i",
        default="pigparsePrices{}.csv".format(today),
        help="The pigparse spell prices file"
    )
    args = parser.parse_args()
    return args


class Spell():
    def __init__(
            self,
            name,
            external=None,
            internal=None,
            count=None,
            pigprice=None,
            pigcount=None):
        self.name = name
        self.internal = internal
        self.external = external
        self.count = count
        self.pigprice = pigprice
        self.pigcount = pigcount

    def __str__(self):
        output = ""
        output = self.name
        if self.external:
            output += ", external=" + str(self.external)
        if self.internal:
            output += ", internal=" + str(self.internal)
        if self.count:
            output += ", count=" + str(self.count)
        if self.pigprice:
            output += ", pigprice=" + str(self.pigprice)
        if self.pigcount:
            output += ", pigcount=" + str(self.pigcount)
        return output


class UpdateSpells():

    def __init__(self, args):

        self.args = args
        self.work = "price_data" + os.sep
        self.spell_dict = {}

        print("\n"*5)
        self.load_prices()
        self.load_counts()
        self.load_pigparse()
        self.out_of_stock()
        self.undercut()
        self.needs_pricing()
        self.too_low()
        print("\n"*5)


    def too_low(self):
        print("\nThe following spells may be priced too low:\n")
        for spell in self.spell_dict.values():
            try:
                if int(spell.external) < float(spell.pigprice) / 2:
                    if int(spell.count) < 10:
                        print(spell)
            except:
                pass


    def needs_pricing(self):
        print("\nThe following spells do not have pricing:\n")
        for spell in self.spell_dict.values():
            try:
                if spell.internal in (None, "None") or spell.external in (None, "None"):
                    if int(spell.count) > 0:
                        print(spell)
            except:
                pass


    def undercut(self):
        print("\nBeing undercut on the following spells, but none in stock:\n")
        for spell in self.spell_dict.values():
            try:
                if float(spell.external) > float(spell.pigprice):
                    if spell.count is None:
                        if int(spell.pigprice) != 0:
                            print(spell)
            except:
                pass
        print("\nBeing undercut on the following spells, but inventory is 2 or less:\n")
        for spell in self.spell_dict.values():
            try:
                if float(spell.external) > float(spell.pigprice):
                    if spell.count in ["1", "2"]:
                        if int(spell.pigprice) != 0:
                            print(spell)
            except:
                pass
        print("\nBeing undercut on the following spells:\n")
        for spell in self.spell_dict.values():
            try:
                if float(spell.external) > float(spell.pigprice):
                    if spell.count is not None and spell.count not in ["1", "2"]:
                        if int(spell.pigprice) != 0:
                            print(spell)
            except:
                pass


    def out_of_stock(self):
        for spell in self.spell_dict.values():
            if spell.count == None:
                if spell.internal and spell.internal != "None":
                    # Means it has a price, but we have no inventory
                    # This won't show up in the final sales output
                    pass
                if spell.external and spell.external != "None":
                    pass


    def load_prices(self):
        with open(self.work + self.args.prices) as prices:
            for line in prices:
                #print(line.strip().split(','))
                try:
                    spell_name = line.split(',')[0].strip('\"')
                except:
                    spell_name = None
                try:
                    external = line.split(',')[1].strip()
                except:
                    external = None
                try:
                    internal = line.split(',')[2].strip()
                except:
                    internal = None
                if spell_name:
                    self.spell_dict[spell_name] = Spell(spell_name, external, internal)


    def load_counts(self):
        with open(self.work + self.args.counts) as counts:
            for line in counts:
                #self.count_list.append(line.split(',')[0])
                try:
                    result = re.search("\'(.*)\'", line)
                    spell_name = result.group(1)
                    #self.count_list.append(result.group(1))
                except:
                    spell_name = None
                try:
                    count = line.strip().split(',')[1].strip(']').strip()
                except:
                    count = None
                if spell_name:
                    spell_name = spell_name.replace("`", "'")
                    if spell_name not in self.spell_dict:
                        print("Warning: " + spell_name + " found in counts, but not in prices.")
                        self.spell_dict[spell_name] = Spell(spell_name, count=count)
                    else:
                        external = self.spell_dict[spell_name].external
                        internal = self.spell_dict[spell_name].internal
                        self.spell_dict[spell_name] = Spell(spell_name, external, internal, count)


    def load_pigparse(self):
        with open(self.work + self.args.pigparse) as pigparse:
            for line in pigparse:
                try:
                    spell_name = line.split(',')[1].split("Spell: ")[1]
                except:
                    spell_name = None
                try:
                    pigprice = line.split(',')[3].strip()
                except:
                    pigprice = None
                try:
                    pigcount = line.split(',')[2].strip()
                except:
                    pigcount = None
                #print(spell_name)
                if spell_name:
                    if spell_name not in self.spell_dict:
                        self.spell_dict[spell_name] = Spell(spell_name, pigprice=pigprice, pigcount=pigcount)
                    else:
                        external = self.spell_dict[spell_name].external
                        internal = self.spell_dict[spell_name].internal
                        count = self.spell_dict[spell_name].count
                        self.spell_dict[spell_name] = Spell(spell_name, external, internal, count, pigprice, pigcount)



def main():
    """Main entry point."""
    args = get_args()
    UpdateSpells(args)


if __name__ == '__main__':
    main()
