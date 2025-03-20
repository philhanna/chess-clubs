from games import invert_color, invert_result


class Game:
    """
    Represents a chess game with relevant details such as player names,
    tournament information, round number, color played, opponent details,
    and game result.
    """
    
    def __init__(self):
        """
        Initializes a Game instance with default None values.
        """
        self.player_id: str = None      # Player ID
        self.player_name: str = None    # Player name
        self.tname: str = None          # Tournament name
        self.tid: str = None            # Tournament ID
        self.tdate: str = None          # Tournament date
        self.sname: str = None          # Section name
        self.rnumber: int = None        # Round number
        self.color: str = None          # Color played ("W" for White, "B" for Black)
        self.opponent_id: str = None    # Opponent ID
        self.opponent_name: str = None  # Opponent name
        self.result: str = None         # Result ("W" for win, "L" for loss, "D" for draw)
    
    def invert(self):
        """
        Inverts the game perspective by swapping player and opponent details.
        
        This function also inverts the color played and the game result.
        """
        self.player_id, self.opponent_id = self.opponent_id, self.player_id
        self.player_name, self.opponent_name = self.opponent_name, self.player_name
        self.color = invert_color(self.color)
        self.result = invert_result(self.result)
                    
    def __str__(self) -> str:
        """
        Returns a string representation of the game.

        Returns:
            str: A formatted string containing all game attributes.
        """
        parts = [
            f'player_id="{self.player_id}"',
            f'player_name="{self.player_name}"',
            f'tname="{self.tname}"',
            f'tid="{self.tid}"',
            f'tdate="{self.tdate}"',
            f'sname="{self.sname}"',
            f'rnumber="{self.rnumber}"',
            f'color="{self.color}"',
            f'opponent_id="{self.opponent_id}"',
            f'opponent_name="{self.opponent_name}"',
            f'result="{self.result}"'
        ]
        return f"Game({','.join(parts)})"
