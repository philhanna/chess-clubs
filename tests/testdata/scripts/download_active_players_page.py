import os
from bs4 import BeautifulSoup
import requests

# This program will download the active players USCF page for this club
# and write it to a file in the testdata directory.

# Get the ID of the club to be used for testing.  It is in the
# testdata/club_id file.  testdata is ../../testdata
testdata = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
club_id_path = os.path.join(testdata, "club_id")
with open(club_id_path) as fp:
    club_id = fp.read()
    
# Using the club_id as the query parameter, get the active players page
url = f"https://www.uschess.org/datapage/top-affil-players.php?affil={club_id}&min=6&Search=Submit"
resp = requests.get(url, timeout=20)
html = resp.text

# Use BeautifulSoup to tidy it up
soup = BeautifulSoup(html, 'html.parser')
html = soup.prettify()

# Write this main page to the testdata directory
filename = os.path.join(testdata, "active_players.html")
with open(filename, "w") as out:
    print(html, file=out)
