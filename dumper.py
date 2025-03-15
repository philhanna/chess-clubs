#! /usr/bin/python

import os
import sys

from bs4 import BeautifulSoup


project_root = os.path.dirname(os.path.abspath(__file__))
packages_dir = os.path.join(project_root, "src")
sys.path.append(packages_dir)

from chess_clubs import get_page, parse_player, get_third_table
from chess_clubs.club import Club


club = Club("A6021250")
club.load()
print(club)

html = get_page(club.url)
soup = BeautifulSoup(html, 'html.parser')
table = get_third_table(soup)
with open("dump.html", "w") as out:
    print(table.prettify(), file=out)
    
# Dump the <th> children of the table
print("Column headings")
for th in table.find("tr").find_all("th", recursive=False):
    print(th.get_text().strip())
    
# Get the individual players
for i, tr in enumerate(table.find_all("tr", recursive=False)):
    if i == 0:
        continue    # skip the first row - headings
    player = parse_player(tr)
    print(f"{i}. {str(player)}")
    
