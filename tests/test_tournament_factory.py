import os
import pytest
from bs4 import BeautifulSoup

from chess_clubs.tournament_factory import TournamentFactory
from tests.testdata import TESTDATA

@pytest.fixture
def get_sample_page_soup():
    testfile = os.path.join(TESTDATA, "tournament.html")
    with open(testfile) as fp:
        html = fp.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def test_parse(get_sample_page_soup):
    tmt = TournamentFactory.from_soup(get_sample_page_soup)
    print(f"\nDEBUG: {tmt=}")