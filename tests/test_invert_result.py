from chess_clubs import invert_result


def test_invert_win():
    assert invert_result("W") == "L"

def test_invert_loss():
    assert invert_result("L") == "W"

def test_draw_remains_same():
    assert invert_result("D") == "D"

def test_invalid_input_returns_unchanged():
    assert invert_result("X") == "X"
    assert invert_result("") == ""
    assert invert_result("w") == "w"  # Case-sensitive check
    assert invert_result("l") == "l"
    assert invert_result("Win") == "Win"
    assert invert_result("Loss") == "Loss"
    assert invert_result("Draw") == "Draw"

def test_none_input_returns_none():
    assert invert_result(None) is None
