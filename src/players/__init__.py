from bs4 import BeautifulSoup, element
from util import get_page
from .player import Player


def parse_player(tr: element.Tag) -> Player:
    """
    Creates a Player object from player details found in this &lt;tr&gt;
    """
    # The rows in the active player table look like this:
    #
    # <tr>
    # 0  <td> 1 </td>
    # 1  <td> <a href="http://msa.uschess.org/MbrDtlMain.php?30420180"> 30420180 </a> </td>
    # 2  <td> <center> 2026-12-31 </center> </td>
    # 3  <td> AVANNI RICHARDSON </td>
    # 4  <td> <center> NC </center> </td>
    # 5  <td> <center> 2020 </center> </td>
    # 6  <td> 2025-03-01 </td>
    # 7  <td> <center> 21 </center> </td>
    # 8  <td> <a href="http://msa.uschess.org/XtblMain.php?202502076302"> 202502076302 </a> </td>
    # </tr>
    tds = tr.find_all("td", recursive=False)

    # Get the player ID and name and create a player object
    id = tds[1].get_text(strip=True)
    name = tds[3].get_text(strip=True)  # The construct will format the name
    player = Player(id, name)

    # Get the player state
    state = tds[4].get_text(strip=True)
    player.state = state

    # Get rating
    rating = tds[5].get_text(strip=True)
    player.rating = rating

    # Get date of rating
    date = tds[6].get_text(strip=True)
    player.date = date

    # Get event count (number of tournaments played in this club)
    event_count = tds[7].get_text(strip=True)
    player.event_count = event_count

    # Get the ID of the last tournament played in this club
    a = tds[8].find("a")
    last_event = a.get_text(strip=True)
    player.last_event = last_event

    # Done
    return player





from bs4 import BeautifulSoup, element
from util import get_page
from .player import Player

def parse_player(tr: element.Tag) -> Player:
    """
    Creates and returns a Player object from a row (<tr>) of an HTML table.
    
    Args:
        tr (element.Tag): A BeautifulSoup Tag object representing a table row
        containing details of an active player.
    
    Returns:
        Player: A Player object populated with extracted data.
    """
    # The rows in the active player table look like this:
    #
    # <tr>
    # 0  <td> 1 </td>
    # 1  <td> <a href="http://msa.uschess.org/MbrDtlMain.php?30420180"> 30420180 </a> </td>
    # 2  <td> <center> 2026-12-31 </center> </td>
    # 3  <td> AVANNI RICHARDSON </td>
    # 4  <td> <center> NC </center> </td>
    # 5  <td> <center> 2020 </center> </td>
    # 6  <td> 2025-03-01 </td>
    # 7  <td> <center> 21 </center> </td>
    # 8  <td> <a href="http://msa.uschess.org/XtblMain.php?202502076302"> 202502076302 </a> </td>
    # </tr>

    # Extract all table cells from the row
    tds = tr.find_all("td", recursive=False)

    # Get the player ID and name, then create a Player object
    id = tds[1].get_text(strip=True)
    name = tds[3].get_text(strip=True)
    player = Player(id, name)

    # Extract additional player attributes
    player.state = tds[4].get_text(strip=True)  # Player's state
    player.rating = tds[5].get_text(strip=True)  # Player's rating
    player.date = tds[6].get_text(strip=True)  # Date of rating
    player.event_count = tds[7].get_text(strip=True)  # Number of tournaments played
    
    # Extract last tournament played
    a = tds[8].find("a")
    player.last_event = a.get_text(strip=True) if a else None
    
    return player

def player_name_from_id(id: str) -> str:
    """
    Retrieves a player's name given their US Chess Federation (USCF) player ID.
    
    Args:
        id (str): The unique USCF player ID.
    
    Returns:
        str: The player's name if found, otherwise an empty string.
    """
    url = f"https://www.uschess.org/msa/thin.php?{id}"
    html = get_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    # Locate the input field containing the player's name
    input_element = soup.find("input", {"name": "memname"})
    return input_element.get_text(strip=True) if input_element else ""
