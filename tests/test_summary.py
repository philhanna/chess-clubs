from chess_clubs.game import Game
from chess_clubs.summary import Summary


def test_invert():
    
    player_id = "12345678"
    opponent_id = "87654321"
    summary = Summary(player_id, opponent_id)    

    for result in "WWWLDD":
        game = Game()
        game.player_id = player_id
        game.opponent_id = opponent_id
        game.result = result
        summary.update_with(game)
    
    assert summary.pid == player_id
    assert summary.oid == opponent_id
    assert summary.wins == 3
    assert summary.losses == 1
    assert summary.draws == 2
    
    summary.invert()

    assert summary.pid == opponent_id
    assert summary.oid == player_id
    assert summary.wins == 1
    assert summary.losses == 3
    assert summary.draws == 2
    