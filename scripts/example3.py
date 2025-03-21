import os
import sys
import time

# ----------------------------------------------------------------------
# PROGRAM NAME:     example3.py
#
# DESCRIPTION:      Illustrates how to get all head-to-head matchups
# ----------------------------------------------------------------------

# Modify the system path before doing any imports of our specific code
this_file = os.path.abspath(__file__)
examples_root = os.path.dirname(this_file)
project_root = os.path.dirname(examples_root)
src_dir = os.path.join(project_root, "src")
sys.path.append(src_dir)        # So it can find our classes
sys.path.append(project_root)   # So it can find "tests"

# Now python will find our packages
from chess_clubs.club import Club

# Load the test configuration data
from tests import config
club_id = config["club_id"]

# Create and load our test club
club = Club(club_id)

# Print the header for the club, which is the club ID and name
print("\n# ----------------------------------------------------------------------")
print(f"# {str(club)}")
print("# ----------------------------------------------------------------------")

# Get the active players
for i, player in enumerate(club.get_active_players(), 1):
    print(f"{i} {str(player)}")
    
# Load the head-to-head matchups
stime = time.time()
print(f"{stime} Loading head-to-head matchups...")
club.load_head_to_head()
etime = time.time()
print(f"{etime} Done with head-to-head matchups...")
elapsed = etime - stime
print(f"Elapsed time = {elapsed:.2f} seconds")
