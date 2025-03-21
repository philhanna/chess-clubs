from unittest.mock import MagicMock, patch
from name_formatter import FormattedName
from chess_clubs import player_name_from_id
from chess_clubs.player import Player

@patch("chess_clubs.player_name_from_id")
@patch("name_formatter.FormattedName")
def test_player_constructor_without_name(mock_formatted_name_class, mock_player_name_from_id):
    # Arrange
    mock_player_name_from_id.return_value = "Elmer Fudd"
    
    mock_formatted_name_instance = MagicMock()
    mock_formatted_name_instance.get_last_first.return_value = "Fudd, Elmer"
    mock_formatted_name_class.return_value = mock_formatted_name_instance

    # Act
    player = Player(id="12345678")
    _ = str(player)

    # Assert
    mock_player_name_from_id.assert_called_once_with("12345678")
    
    assert player.id == "12345678"
    assert player.name == "Fudd, Elmer"
    
    player.name = "Empty"

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
