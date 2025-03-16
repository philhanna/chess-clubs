from bs4 import element

# This file contains functions that are called in the clubs package.
# They are split out here from the Club class for ease of unit testing.


def get_active_player_list_url(main_table) -> str:
    """
    Creates the URL that can be used to retrieve the active player list.
    This URL will add a filter to include only those players with
    at least six games with this club.
    """
    link = main_table.find('a', string="Active Player List")
    url = link.get("href")
    url += "&min=6"
    url += "&Search=Submit"
    return url


def get_club_name(main_table) -> str:
    """
    Extracts and returns the chess club's name from an HTML table.
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
    """
    tables = soup.find_all("table", recursive=True)
    if len(tables) < 3:
        raise ValueError(
            f"Expected at least 3 tables, found {len(tables)}")
    table = tables[2]   # Get the 3rd table
    return table

from .club import Club 

__all__ = [
    'Club',    
]