from typing import List
from bs4 import BeautifulSoup
from games.game import Game
from util import get_page


def get_head_to_head_url(player_id: str, opponent_id: str) -> str:
    parts = []
    parts.append(f"https://www.uschess.org/datapage/gamestats.php?memid={player_id}")
    parts.append(f"ptype=0")
    parts.append(f"rs=R")
    parts.append(f"drill={opponent_id}")
    url = "&".join(parts)
    return url

class HeadToHead:
    def __init__(self, player_id: str, opponent_id: str):
        
        # Instance variables
        self.player_id: str = player_id
        self.opponent_id: str = opponent_id
        self.games: List[Game] = []
        
        # Get the head to head page
        url = get_head_to_head_url(player_id, opponent_id)
        html = get_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        #with open("/tmp/soup.html", "w") as out: print(soup.prettify(), file=out)
        
        # Loop through the games
        th = soup.find("th", string=lambda text: text and "Event Name" in text)
        tr = th.find_parent("tr")
        while True:
            tr = tr.find_next_sibling("tr")
            if not tr:
                break
            #game = game_from_soup(tr)
            
            
    pass
