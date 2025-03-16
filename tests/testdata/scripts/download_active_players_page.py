import os
import sys
from bs4 import BeautifulSoup
import requests

# ----------------------------------------------------------------------
# This program will download the active players USCF page for this club
# and write it to a file in the testdata directory.
# ----------------------------------------------------------------------

# Patch the system path before importing any of our code
thisfile = os.path.abspath(__file__)
scripts_dir = os.path.dirname(thisfile)
testdata_dir = os.path.dirname(scripts_dir)
tests_dir = os.path.dirname(testdata_dir)
project_root = os.path.dirname(tests_dir)
sys.path.append(project_root)

# Now we can import the tests package
from tests import get_config

# Get the configuration data
config = get_config()
club_id = config["club_id"]

# Using the club_id as the query parameter, get the active players page
url = f"https://www.uschess.org/datapage/top-affil-players.php?affil={club_id}&min=5&Search=Submit"
resp = requests.get(url, timeout=20)
html = resp.text

# Use BeautifulSoup to tidy it up
soup = BeautifulSoup(html, 'html.parser')
html = soup.prettify()

# Write this active players page to the testdata directory
filename = os.path.join(testdata_dir, "active_players.html")
with open(filename, "w") as out:
    print(html, file=out)
