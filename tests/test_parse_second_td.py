from bs4 import BeautifulSoup

from chess_clubs.game import Game
from chess_clubs.game_factory import parse_second_td

def test_parse_second_td_valid():
    html = '<td>ADULTS ONLY WEDNESDAY</td>'
    td = BeautifulSoup(html, "html.parser").td
    game = Game()
    parse_second_td(game, td)
    
    assert game.sname == "ADULTS ONLY WEDNESDAY"

def test_parse_second_td_empty():
    html = '<td></td>'
    td = BeautifulSoup(html, "html.parser").td
    game = Game()
    parse_second_td(game, td)
    
    assert game.sname == ""
