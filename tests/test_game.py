from chess_clubs.game import Game


def test_game_str():
    game = Game()
    game.player_id = "12345678"
    game.player_name = "Elmer Fudd"
    actual = str(game)
    assert "12345678" in actual
    assert "Elmer Fudd" in actual