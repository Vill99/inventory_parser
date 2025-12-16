cd ~/Code/inventory_parser/scraper
python get_pigparse_data.py
# check errors
cd ~/Code/inventory_parser
python parse_spell_mules.py -o -c
# check errors
python copy_latest_prices.py
# check errors
python update_spell_prices.py
# check errors
if [ $? -eq 0 ]; then
    python output_spell_auction.py external
else
    echo Fix all the issues, then run output_spell_auction.py external
fi
