import os
import sys
from bs4 import BeautifulSoup

# Modify the system path before doing any imports of my code

this_file = os.path.abspath(__file__)
examples_root = os.path.dirname(this_file)
project_root = os.path.dirname(examples_root)
src_dir = os.path.join(project_root, "src")
tests_dir = os.path.join(project_root, "tests")
sys.path.append(src_dir)
sys.path.append(tests_dir)

# Now python will find our packages


from clubs.club import Club
from players import parse_player
from clubs import get_main_table
from util import get_page
from tests.testdata import TESTDATA


# Instantiate our test club

jsonfile = os.path.join(TESTDATA, "config.json")
print(f"DEBUG: {jsonfile=}")

club = Club("A6021250")
club.load()
print(club)

html = get_page(club.url)
soup = BeautifulSoup(html, 'html.parser')
main_table = get_main_table(soup)
with open("../tests/testdata/main_table.html", "w") as fp:
    print(main_table.prettify(), file=fp)

# Get the individual players
for i, tr in enumerate(main_table.find_all("tr", recursive=False)):
    print(f"DEBUG: {i=}\n{tr.prettify()}")
    if i == 0:
        continue    # skip the first row - headings
    player = parse_player(tr)
    print(f"{i}. {str(player)}")
