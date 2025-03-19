
import os
import sys

# Modify the system path before doing any imports of our specific code
this_file = os.path.abspath(__file__)
examples_root = os.path.dirname(this_file)
project_root = os.path.dirname(examples_root)
src_dir = os.path.join(project_root, "src")
sys.path.append(src_dir)

# Now do our imports
from games.head_to_head import HeadToHead


player_id = "12910923"
opponent_id = "13214962"
obj = HeadToHead(player_id, opponent_id)
for game in obj.games:
    print(game)