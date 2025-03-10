import requests
from bs4 import BeautifulSoup

class Club:
    """ Represents a chess club """
    def __init__(self, id: str, name: str = None):
        self.id: str = id
        self.name: str = name
        
    def load(self):
        url = f"https://www.uschess.org/msa/AffDtlMain.php?{self.id}"
        html = Club.get(url)
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all("table", recursive=True)
        if len(tables) < 3:
            raise ValueError(f"Expected at least 3 tables, found {len(tables)}")
        table = tables[2]   # Get the 3rd table
    
    @staticmethod
    def get(url: str) -> str:
        """ Gets the contents of the specified url from the network """
        response = requests.get(url, timeout=20)  # Set a timeout to avoid hanging requests
        response.raise_for_status()  # Raise an error for HTTP error responses (4xx, 5xx)
        return response.text
