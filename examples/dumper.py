import os
import sys

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
from tests import config
from clubs.club import Club

# Load the test configuration data
club_id = config["club_id"]

# Create and load our test club
club = Club(club_id)

# Print the header for the club, which is the club ID and name
print("\n# ----------------------------------------------------------------------")
print(f"# {str(club)}")
print("# ----------------------------------------------------------------------")

# Get the active players
for i, player in enumerate(club.active_players(), 1):
    print(f"{i} {str(player)}")
