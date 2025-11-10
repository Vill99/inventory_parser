"""This script will copy the most recent pricing data to today's date
"""
import os
import re
import shutil
from datetime import datetime

# Pattern: spell_prices-YYYY-MM-DD.py
pattern = re.compile(r"spell_prices-(\d{4})-(\d{2})-(\d{2})\.py")

files = [f for f in os.listdir('price_data') if pattern.match(f)]

if not files:
    print("No matching files found.")
    exit(1)

# Extract date from filename and find the newest
dated_files = []
for f in files:
    match = pattern.match(f)
    if match:
        year, month, day = match.groups()
        file_date = datetime(int(year), int(month), int(day))
        dated_files.append((file_date, f))

# Get the latest file
latest_date, latest_file = max(dated_files, key=lambda x: x[0])

# Create new filename with today's date
today = datetime.today().strftime("%Y-%m-%d")
new_filename = f"spell_prices-{today}.py"

# Copy
if latest_file == new_filename:
    print("Today's file already exists")
else:
    shutil.copy('price_data' + os.sep + latest_file, 
                'price_data' + os.sep + new_filename)

    print(f"Copied {latest_file} → {new_filename}")


