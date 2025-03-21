from typing import List
from bs4 import BeautifulSoup, element
from name_formatter import FormattedName
from chess_clubs import get_page
from chess_clubs.game import Game
from chess_clubs.game_factory import GameFactory
from chess_clubs.summary import Summary

class HeadToHead:
    """
    Represents a head-to-head record between two chess players.
    
    This class fetches and processes game results between a given player
    and an opponent from the US Chess Federation website.
    """

    def __init__(self, player_id: str, opponent_id: str):
        """
        Initializes a HeadToHead instance.
        
        Args:
            player_id (str): The unique identifier of the player.
            opponent_id (str): The unique identifier of the opponent.
        """
        self.player_id: str = player_id
        self.opponent_id: str = opponent_id
        self.games: List[Game] = []
        self.summary: Summary = Summary()

    def load(self):
        """
        Loads head-to-head game data from the US Chess Federation website.
        
        This function retrieves the webpage containing the head-to-head game
        results, extracts relevant data, and populates the list of games and
        summary statistics.
        """
        url = get_head_to_head_url(self.player_id, self.opponent_id)
        html = get_page(url)
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve the player's formatted name
        player_name = get_player_name(soup)
        player_name = FormattedName(player_name).get_last_first()

        # Locate the table header for game results
        th = soup.find("th", string=lambda text: text and "Event Name" in text)
        if th is None:
            return  # No games found

        # Skip the headings row
        tr = th.find_parent("tr")

        # Process each game row
        while True:
            tr = tr.find_next_sibling("tr")
            if not tr or not is_game_row(tr):
                break

            # Parse the game and assign player details
            game = GameFactory.from_soup(tr)
            game.player_id = self.player_id
            game.player_name = player_name

            # Store the game data
            self.games.append(game)
            self.summary.update_with(game)

    def invert(self):
        """
        Swaps player and opponent IDs, inverting the head-to-head perspective.
        
        This function also inverts the summary and game results accordingly.
        """
        self.player_id, self.opponent_id = self.opponent_id, self.player_id
        self.games = [game.invert() for game in self.games]
        self.summary = self.summary.invert()

#   ============================================================
#   Functions
#   ============================================================

def get_head_to_head_url(player_id: str, opponent_id: str) -> str:
    """
    Constructs the URL to retrieve head-to-head game results from USCF.
    
    Args:
        player_id (str): The unique identifier of the player.
        opponent_id (str): The unique identifier of the opponent.
    
    Returns:
        str: The URL pointing to the head-to-head game statistics page.
    """
    url = (f"https://www.uschess.org/datapage/gamestats.php?memid={player_id}"
           f"&ptype=0&rs=R&drill={opponent_id}")
    return url

def get_player_name(soup: BeautifulSoup) -> str:
    """
    Extracts the player's name from the head-to-head game page.
    
    Args:
        soup (BeautifulSoup): Parsed HTML content of the webpage.
    
    Returns:
        str: The player's name in text format.
        None: If the player's name could not be found.
    """
    td = soup.find("td", string=lambda text: text and text.strip() == "Name")
    if not td:
        return None
    return td.find_next_sibling("td").get_text(strip=True)

def is_game_row(tr: element.Tag) -> bool:
    """
    Determines whether a table row corresponds to a game entry.
    
    Args:
        tr (element.Tag): A table row from the parsed HTML.
    
    Returns:
        bool: True if the row contains game data, False otherwise.
    """
    text = tr.find("td").get_text(strip=True)
    return not text.startswith("Search for")
