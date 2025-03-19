import pytest
from bs4 import BeautifulSoup
from unittest.mock import Mock

from games.game import Game
from games.game_factory import parse_fourth_td

# Assuming the function is in a module called 'parser'

def create_td_tag(content):
    """Helper function to create a BeautifulSoup <td> tag."""
    return BeautifulSoup(f"<td>{content}</td>", "html.parser").td

@pytest.fixture
def game():
    """Fixture to create a mock Game object for testing."""
    return Mock(spec=Game)

def test_parse_fourth_td_valid_color_B(game):
    td = create_td_tag("B")
    parse_fourth_td(game, td)
    assert game.color == "B"

def test_parse_fourth_td_valid_color_W(game):
    td = create_td_tag("W")
    parse_fourth_td(game, td)
    assert game.color == "W"

def test_parse_fourth_td_unknown_color_U(game):
    td = create_td_tag("U")
    parse_fourth_td(game, td)
    assert game.color == "U"

def test_parse_fourth_td_blank_color(game):
    td = create_td_tag("")
    parse_fourth_td(game, td)
    assert game.color == ""

def test_parse_fourth_td_invalid_color(game):
    td = create_td_tag("X")
    parse_fourth_td(game, td)
    assert game.color == "U"

def test_parse_fourth_td_whitespace_color(game):
    td = create_td_tag("  B  ")
    parse_fourth_td(game, td)
    assert game.color == "B"

def test_parse_fourth_td_nested_content(game):
    td = BeautifulSoup("<td><span>W</span></td>", "html.parser").td
    parse_fourth_td(game, td)
    assert game.color == "W"

def test_parse_fourth_td_numeric_value(game):
    td = create_td_tag("123")
    parse_fourth_td(game, td)
    assert game.color == "U"

def test_parse_fourth_td_special_characters(game):
    td = create_td_tag("@#$")
    parse_fourth_td(game, td)
    assert game.color == "U"
