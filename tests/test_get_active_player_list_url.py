import pytest
from bs4 import BeautifulSoup

from chess_clubs import get_active_player_list_url


def make_table_with_link(href="/some/path?param=value"):
    html = f'''
    <table>
        <tr><td><a href="{href}">Active Player List</a></td></tr>
    </table>
    '''
    return BeautifulSoup(html, "html.parser").table

def test_default_min_games():
    table = make_table_with_link("/players?sort=rating")
    url = get_active_player_list_url(table)
    assert url == "/players?sort=rating&min=5&Search=Submit"

def test_custom_min_games():
    table = make_table_with_link("/players?sort=rating")
    url = get_active_player_list_url(table, min_games=10)
    assert url == "/players?sort=rating&min=10&Search=Submit"

def test_existing_query_parameters():
    table = make_table_with_link("/list?category=active")
    url = get_active_player_list_url(table, min_games=20)
    assert url == "/list?category=active&min=20&Search=Submit"

def test_no_link_raises_exception():
    html = '''
    <table>
        <tr><td><a href="/other">Other Link</a></td></tr>
    </table>
    '''
    table = BeautifulSoup(html, "html.parser").table
    with pytest.raises(AttributeError):
        get_active_player_list_url(table)
