from bs4 import BeautifulSoup, element
from name_formatter import FormattedName

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

def player_name_from_id(id: str) -> str:
    """ Given a USCF player ID, returns the player's name
    """
    url = f"https://www.uschess.org/msa/thin.php?{id}"
    html = get_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    input_element = soup.find("input", {"name": "memname"})
    name = input_element.get_text().strip() if input_element else ""
    return name
