from bs4 import BeautifulSoup
import chess_clubs


class Club:
    """Represents a chess club, identified by its US Chess Federation (USCF) club ID.

    This class allows fetching and parsing club details from the USCF website.
    """

    def __init__(self, id: str):
        """
        Initializes a Club instance.

        Args:
            id (str): The unique identifier of the club from US Chess Federation.
            name (str, optional): The name of the club. Defaults to None.
        """
        self.id: str = id
        self.name: str = None
        self.url: str = None

    def load(self):
        """Fetches and processes the club's details from the US Chess Federation website.

        Retrieves the webpage corresponding to the club's ID, parses the HTML content,
        and extracts relevant information from the third table on the page.
        """
        url = f"https://www.uschess.org/msa/AffDtlMain.php?{self.id}"
        html = chess_clubs.get_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        main_table = chess_clubs.get_main_table(soup)
        self.name = chess_clubs.get_club_name(main_table)
        self.url = chess_clubs.get_active_player_list_url(main_table)

    def __str__(self) -> str:
        parts = []
        parts.append(f'ID="{self.id}"')
        parts.append(f'name="{self.name}"')
        parts.append(f'url="{self.url}"')
        inner = ",".join(parts)
        result = f"Club({inner})"
        return result
