# inventory_parser
Simple scripts for parsing Everquest inventory files

### output_spell_auction.py
This is the main script that outputs the auction script.
You will need to create the following 3 files and put them in price_data:

unixgeekSpellPricesYYYY-MM-DD.csv

spell_counts-YYYY-MM-DD.py

spell_prices-YYYY-MM-DD.py


Instructions for doing so, are a little weak, but found in the actual script

### update_spell_prices.py
You will need to update the script itself with the latest versions of spell data.
It will give you hints as to mispriced auctions

### parse_inventory.py 
This script will read the inventory for a single toon, and output a list of the items they are holding. 
It looks in the current directory for the Inventory.txt file
You can import the script and use the *get_inventory* function to return a list of items

### parse_sky_mules.py
This script parses all the sky mules, which are specified in **mule_list.py**, it will output a list of
inventories that can be copy pasted into the skymules google sheet, and then adjusted to track all sky
items. It should be run once the sheet stops reflecting the inventories accurately.

### parse_spell_mules.py
This script will print out a list of all the spells in the inventories and their counts. Then it will sort
them by class and print out each classes spells.

### spell_checker.py
This script will check a character's spellbook and list the missing spells.



