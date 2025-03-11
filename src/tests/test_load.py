import os
import pytest
from unittest.mock import patch
from bs4 import BeautifulSoup

from chess_clubs.club import Club
from tests.testdata import TESTDATA


# Sample HTML with a valid structure (3 tables, correct elements)
#
# NOTE: This is currently not used. The sample html file is used instead.
SAMPLE_HTML_VALID = """
<html>
<body>
    <table></table>
    <table></table>
    <table>
        <tr>
            <td><font size="+1">A6021250: HIGHWAY 264 CHESS PROMOTIONS</font></td>
        </tr>
        <tr>
            <td><a href="https://www.uschess.org/datapage/top-affil-players.php?affil=A6021250">Active Player List</a></td>
        </tr>
    </table>
</body>
</html>
"""

# Sample HTML with fewer than 3 tables (should trigger an error)
SAMPLE_HTML_FEW_TABLES = """
<html>
<body>
    <table></table>
    <table></table>
</body>
</html>
"""

# Sample HTML missing the <font size="+1"> tag (should trigger an error)
SAMPLE_HTML_NO_FONT_TAG = """
<html>
<body>
    <table></table>
    <table></table>
    <table>
        <tr>
            <td><a href="https://www.uschess.org/datapage/top-affil-players.php?affil=A6021250">Active Player List</a></td>
        </tr>
    </table>
</body>
</html>
"""

# Sample HTML missing the Active Player List link (should trigger an error)
SAMPLE_HTML_NO_PLAYER_LIST = """
<html>
<body>
    <table></table>
    <table></table>
    <table>
        <tr>from chess_clubs import get_page

            <td><font size="+1">A6021250: HIGHWAY 264 CHESS PROMOTIONS</font></td>
        </tr>
    </table>
</body>
</html>
"""


@patch("chess_clubs.get_page")
def test_load_success(mock_get_page):
    """Test that the load method works when at least 3 tables exist."""
    testfile = os.path.join(TESTDATA, "A6021250_main.html")
    with open(testfile) as fp:
        html = fp.read()
    mock_get_page.return_value = html
    club = Club(id="A6021250")

    # No exception should be raised
    club.load()
    _ = str(club)

    assert club.id == "A6021250"
    assert club.name == "HIGHWAY 264 CHESS PROMOTIONS"
    assert club.url == "https://www.uschess.org/datapage/top-affil-players.php?affil=A6021250&min=6&Search=Submit"


@patch("chess_clubs.get_page")
def test_load_fails_with_few_tables(mock_get_page):
    """Test that load raises an error if fewer than 3 tables are found."""
    mock_get_page.return_value = SAMPLE_HTML_FEW_TABLES
    club = Club(id="A6021250")

    with pytest.raises(ValueError, match=r"Expected at least 3 tables, found 2"):
        club.load()


@patch("chess_clubs.get_page")
def test_load_fails_missing_font_tag(mock_get_page):
    """Test that load raises an error if the font tag with size='+1' is missing."""
    mock_get_page.return_value = SAMPLE_HTML_NO_FONT_TAG
    club = Club(id="A6021250")

    with pytest.raises(ValueError, match="No <font size=\\+1> tag found"):
        club.load()


@patch("chess_clubs.get_page")
def test_load_fails_missing_active_player_list(mock_get_page):
    """Test that load raises an error if the Active Player List link is missing."""
    mock_get_page.return_value = SAMPLE_HTML_NO_PLAYER_LIST
    club = Club(id="A6021250")

    with pytest.raises(AttributeError):  # Since .get("href") would be called on None
        club.load()
