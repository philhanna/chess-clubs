from chess_clubs.game import Game


def test_invert_basic_white_win():
    game = Game()
    game.player_id = "P1"
    game.opponent_id = "P2"
    game.player_name = "Alice"
    game.opponent_name = "Bob"
    game.color = "W"
    game.result = "W"

    game.invert()

    assert game.player_id == "P2"
    assert game.opponent_id == "P1"
    assert game.player_name == "Bob"
    assert game.opponent_name == "Alice"
    assert game.color == "B"  # White becomes Black
    assert game.result == "L"  # Win becomes Loss


def test_invert_black_loss():
    game = Game()
    game.player_id = "X"
    game.opponent_id = "Y"
    game.player_name = "Carol"
    game.opponent_name = "Dave"
    game.color = "B"
    game.result = "L"

    game.invert()

    assert game.player_id == "Y"
    assert game.opponent_id == "X"
    assert game.player_name == "Dave"
    assert game.opponent_name == "Carol"
    assert game.color == "W"
    assert game.result == "W"


def test_invert_draw_result():
    game = Game()
    game.player_id = "123"
    game.opponent_id = "456"
    game.player_name = "Eve"
    game.opponent_name = "Frank"
    game.color = "W"
    game.result = "D"

    game.invert()

    assert game.player_id == "456"
    assert game.opponent_id == "123"
    assert game.player_name == "Frank"
    assert game.opponent_name == "Eve"
    assert game.color == "B"
    assert game.result == "D"  # Draw stays the same


def test_invert_unexpected_values():
    game = Game()
    game.player_id = "A"
    game.opponent_id = "B"
    game.player_name = "PlayerA"
    game.opponent_name = "PlayerB"
    game.color = "X"
    game.result = "Z"

    game.invert()

    assert game.player_id == "B"
    assert game.opponent_id == "A"
    assert game.player_name == "PlayerB"
    assert game.opponent_name == "PlayerA"
    assert game.color == "X"  # Unknown color remains unchanged
    assert game.result == "Z"  # Unknown result remains unchanged
def test_double_invert_restores_original():
    game = Game()
    game.player_id = "100"
    game.opponent_id = "200"
    game.player_name = "Alpha"
    game.opponent_name = "Beta"
    game.color = "W"
    game.result = "L"

    original_state = {
        "player_id": game.player_id,
        "opponent_id": game.opponent_id,
        "player_name": game.player_name,
        "opponent_name": game.opponent_name,
        "color": game.color,
        "result": game.result,
    }

    game.invert()
    game.invert()

    assert game.player_id == original_state["player_id"]
    assert game.opponent_id == original_state["opponent_id"]
    assert game.player_name == original_state["player_name"]
    assert game.opponent_name == original_state["opponent_name"]
    assert game.color == original_state["color"]
    assert game.result == original_state["result"]
