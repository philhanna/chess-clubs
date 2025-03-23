import re
from typing import List

from bs4 import BeautifulSoup
from chess_clubs import get_head_to_head_url, get_page
from chess_clubs.game import Game
from chess_clubs.game_factory import GameFactory


class HeadToHead:
    """
    Collects games for a specified pair of opponents
    """

    def __init__(self, player_id: str, opponent_id: str):
        self.player_id: str = player_id
        self.opponent_id: str = opponent_id
        self.games: List[Game] = []
        
        # Get the HTML of the head-to-head matchup page
        html = self.get_html()
        soup = BeautifulSoup(html, 'html.parser')
        
        # Navigate to where the rows should be
        links = soup.find_all("a", href=re.compile("XtblMain"))
        for link in links:
            tr = link.find_parent("tr")
            game = GameFactory.from_soup(self.player_id, tr)
            self.games.append(game)

    def get_html(self) -> str:
        url = get_head_to_head_url(self.player_id, self.opponent_id)
        html = get_page(url)
        return html
    
    pass
