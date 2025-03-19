import pytest
from bs4 import BeautifulSoup
from unittest.mock import Mock

from games.game import Game
from games.game_factory import parse_third_td 


def create_td_tag(content):
    return BeautifulSoup(f"<td>{content}</td>", "html.parser").td

@pytest.fixture
def game():
    return Mock(spec=Game)

def test_parse_third_td_valid_input(game):
    td = create_td_tag("1")
    parse_third_td(game, td)
    assert game.rnumber == 1

def test_parse_third_td_with_whitespace(game):
    td = create_td_tag("  5  ")
    parse_third_td(game, td)
    assert game.rnumber == 5

def test_parse_third_td_zero(game):
    td = create_td_tag("0")
    parse_third_td(game, td)
    assert game.rnumber == 0

def test_parse_third_td_large_number(game):
    td = create_td_tag("1000")
    parse_third_td(game, td)
    assert game.rnumber == 1000

def test_parse_third_td_invalid_input(game):
    td = create_td_tag("not a number")
    with pytest.raises(ValueError):
        parse_third_td(game, td)

def test_parse_third_td_empty_td(game):
    td = create_td_tag("")
    with pytest.raises(ValueError):
        parse_third_td(game, td)

def test_parse_third_td_nested_content(game):
    td = BeautifulSoup("<td><span>3</span></td>", "html.parser").td
    parse_third_td(game, td)
    assert game.rnumber == 3
