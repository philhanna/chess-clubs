import requests
import re
from bs4 import element
from .player import Player


def get_active_player_list_url(table) -> str:
    link = table.find('a', string="Active Player List")
    url = link.get("href")
    url += "&min=6"
    url += "&Search=Submit"
    return url


def get_club_name(table) -> str:
    """
    Extracts and returns the chess club's name from an HTML table.
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


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a webpage from a given URL.
    """
    response = requests.get(
        url, timeout=20)  # Set a timeout to avoid hanging requests
    response.raise_for_status()  # Raise an error for HTTP error responses (4xx, 5xx)
    return response.text


def get_player(tr: element.Tag) -> Player:
    tds = tr.find_all("td", recursive=False)
    id = tds[1].get_text(strip=True)
    name = tds[3].get_text(strip=True)
    player = Player(id, name)
    return player


def get_third_table(soup) -> element.Tag:
    """
    Extracts and returns the third HTML table from the parsed webpage.
    """
    tables = soup.find_all("table", recursive=True)
    if len(tables) < 3:
        raise ValueError(
            f"Expected at least 3 tables, found {len(tables)}")
    table = tables[2]   # Get the 3rd table
    return table


def format_name(name: str) -> str:
    """Converts a name string into 'Lastname, Firstname' format with specific rules."""

    # Remove any commas or periods
    name = re.sub(r'[,.]', '', name)
    
    # Ensure it is uppercase
    name = name.upper()

    # Recognized suffixes (considered part of last name)
    suffixes = {"JR", "SR", "II", "III", "IV", "V"}

    # Split into parts
    parts = name.split()

    # Identify suffix if present
    suffix = ""
    if parts and parts[-1] in suffixes:
        suffix = parts.pop()  # Remove suffix from the parts list

    # Ensure at least two parts exist
    if len(parts) < 2:
        return name  # If not, return the name as-is

    # First and last name determination
    last_name = parts.pop()
    # Everything else is considered the first name
    first_name = " ".join(parts)

    # Reattach suffix if present
    if suffix:
        last_name += f" {suffix}"

    # Capitalization rules
    def format_part(part: str) -> str:
        part = part.lower().capitalize()  # Convert to lowercase then capitalize
        if part.startswith("Mc") and len(part) > 2:
            part = "Mc" + part[2].upper() + part[3:]
        elif part.startswith("O'") and len(part) > 2:
            part = "O'" + part[2].upper() + part[3:]
        return part

    first_name = format_part(first_name)
    last_name = " ".join(format_part(p) for p in last_name.split())

    return f"{last_name}, {first_name}"
