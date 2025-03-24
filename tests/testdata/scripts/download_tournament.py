#! /usr/bin/python

from bs4 import BeautifulSoup
import requests

TOURNAMENT_ID = "202503213862"
FILENAME = "../tournament.html"

url = f"https://www.uschess.org/msa/XtblMain.php?{TOURNAMENT_ID}"
r = requests.get(url, timeout=20)
r.raise_for_status()
html = r.text
soup = BeautifulSoup(html, 'html.parser')
html_prime = soup.prettify()
with open(FILENAME, "w") as out:
    out.write(html_prime)
    out.write("\n")