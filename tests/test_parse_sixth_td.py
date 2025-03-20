import pytest
from bs4 import BeautifulSoup
from unittest.mock import Mock

from games.game import Game
from games.game_factory import parse_sixth_td

def create_td_tag(content):
    """Helper function to create a BeautifulSoup <td> tag."""
    return BeautifulSoup(content, "html.parser").td

@pytest.fixture
def game():
    """Fixture to create a mock Game object for testing."""
    return Mock(spec=Game)

def test_parse_sixth_td_valid_name(game):
    td_content = """
    <td>
     <a href="http://msa.uschess.org/MbrDtlMain.php?32197553">
      GRAHAM RF NAPIER
     </a>
    </td>
    """
    td = create_td_tag(td_content)
    parse_sixth_td(game, td)
    assert game.opponent_name == "Napier, Graham Rf"

def test_parse_sixth_td_different_name(game):
    td_content = """
    <td>
     <a href="http://msa.uschess.org/MbrDtlMain.php?12345678">
      JOHN DOE
     </a>
    </td>
    """
    td = create_td_tag(td_content)
    parse_sixth_td(game, td)
    assert game.opponent_name == "Doe, John"

def test_parse_sixth_td_whitespace(game):
    td_content = """
    <td>
     <a href="http://msa.uschess.org/MbrDtlMain.php?98765432">
        JANE SMITH    
     </a>
    </td>
    """
    td = create_td_tag(td_content)
    parse_sixth_td(game, td)
    assert game.opponent_name == "Smith, Jane"

def test_parse_sixth_td_no_anchor(game):
    td_content = """
    <td>
      MICHAEL BROWN
    </td>
    """
    td = create_td_tag(td_content)
    parse_sixth_td(game, td)
    assert game.opponent_name == "Brown, Michael"

def test_parse_sixth_td_empty(game):
    td_content = "<td></td>"
    td = create_td_tag(td_content)
    parse_sixth_td(game, td)
    assert game.opponent_name == ""

def test_parse_sixth_td_nested_tags(game):
    td_content = """
    <td>
     <a href="http://msa.uschess.org/MbrDtlMain.php?11223344">
      <span>DAVID LEE</span>
     </a>
    </td>
    """
    td = create_td_tag(td_content)
    parse_sixth_td(game, td)
    assert game.opponent_name == "Lee, David"

def test_parse_sixth_td_special_characters(game):
    td_content = """
    <td>
     <a href="http://msa.uschess.org/MbrDtlMain.php?55667788">
      O'REILLY
     </a>
    </td>
    """
    td = create_td_tag(td_content)
    parse_sixth_td(game, td)
    assert game.opponent_name == "O'Reilly"

def test_parse_sixth_td_numbers_in_name(game):
    td_content = """
    <td>
     <a href="http://msa.uschess.org/MbrDtlMain.php?99001122">
      BOB 123
     </a>
    </td>
    """
    td = create_td_tag(td_content)
    parse_sixth_td(game, td)
    assert game.opponent_name == "123, Bob"
