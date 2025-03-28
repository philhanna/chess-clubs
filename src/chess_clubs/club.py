from bs4 import BeautifulSoup
from typing import Dict, Generator, Tuple

from chess_clubs import get_active_player_list_url, get_club_name, get_main_table, get_page, parse_player
from chess_clubs.player import Player

class Club:
    """
    Represents a chess club, identified by its US Chess Federation (USCF) club ID.

    This class fetches and processes club details from the US Chess Federation website,
    including club name, active players, and head-to-head results.
    """

    def __init__(self, id: str):
        """
        Initializes a Club instance by retrieving and parsing club information from USCF.

        Args:
            id (str): The unique identifier of the club from the US Chess Federation.
        """
        self.id: str = id
        self.name: str = None
        self.url: str = f"https://www.uschess.org/msa/AffDtlMain.php?{self.id}"
        self.active_players_url: str = None
        
        # Fetch and parse the club's webpage to extract relevant information
        html = get_page(self.url)
        soup = BeautifulSoup(html, 'html.parser')
        main_table = get_main_table(soup)
        self.name = get_club_name(main_table)
        self.active_players_url = get_active_player_list_url(main_table)

    def get_active_players(self) -> Generator[Player, None, None]:
        """
        Generator function that retrieves the active players from the club.

        Returns:
            Generator[Player, None, None]: A generator yielding Player objects.
        """
        html = get_page(self.active_players_url)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Locate the active player table, which appears after the first <h4> tag
        div = soup.find("h4")
        assert div is not None, "Expected an <h4> tag before the active player table."
        aptable = div.find_next('table')
        assert aptable is not None, "Expected a table following the <h4> tag."
        
        for i, tr in enumerate(aptable.find_all('tr')):
            if i == 0:
                continue  # Skip header row

            player = parse_player(tr)
            yield player
        
    def __str__(self) -> str:
        """
        Returns a string representation of the Club instance.

        Returns:
            str: A formatted string containing club ID and name.
        """
        parts = [
            f'ID="{self.id}"',
            f'name="{self.name}"'
        ]
        return f"Club({','.join(parts)})"

