import re
from bs4 import element


class Game:
    def __init__(self):
        self.tname: str = None      # Tournament name
        self.tid: str = None        # Tournament ID
        self.tdate: str = None      # Tournament date
        self.sname: str = None      # Section name
        self.rnumber: int = None    # Round number

def game_from_soup(tr: element.Tag) -> Game:
    # Create an empty Game object
    game = Game()

    # Parse the <tr> for the game attributes
    tds = tr.find_all("td")
    if len(tds) < 8:
        errmsg = f"Expected 8 <td> elements, found {len(tds)}"
        raise RuntimeError(errmsg)
    parse_first_td(game, tds[0])    # Tournament name, ID, and date
    parse_second_td(game, tds[1])   # Section name
    parse_third_td(game, tds[2])    # Round
    parse_fourth_td(game, tds[3])   # Color

    # Done
    return game

def parse_first_td(game: Game, td: element.Tag):
    """ Extracts the tournament name, ID, and date and stores them in
    instance variables.
    
    The cell contains:
    <td>
        <a href="http://msa.uschess.org/XtblMain.php?202412219692">
            ADULT AND YOUTH BEFORE CHRISTMAS24
        </a>
    </td>
    """
    # Tournament name
    tname = td.get_text(strip=True)
    game.tname = tname

    # Tournament ID
    a = td.find("a")
    assert a is not None
    href = a.get("href")
    assert href is not None
    parts = href.split("?")
    assert len(parts) == 2
    tid = parts[1]
    game.tid = tid

    # Tournament date (first 8 bytes of the tournament ID)
    yyyymmdd = tid[0:8]
    m = re.match(r'(\d{4})(\d{2})(\d{2})', yyyymmdd)
    assert m is not None
    tdate = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    game.tdate = tdate
    return

def parse_second_td(game: Game, td: element.Tag):
    """ Extracts the section name from this <td> and stores it in the
    game instance variable.
    
    <td>
        ADULTS ONLY WEDNESDAY
    </td>
    """
    sname = td.get_text(strip=True)
    game.sname = sname
    return

def parse_third_td(game: Game, td: element.Tag):
    """ Extracts the round number from this <td> and stores it in the
    game instance variable.
    
    <td>
        1
    </td>
    """
    rnumber = int(td.get_text(strip=True))
    game.rnumber = rnumber
    return

def parse_fourth_td(game: Game, td: element.Tag):
    """ Extracts the color played by the player from
    
    <td>
        B
    </td>
    
    Note that this may be empty or U, if color not known (fairly common)
    """
    color = td.get_text(strip=True)
    if color and color not in ['W', 'B']:
        game.color = "U"
    else:
        game.color = color
    return
    