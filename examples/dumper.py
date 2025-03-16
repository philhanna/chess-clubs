import os
import sys
from bs4 import BeautifulSoup


# ----------------------------------------------------------------------
# PROGRAM NAME:     dumper.py
#
# DESCRIPTION:      Illustrates how to get the club's active players.
# ----------------------------------------------------------------------

# Modify the system path before doing any imports of our specific code
this_file = os.path.abspath(__file__)
examples_root = os.path.dirname(this_file)
project_root = os.path.dirname(examples_root)
src_dir = os.path.join(project_root, "src")
sys.path.append(src_dir)
sys.path.append(project_root)

# Now python will find our packages
from clubs.club import Club
from tests import get_config
from util import get_page

# Load the test configuration data
config = get_config()
club_id = config["club_id"]

# Instantiate and load our test club
club = Club(club_id)
club.load()

# Print the header for the club, which is the club ID and name
print("\n# ----------------------------------------------------------------------")
print(f"# {str(club)}")
print("# ----------------------------------------------------------------------")

# Get the active players
for i, player in enumerate(club.active_players(), 1):
    print(f"{i} {str(player)}")