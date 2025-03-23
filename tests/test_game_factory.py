from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock
from chess_clubs.game import Game
from chess_clubs.game_factory import GameFactory


@patch("name_formatter.FormattedName")
def test_from_soup_with_valid_row(mock_formatted_name_class):
    # Prepare mock for FormattedName
    mock_name = MagicMock()
    mock_name.get_last_first.return_value = "Napier, Graham"
    mock_formatted_name_class.return_value = mock_name

    html = """
    <tr>
        <td><a href="http://msa.uschess.org/XtblMain.php?202412219692"> ADULT AND YOUTH BEFORE CHRISTMAS24 </a></td>
        <td>ADULTS ONLY WEDNESDAY</td>
        <td>1</td>
        <td>B</td>
        <td><a href="./gamestats.php?memid=12910923&amp;ptype=0&amp;rs=R&amp;dkey=wk_memid&amp;drill=32197553">32197553</a></td>
        <td><a href="http://msa.uschess.org/MbrDtlMain.php?32197553">GRAHAM RF NAPIER</a></td>
        <td><nobr>1074 =&gt; 1012 (R)</nobr></td>
        <td>W</td>
    </tr>
    """

    player_id = "12910923"
    soup = BeautifulSoup(html, "html.parser")
    tr = soup.find("tr")

    game = GameFactory.from_soup(player_id, tr)

    assert isinstance(game, Game)
    assert game.player_id == player_id
    assert game.tname == "ADULT AND YOUTH BEFORE CHRISTMAS24"
    assert game.tid == "202412219692"
    assert game.tdate == "2024-12-21"
    assert game.sname == "ADULTS ONLY WEDNESDAY"
    assert game.rnumber == 1
    assert game.color == "B"
    assert game.opponent_id == "32197553"
    assert game.opponent_name == "Napier, Graham Rf"
    assert game.result == "W"
