import requests
from bs4 import BeautifulSoup, element


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

    def __str__(self) -> str:
        parts = []
        parts.append(f'ID="{self.id}"')
        parts.append(f'name="{self.name}"')
        parts.append(f'url="{self.url}"')
        inner = ",".join(parts)
        result = f"Club({inner})"
        return result
    
    def get_active_player_list_url(self, table) -> str:
        link = table.find('a', string="Active Player List")
        url = link.get("href")
        return url
    
    def get_club_name(self, table) -> str:
        """
        Extracts and returns the chess club's name from an HTML table.

        Args:
            table (element.Tag): The HTML table containing the club details.

        Returns:
            str: The extracted name of the chess club.

        Raises:
            ValueError: If the expected font tag with size "+1" is not found,
                        or if the extracted text does not contain a colon
                        (":") to split the ID and name.
        """
        tag = table.find("font", {"size": "+1"})
        if not tag:
            errmsg = "No <font size=+1> tag found"
            raise ValueError(errmsg)

        text = tag.get_text(strip=True)
        id_part, name_part = text.split(":", 1)
        id_part = id_part.strip()

        name_part = name_part.strip()
        return name_part

    def get_3rd_table(self, soup) -> element.Tag:
        """
        Extracts and returns the third HTML table from the parsed webpage.

        Args:
            soup (BeautifulSoup): The parsed HTML document.

        Returns:
            element.Tag: The third table in the HTML structure.

        Raises:
            ValueError: If fewer than three tables are found in the HTML document.
        """
        tables = soup.find_all("table", recursive=True)
        if len(tables) < 3:
            raise ValueError(
                f"Expected at least 3 tables, found {len(tables)}")
        table = tables[2]   # Get the 3rd table
        return table

    def load(self):
        """Fetches and processes the club's details from the US Chess Federation website.

        Retrieves the webpage corresponding to the club's ID, parses the HTML content,
        and extracts relevant information from the third table on the page.
        """
        url = f"https://www.uschess.org/msa/AffDtlMain.php?{self.id}"
        html = Club.get(url)
        soup = BeautifulSoup(html, 'html.parser')
        table3 = self.get_3rd_table(soup)
        self.name = self.get_club_name(table3)
        self.url = self.get_active_player_list_url(table3)

    # ------------------------------------------------------------------
    # Static methods
    # ------------------------------------------------------------------

    @staticmethod
    def get(url: str) -> str:
        """
        Fetches the HTML content of a webpage from a given URL.

        Args:
            url (str): The URL to retrieve.

        Returns:
            str: The HTML content of the fetched webpage.

        Raises:
            requests.exceptions.RequestException: If the request encounters an HTTP error or timeout.
        """
        response = requests.get(
            url, timeout=20)  # Set a timeout to avoid hanging requests
        response.raise_for_status()  # Raise an error for HTTP error responses (4xx, 5xx)
        return response.text
