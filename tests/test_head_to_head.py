import pytest
from unittest.mock import patch
from pathlib import Path

from chess_clubs.head_to_head import HeadToHead
from tests.testdata import TESTDATA

@pytest.fixture
def sample_html():
    # Load mock HTML from local file
    path = Path(TESTDATA) / "head_to_head_page.html" 
    return path.read_text(encoding="utf-8")

@pytest.fixture
def bad_html():
    path = Path(TESTDATA) / "head_to_head_zero.html"
    return path.read_text(encoding="utf-8")

def test_head_to_head_init_parses_html(sample_html):
    with patch.object(HeadToHead, 'get_html', return_value=sample_html):
        # Create a HeadToHead object, which will use the mocked HTML
        h2h = HeadToHead(player_id="12345678", opponent_id="87654321")
        assert h2h.player_id == "12345678"
        assert h2h.opponent_id == "87654321"
        assert isinstance(h2h.games, list)
        assert len(h2h.games) == 6

def test_head_to_head_zero(bad_html):
    with patch.object(HeadToHead, 'get_html', return_value=bad_html):
        # Create a HeadToHead object, which will use the mocked HTML
        h2h = HeadToHead(player_id="12345678", opponent_id="87654321")
        assert h2h.player_id == "12345678"
        assert h2h.opponent_id == "87654321"
        assert isinstance(h2h.games, list)
        assert len(h2h.games) == 0
