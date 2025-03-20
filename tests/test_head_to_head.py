import pytest

from clubs.head_to_head import HeadToHead
from tests import config

def test_good_pair():
    player_id = config['head_to_head']['player1']
    opponent_id = config['head_to_head']['player2']
    obj = HeadToHead(player_id, opponent_id)
    obj.load()
    assert obj is not None