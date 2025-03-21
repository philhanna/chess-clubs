from chess_clubs import invert_color

def test_invert_white():
    assert invert_color("W") == "B"

def test_invert_black():
    assert invert_color("B") == "W"

def test_invalid_input_returns_unchanged():
    assert invert_color("X") == "X"
    assert invert_color("") == ""
    assert invert_color("w") == "w"  # Case-sensitive check
    assert invert_color("b") == "b"
    assert invert_color("White") == "White"
    assert invert_color("Black") == "Black"

def test_none_input_returns_none():
    assert invert_color(None) is None
