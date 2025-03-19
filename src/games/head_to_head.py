from typing import List
from bs4 import BeautifulSoup, element
from name_formatter import FormattedName
from games.game import Game
from games.game_factory import GameFactory
from games.summary import Summary
from util import get_page


class HeadToHead:
    def __init__(self, player_id: str, opponent_id: str):
        # Instance variables
        self.player_id: str = player_id
        self.opponent_id: str = opponent_id
        self.games: List[Game] = []
        self.summary: Summary = Summary()

        # Get the head to head page
        url = get_head_to_head_url(player_id, opponent_id)
        html = get_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        # with open("/tmp/soup.html", "w") as fp: print(soup.prettify(), file=fp)

        # Get the player name
        player_name = get_player_name(soup)
        player_name = FormattedName(player_name).get_last_first()

        # See if there are any head-to-head games
        th = soup.find("th", string=lambda text: text and "Event Name" in text)
        if th is None:
            return
        tr = th.find_parent("tr")   # Skip the heading row

        # Loop through the games
        while True:

            # Get next row.  If no more, or if this is the "Search for"
            # row, we are done
            tr = tr.find_next_sibling("tr")
            if not tr or not is_game_row(tr):
                break

            # Parse the game
            game = GameFactory.from_soup(tr)

            # Add the player ID and name
            game.player_id = player_id
            game.player_name = player_name

            # Add it to the list
            self.games.append(game)

            # Update the summary
            self.summary.add(game)
            
        # Done
        return



#   ============================================================
#   Functions
#   ============================================================


def get_head_to_head_url(player_id: str, opponent_id: str) -> str:
    parts = []
    parts.append(
        f"https://www.uschess.org/datapage/gamestats.php?memid={player_id}")
    parts.append(f"ptype=0")
    parts.append(f"rs=R")
    parts.append(f"drill={opponent_id}")
    url = "&".join(parts)
    return url


def is_game_row(tr: element.Tag) -> bool:
    text = tr.find("td").get_text(strip=True)
    done = text.startswith("Search for")
    return not done


def get_player_name(soup: BeautifulSoup) -> str:
    td = soup.find("td", string=lambda text: text and text.strip() == "Name")
    if not td:
        return None
    td = td.find_next_sibling("td")
    result = td.get_text(strip=True)
    return result
