import re
from bs4 import element
from name_formatter import FormattedName
from chess_clubs.game import Game


class GameFactory:
    """
    Factory class responsible for creating Game objects from HTML table rows.
    """

    def from_soup(player_id: str, tr: element.Tag) -> Game:
        """
        Parses an HTML table row (<tr>) from a Game Statistics page in
        the USCF website and creates a Game object with extracted attributes.
        The Game Statistics page is the one that shows lifetime head-to-head
        matchups between two players.  The url is created from the
        get_head_to_head_url() method in the HeadToHead class.

        Args:
            tr (element.Tag): A BeautifulSoup Tag object representing a
            row in the game table.

        Returns:
            Game: A fully populated Game object.
        """
        game = Game()
        game.player_id = player_id

        # The <tr> looks something like this:
        #
        # <tr>
        #   <td> <a href="http://msa.uschess.org/XtblMain.php?202412219692"> ADULT AND YOUTH BEFORE CHRISTMAS24 </a> </td>
        #   <td> ADULTS ONLY WEDNESDAY </td>
        #   <td> 1 </td>
        #   <td> B </td>
        #   <td> <a href="./gamestats.php?memid=12910923&amp;ptype=0&amp;rs=R&amp;dkey=wk_memid&amp;drill=32197553"> 32197553 </a> </td>
        #   <td> <a href="http://msa.uschess.org/MbrDtlMain.php?32197553"> GRAHAM RF NAPIER </a> </td>
        #   <td> <nobr> 1074 =&gt; 1012 (R) </nobr> </td>
        #   <td> W </td>
        #   </tr>

        # Parse the <tr> for the game attributes
        tds = tr.find_all("td")
        assert len(tds) >= 8, f"Expected 8 <td> elements, found {len(tds)}"

        parse_first_td(game, tds[0])    # Tournament name, ID, and date
        parse_second_td(game, tds[1])   # Section name
        parse_third_td(game, tds[2])    # Round number
        parse_fourth_td(game, tds[3])   # Color played
        parse_fifth_td(game, tds[4])    # Opponent ID
        parse_sixth_td(game, tds[5])    # Opponent name
        parse_seventh_td(game, tds[6])  # Rating string (not used)
        parse_eighth_td(game, tds[7])   # Result (W|L|D)

        return game

#   ============================================================
#   Parsing Functions
#   ============================================================


def parse_first_td(game: Game, td: element.Tag):
    """
    Extracts tournament name, ID, and date from a <td> element.

    Args:
        game (Game): The game instance being populated.
        td (element.Tag): The table cell containing tournament information.
    """
    
    # Tournament name
    game.tname = td.get_text(strip=True)

    # Tournament ID
    a = td.find("a")
    assert a is not None, "Expected an <a> tag with tournament ID."

    href = a.get("href")
    assert href is not None, "Expected a valid href attribute."

    a = td.find("a")
    assert a is not None
    href = a.get("href")
    assert href is not None
    parts = href.split("?")
    assert len(parts) == 2
    tid = parts[1]
    game.tid = tid

    # Extract tournament date from the first 8 characters of tournament ID
    yyyymmdd = tid[:8]
    m = re.match(r'(\d{4})(\d{2})(\d{2})', yyyymmdd)
    assert m is not None, "Invalid tournament date format."
    game.tdate = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"


def parse_second_td(game: Game, td: element.Tag):
    """
    Extracts the section name from a <td> element.
    """
    game.sname = td.get_text(strip=True)


def parse_third_td(game: Game, td: element.Tag):
    """
    Extracts the round number from a <td> element.
    """
    game.rnumber = int(td.get_text(strip=True))


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


def parse_fifth_td(game: Game, td: element.Tag):
    """
    Extracts the opponent's ID from a <td> element.
    """
    game.opponent_id = td.get_text(strip=True)


def parse_sixth_td(game: Game, td: element.Tag):
    """
    Extracts the opponent's name and formats it as Last, First.
    """
    name = td.get_text(strip=True)
    game.opponent_name = FormattedName(name).get_last_first()


def parse_seventh_td(game: Game, td: element.Tag):
    """
    Placeholder function for rating information (not used).
    """
    pass


def parse_eighth_td(game: Game, td: element.Tag):
    """
    Extracts the game result (W/L/D) from a <td> element.
    """
    game.result = td.get_text(strip=True)
