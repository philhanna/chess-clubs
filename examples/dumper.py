import os
import sys
from bs4 import BeautifulSoup

this_file = os.path.abspath(__file__)
examples_root = os.path.dirname(this_file)
project_root = os.path.dirname(examples_root)
packages_dir = os.path.join(project_root, "src")
sys.path.append(packages_dir)
print("DEBUG: System path is:")
for token in sys.path:
    print(f"\t{token}")
from chess_clubs.club import Club
from chess_clubs import get_page, parse_player, get_main_table

club = Club("A6021250")
club.load()
print(club)

html = get_page(club.url)
soup = BeautifulSoup(html, 'html.parser')
main_table = get_main_table(soup)

# Get the individual players
for i, tr in enumerate(main_table.find_all("tr", recursive=False)):
    if i == 0:
        continue    # skip the first row - headings
    player = parse_player(tr)
    print(f"{i}. {str(player)}")
