import os
import sys

# ----------------------------------------------------------------------
# PROGRAM NAME:     example2.py
#
# DESCRIPTION:      Illustrates how to find head-to-head results
# ----------------------------------------------------------------------

# Modify the system path before doing any imports of our specific code
this_file = os.path.abspath(__file__)
examples_root = os.path.dirname(this_file)
project_root = os.path.dirname(examples_root)
src_dir = os.path.join(project_root, "src")
sys.path.append(src_dir)        # So it can find our classes
sys.path.append(project_root)   # So it can find "tests"

# Now do our imports
from games.head_to_head import HeadToHead
from games.summary import Summary

# Load the example configuration data
# (modify in config.json as desired)
from tests import config
player_id = config['head_to_head']['player1']
opponent_id = config['head_to_head']['player2']

# Create and load the head-to-head details for these players
obj = HeadToHead(player_id, opponent_id)

# Create an empty summary object
summary = Summary()

# Loop through the games
for game in obj.games:
    print(game)
    summary.games += 1
    if game.result == "W":
        summary.wins += 1
    if game.result == "L":
        summary.losses += 1
    if game.result == "D":
        summary.draws += 1

# Print the summary
print(summary)