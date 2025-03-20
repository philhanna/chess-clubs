# Package for games, game functions, and factory classes

#   ============================================================
#   Functions
#   ============================================================
            
def invert_color(color: str) -> str:
    """
    Inverts the color played in a game.
    
    Args:
        color (str): "W" for White or "B" for Black.
    
    Returns:
        str: "B" if input was "W", "W" if input was "B", otherwise unchanged.
    """
    if color and color == "W":
        return "B"
    if color and color == "B":
        return "W"
    return color

def invert_result(result: str) -> str:
    """
    Inverts the game result perspective.
    
    Args:
        result (str): "W" for win, "L" for loss, "D" for draw.
    
    Returns:
        str: "L" if input was "W", "W" if input was "L", otherwise unchanged.
    """
    if result and result == "W":
        return "L"
    if result and result == "L":
        return "W"
    return result
