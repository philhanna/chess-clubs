
# Modify the system path before doing any imports of our specific code
import os
import sys


this_file = os.path.abspath(__file__)
examples_root = os.path.dirname(this_file)
project_root = os.path.dirname(examples_root)
src_dir = os.path.join(project_root, "src")
sys.path.append(src_dir)
sys.path.append(project_root)
from games.head_to_head import HeadToHead


player_id = "12910923"
opponent_id = "12877028"
obj = HeadToHead(player_id, opponent_id)
for game in obj.games:
    print(game)