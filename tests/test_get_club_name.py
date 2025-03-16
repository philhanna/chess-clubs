import pytest
from bs4 import BeautifulSoup
from clubs import get_club_name
from clubs.club import Club
from tests import get_config

@pytest.fixture
def club():
    """Fixture to create a Club instance."""
    config = get_config()
    id = config["club_id"]
    return Club(id)

def test_get_club_name_valid(club):
    """Test that the method correctly extracts the club name from a valid table."""
    html = """
    <html>
        <body>
            <table>
                <tr><td><font size="+1">A6021250: HIGHWAY 264 CHESS PROMOTIONS</font></td></tr>
            </table>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")
    
    assert get_club_name(table) == "HIGHWAY 264 CHESS PROMOTIONS"

def test_get_club_name_missing_font_tag(club):
    """Test that the method raises a ValueError when the font tag is missing."""
    html = "<table><tr><td>No font tag here</td></tr></table>"
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")

    with pytest.raises(ValueError, match="No <font size=\\+1> tag found"):
        get_club_name(table)

def test_get_club_name_invalid_format(club):
    """Test that the method raises an error if the font tag doesn't contain ':'."""
    html = """
    <table>
        <tr><td><font size="+1">Invalid Format Club Name</font></td></tr>
    </table>
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")

    with pytest.raises(ValueError):  # Expect a ValueError due to missing ':'
        get_club_name(table)

def test_get_club_name_extra_spaces(club):
    """Test that extra spaces are stripped correctly."""
    html = """
    <table>
        <tr><td><font size="+1">   A6021250   :   HIGHWAY 264 CHESS PROMOTIONS   </font></td></tr>
    </table>
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")

    assert get_club_name(table) == "HIGHWAY 264 CHESS PROMOTIONS"

def test_get_club_name_multiple_font_tags(club):
    """Test that the method correctly picks the first matching font tag."""
    html = """
    <table>
        <tr><td><font size="+1">A6021250: FIRST CLUB NAME</font></td></tr>
        <tr><td><font size="+1">B7021450: SECOND CLUB NAME</font></td></tr>
    </table>
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")

    assert get_club_name(table) == "FIRST CLUB NAME"
