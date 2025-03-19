# Tests
from bs4 import BeautifulSoup
import pytest

from games.game import Game, parse_first_td


def test_parse_first_td_valid():
    html = '<td><a href="http://msa.uschess.org/XtblMain.php?202412219692">ADULT AND YOUTH BEFORE CHRISTMAS24</a></td>'
    td = BeautifulSoup(html, "html.parser").td
    game = Game()
    parse_first_td(game, td)
    
    assert game.tname == "ADULT AND YOUTH BEFORE CHRISTMAS24"
    assert game.tid == "202412219692"
    assert game.tdate == "2024-12-21"

def test_parse_first_td_no_anchor():
    html = '<td>ADULT AND YOUTH BEFORE CHRISTMAS24</td>'
    td = BeautifulSoup(html, "html.parser").td
    game = Game()
    
    with pytest.raises(AssertionError):
        parse_first_td(game, td)

def test_parse_first_td_no_href():
    html = '<td><a>ADULT AND YOUTH BEFORE CHRISTMAS24</a></td>'
    td = BeautifulSoup(html, "html.parser").td
    game = Game()
    
    with pytest.raises(AssertionError):
        parse_first_td(game, td)

def test_parse_first_td_malformed_href():
    html = '<td><a href="http://msa.uschess.org/XtblMain.php">ADULT AND YOUTH BEFORE CHRISTMAS24</a></td>'
    td = BeautifulSoup(html, "html.parser").td
    game = Game()
    
    with pytest.raises(AssertionError):
        parse_first_td(game, td)

def test_parse_first_td_invalid_tid_format():
    html = '<td><a href="http://msa.uschess.org/XtblMain.php?ABCDEF">ADULT AND YOUTH BEFORE CHRISTMAS24</a></td>'
    td = BeautifulSoup(html, "html.parser").td
    game = Game()
    
    with pytest.raises(AssertionError):
        parse_first_td(game, td)

def test_parse_first_td_short_tid():
    html = '<td><a href="http://msa.uschess.org/XtblMain.php?202412">ADULT AND YOUTH BEFORE CHRISTMAS24</a></td>'
    td = BeautifulSoup(html, "html.parser").td
    game = Game()
    
    with pytest.raises(AssertionError):
        parse_first_td(game, td)
