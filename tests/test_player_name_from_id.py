from unittest.mock import patch

from chess_clubs import player_name_from_id

@patch("chess_clubs.get_page")
def test_valid_player_id_returns_name(mock_get_page):
    html = '''
    <html><body>
        <input type="text" name="memname" value="John Doe">
    </body></html>
    '''
    mock_get_page.return_value = html
    assert player_name_from_id("12345678") == "John Doe"

@patch("chess_clubs.get_page")
def test_missing_memname_returns_empty_string(mock_get_page):
    html = '''
    <html><body>
        <p>No name here</p>
    </body></html>
    '''
    mock_get_page.return_value = html
    assert player_name_from_id("12345678") == ""

@patch("chess_clubs.get_page")
def test_malformed_html(mock_get_page):
    html = "<html><body><input name='wrongname' value='Ghost'></body></html>"
    mock_get_page.return_value = html
    assert player_name_from_id("99999999") == ""
