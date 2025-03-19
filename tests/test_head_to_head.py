import pytest

from games.head_to_head import HeadToHead

def test_good_pair():
    player_id = "12910923"
    opponent_id = "32197553"
    obj = HeadToHead(player_id, opponent_id)
    assert obj is not None