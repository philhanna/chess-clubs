import os
import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import requests
from chess_clubs.club import Club
from testdata import TESTDATA

@pytest.fixture
def sample_html():
    """Returns a sample HTML response with at least 3 tables."""
    testfile = os.path.join(TESTDATA, "main.html")
    with open(testfile) as fp:
        html = fp.read()
    return html

@pytest.fixture
def insufficient_tables_html():
    """Returns a sample HTML response with fewer than 3 tables."""
    return """
    <html><body>
        <table id="first"></table>
        <table id="second"></table>
    </body></html>
    """

@patch.object(Club, 'get')
def test_load_success(mock_get, sample_html):
    """Test that the load method works when at least 3 tables exist."""
    mock_get.return_value = sample_html
    club = Club(id="A6021250")

    # No exception should be raised
    club.load()

@patch.object(Club, 'get')
def test_load_fails_with_few_tables(mock_get, insufficient_tables_html):
    """Test that load raises a ValueError when there are fewer than 3 tables."""
    mock_get.return_value = insufficient_tables_html
    club = Club(id="5678")

    with pytest.raises(ValueError, match="Expected at least 3 tables, found 2"):
        club.load()

@patch.object(requests, 'get')
def test_load_http_error(mock_requests_get):
    """Test that load raises an HTTP error when the request fails."""
    mock_requests_get.side_effect = requests.HTTPError("404 Not Found")
    club = Club(id="91011")

    with pytest.raises(requests.HTTPError, match="404 Not Found"):
        club.load()

@patch.object(requests, 'get')
def test_load_timeout(mock_requests_get):
    """Test that load raises a timeout error when the request takes too long."""
    mock_requests_get.side_effect = requests.Timeout("Request timed out")
    club = Club(id="121314")

    with pytest.raises(requests.Timeout, match="Request timed out"):
        club.load()
