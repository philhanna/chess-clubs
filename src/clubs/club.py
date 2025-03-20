from bs4 import BeautifulSoup
from typing import Dict, Generator, Tuple
from clubs import get_active_player_list_url, get_club_name, get_main_table
from clubs.head_to_head import HeadToHead
from players import parse_player
from players.player import Player
from util import get_page


class Club:
    """Represents a chess club, identified by its US Chess Federation (USCF) club ID.

    This class allows fetching and parsing club details from the USCF website.
    """

    def __init__(self, id: str):
        """
        Initializes a Club instance.

        Args:
            id (str): The unique identifier of the club from US Chess Federation.
        """
        self.id: str = id
        self.name: str = None
        self.url: str = f"https://www.uschess.org/msa/AffDtlMain.php?{self.id}"
        self.active_players_url: str = None
        self.head_to_head_map: Dict[Tuple[str, str], HeadToHead] = {}
        
        # Fetch and process the club's details from the US Chess
        # Federation website.  Retrieve the webpage corresponding to the
        # club's ID, parse the HTML content, and extract relevant
        # information from the third table on the page.
        
        html = get_page(self.url)
        soup = BeautifulSoup(html, 'html.parser')
        main_table = get_main_table(soup)
        self.name = get_club_name(main_table)
        self.active_players_url = get_active_player_list_url(main_table)


    def get_active_players(self) -> Generator[Player, None, None]:
        """ A generator that returns the active players in this club one at a time. """
        html = get_page(self.active_players_url)
        soup = BeautifulSoup(html, 'html.parser')
        
        # The active player table is the first <table> after the first <h4>
        div = soup.find("h4")
        assert div is not None
        aptable = div.find_next('table')
        assert aptable is not None
        for i, tr in enumerate(aptable.find_all('tr')):
            if i == 0:
                continue    # First row is just column headers
            player = parse_player(tr)
            yield player

        # Done
        pass

    def load_head_to_head(self):
        players = [player for player in self.get_active_players()]
        n = len(players)
        for i in range(n-1):
            player_id = players[i].id
            print(f"{i}. {players[i].name}")
            for j in range(i+1, n):
                opponent_id = players[j].id
                hth = HeadToHead(player_id, opponent_id)
                hth.load()
                if not hth.games:
                    self.head_to_head_map[(player_id, opponent_id)] = None
                    self.head_to_head_map[(opponent_id, player_id)] = None
                else:
                    self.head_to_head_map[(player_id, opponent_id)] = hth
                    self.head_to_head_map[(opponent_id, player_id)] = hth.invert()
        return
    
    def __str__(self) -> str:
        """ Returns a string representation of this object """
        parts = []
        parts.append(f'ID="{self.id}"')
        parts.append(f'name="{self.name}"')
        inner = ",".join(parts)
        result = f"Club({inner})"
        return result
