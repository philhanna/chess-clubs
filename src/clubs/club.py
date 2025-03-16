from bs4 import BeautifulSoup

from clubs import get_active_player_list_url, get_club_name, get_main_table
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

    def load(self):
        """Fetches and processes the club's details from the US Chess Federation website.

        Retrieves the webpage corresponding to the club's ID, parses the HTML content,
        and extracts relevant information from the third table on the page.
        """
        html = get_page(self.url)
        soup = BeautifulSoup(html, 'html.parser')
        main_table = get_main_table(soup)
        self.name = get_club_name(main_table)
        self.active_players_url = get_active_player_list_url(main_table)

    def __str__(self) -> str:
        parts = []
        parts.append(f'ID="{self.id}"')
        parts.append(f'name="{self.name}"')
        inner = ",".join(parts)
        result = f"Club({inner})"
        return result
