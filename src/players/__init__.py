from bs4 import BeautifulSoup, element

from util import get_page
from .player import Player

def parse_player(tr: element.Tag) -> Player:
    """
    Creates a Player object from player details found in this &lt;tr&gt;
    """
    tds = tr.find_all("td", recursive=False)
    id = tds[1].get_text(strip=True)
    name = tds[3].get_text(strip=True)
    player = Player(id, name)
    return player

def player_name_from_id(id: str) -> str:
    """ Given a USCF player ID, returns the player's name
    """
    url = f"https://www.uschess.org/msa/thin.php?{id}"
    html = get_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    input_element = soup.find("input", {"name": "memname"})
    name = input_element.get_text().strip() if input_element else ""
    return name