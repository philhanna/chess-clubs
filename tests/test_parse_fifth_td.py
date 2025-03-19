import pytest
from bs4 import BeautifulSoup
from unittest.mock import Mock

from games.game import Game, parse_fifth_td

def create_td_tag(content):
    """Helper function to create a BeautifulSoup <td> tag."""
    return BeautifulSoup(content, "html.parser").td

@pytest.fixture
def game():
    """Fixture to create a mock Game object for testing."""
    return Mock(spec=Game)

def test_parse_fifth_td_valid_id(game):
    td_content = """
    <td>
     <a href="./gamestats.php?memid=12910923&amp;ptype=0&amp;rs=R&amp;dkey=wk_memid&amp;drill=32197553">
      32197553
     </a>
    </td>
    """
    td = create_td_tag(td_content)
    parse_fifth_td(game, td)
    assert game.opponent_id == "32197553"

def test_parse_fifth_td_different_id(game):
    td_content = """
    <td>
     <a href="./gamestats.php?memid=12910923&amp;ptype=0&amp;rs=R&amp;dkey=wk_memid&amp;drill=10000000">
      10000000
     </a>
    </td>
    """
    td = create_td_tag(td_content)
    parse_fifth_td(game, td)
    assert game.opponent_id == "10000000"

def test_parse_fifth_td_whitespace(game):
    td_content = """
    <td>
     <a href="./gamestats.php?memid=12910923&amp;ptype=0&amp;rs=R&amp;dkey=wk_memid&amp;drill=12345678">
        12345678    
     </a>
    </td>
    """
    td = create_td_tag(td_content)
    parse_fifth_td(game, td)
    assert game.opponent_id == "12345678"

def test_parse_fifth_td_no_anchor(game):
    td_content = """
    <td>
      98765432
    </td>
    """
    td = create_td_tag(td_content)
    parse_fifth_td(game, td)
    assert game.opponent_id == "98765432"

def test_parse_fifth_td_empty(game):
    td_content = "<td></td>"
    td = create_td_tag(td_content)
    parse_fifth_td(game, td)
    assert game.opponent_id == ""

def test_parse_fifth_td_nested_tags(game):
    td_content = """
    <td>
     <a href="./gamestats.php?memid=12910923&amp;ptype=0&amp;rs=R&amp;dkey=wk_memid&amp;drill=11223344">
      <span>11223344</span>
     </a>
    </td>
    """
    td = create_td_tag(td_content)
    parse_fifth_td(game, td)
    assert game.opponent_id == "11223344"

def test_parse_fifth_td_multiple_numbers(game):
    td_content = """
    <td>
     <a href="./gamestats.php?memid=12910923&amp;ptype=0&amp;rs=R&amp;dkey=wk_memid&amp;drill=11223344">
      11223344 55667788
     </a>
    </td>
    """
    td = create_td_tag(td_content)
    parse_fifth_td(game, td)
    assert game.opponent_id == "11223344 55667788"

def test_parse_fifth_td_non_numeric(game):
    td_content = """
    <td>
     <a href="./gamestats.php?memid=12910923&amp;ptype=0&amp;rs=R&amp;dkey=wk_memid&amp;drill=ABCDEFGH">
      ABCDEFGH
     </a>
    </td>
    """
    td = create_td_tag(td_content)
    parse_fifth_td(game, td)
    assert game.opponent_id == "ABCDEFGH"
