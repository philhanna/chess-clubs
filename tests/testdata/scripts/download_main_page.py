import os
import json
from bs4 import BeautifulSoup
import requests

# This program will download the active players USCF page for this club
# and write it to a file in the testdata directory.

# Get the testdata directory
testdata = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(testdata, "config.json")

# Read the JSON configuration file
with open(config_path, "r") as fp:
    config = json.load(fp)
    club_id = config["club_id"]
    
print(f"DEBUG: {club_id=}")
    
# Using the club_id as the query parameter, get the active players page
url = f"https://www.uschess.org/datapage/top-affil-players.php?affil={club_id}&min=6&Search=Submit"
print(f"DEBUG: {url=}")
resp = requests.get(url, timeout=20)
html = resp.text

# Use BeautifulSoup to tidy it up
soup = BeautifulSoup(html, 'html.parser')
html = soup.prettify()

# Write this main page to the testdata directory
filename = os.path.join(testdata, "main.html")
with open(filename, "w") as out:
    print(html, file=out)
