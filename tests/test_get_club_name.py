import pytest
from bs4 import BeautifulSoup
from clubs import get_club_name

def test_get_club_name_valid():
    """Test that the method correctly extracts the club name from a valid table."""
    html = """
    <html>
        <body>
            <table>
                <tr><td><font size="+1">A2345678: MY FAVORITE CLUB</font></td></tr>
            </table>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")
    
    assert get_club_name(table) == "MY FAVORITE CLUB"

def test_get_club_name_missing_font_tag():
    """Test that the method raises a ValueError when the font tag is missing."""
    html = "<table><tr><td>No font tag here</td></tr></table>"
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")

    with pytest.raises(ValueError, match="No <font size=\\+1> tag found"):
        get_club_name(table)

def test_get_club_name_invalid_format():
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

def test_get_club_name_extra_spaces():
    """Test that extra spaces are stripped correctly."""
    html = """
    <table>
        <tr><td><font size="+1">   A2345678   :   MY FAVORITE CLUB   </font></td></tr>
    </table>
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")

    assert get_club_name(table) == "MY FAVORITE CLUB"

def test_get_club_name_multiple_font_tags():
    """Test that the method correctly picks the first matching font tag."""
    html = """
    <table>
        <tr><td><font size="+1">A2345678: FIRST CLUB NAME</font></td></tr>
        <tr><td><font size="+1">B2345678: SECOND CLUB NAME</font></td></tr>
    </table>
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")

    assert get_club_name(table) == "FIRST CLUB NAME"
