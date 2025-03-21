import time
from bs4 import BeautifulSoup, element
import requests

from chess_clubs.config import load_config
from chess_clubs.player import Player

config = load_config()

def get_active_player_list_url(main_table, MIN_GAMES=config.app.MIN_GAMES) -> str:
    """
    Constructs the URL for retrieving the active player list.

    This function finds the appropriate link in the given HTML table and
    modifies the URL to include a filter for players with a minimum number
    of games.

    Args:
        main_table: The BeautifulSoup tag representing the main HTML table.
        min_games (int, optional): The minimum number of games required to be considered active. Defaults to 5.

    Returns:
        str: The constructed URL with the appropriate filter parameters.
    """
    link = main_table.find('a', string="Active Player List")
    url = link.get("href")
    url += f"&min={MIN_GAMES}"
    url += "&Search=Submit"
    return url


def get_club_name(main_table) -> str:
    """
    Extracts the chess club's name from an HTML table.

    Args:
        main_table: The BeautifulSoup tag representing the main HTML table.

    Returns:
        str: The name of the club.

    Raises:
        ValueError: If the expected font tag is not found in the table.
    """
    tag = main_table.find("font", {"size": "+1"})
    if not tag:
        errmsg = "No <font size=+1> tag found"
        raise ValueError(errmsg)

    text = tag.get_text(strip=True)
    id_part, name_part = text.split(":", 1)
    id_part = id_part.strip()
    name_part = name_part.strip()
    return name_part


def get_main_table(soup) -> element.Tag:
    """
    Extracts and returns the third HTML table from the parsed webpage.

    Args:
        soup: The BeautifulSoup object representing the parsed HTML page.

    Returns:
        element.Tag: The third HTML table found in the document.

    Raises:
        AssertionError: If fewer than three tables are found in the HTML.
    """
    tables = soup.find_all("table", recursive=True)
    assert len(tables) >= 3, f"Expected at least 3 tables, found {len(tables)}"
    return tables[2]  # Get the 3rd table


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a webpage from a given URL, retrying on timeout errors.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        str: The HTML content of the requested webpage.

    Raises:
        requests.exceptions.RequestException: If the request encounters an error.
    """
    config = load_config()
    MAX_ATTEMPTS = config.net.MAX_ATTEMPTS
    TIMEOUT = config.net.TIMEOUT
    RETRY_DELAY = config.net.RETRY_DELAY

    for attempt in range(MAX_ATTEMPTS):
        try:
            # Attempt to fetch the page
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.text
        except requests.exceptions.Timeout:
            if attempt < MAX_ATTEMPTS - 1:
                # If a timeout occurs and attempts are remaining, retry
                print(
                    f"Timeout occurred, retrying... ({attempt + 1}/{MAX_ATTEMPTS})")
                time.sleep(RETRY_DELAY)
            else:
                # Raise the exception after the last attempt
                raise
        except requests.exceptions.RequestException as e:
            # For any other request exception, raise it immediately
            raise e


def invert_color(color: str) -> str:
    """
    Inverts the color played in a game.

    Args:
        color (str): "W" for White or "B" for Black.

    Returns:
        str: "B" if input was "W", "W" if input was "B", otherwise unchanged.
    """
    if color and color == "W":
        return "B"
    if color and color == "B":
        return "W"
    return color


def invert_result(result: str) -> str:
    """
    Inverts the game result perspective.

    Args:
        result (str): "W" for win, "L" for loss, "D" for draw.

    Returns:
        str: "L" if input was "W", "W" if input was "L", otherwise unchanged.
    """
    if result and result == "W":
        return "L"
    if result and result == "L":
        return "W"
    return result


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
    player.event_count = tds[7].get_text(
        strip=True)  # Number of tournaments played

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
    if not input_element:
        return ""
    name = input_element.get("value")
    return name.strip()
