import pytest
import requests
from unittest.mock import patch
from tests.testdata import TESTDATA
from util import get_page


@pytest.fixture
def main_url():
    testdata = TESTDATA
    return "https://www.uschess.org/msa/AffDtlMain.php?A6021250"

def test_load(main_url):
    