from bs4 import element

# This file contains functions that are used in the clubs package.
# These functions are separated from the Club class for better modularity
# and ease of unit testing.

def get_active_player_list_url(main_table, min_games=5) -> str:
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
    url += f"&min={min_games}"
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
        ValueError: If fewer than three tables are found in the HTML.
    """
    tables = soup.find_all("table", recursive=True)
    if len(tables) < 3:
        raise ValueError(f"Expected at least 3 tables, found {len(tables)}")
    
    return tables[2]  # Get the 3rd table

from .club import Club 

# Specify which objects are publicly available when importing this module
__all__ = [
    'Club',    
]
