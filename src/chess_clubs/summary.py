from chess_clubs.game import Game

class Summary:
    """
    Represents a summary of a player's game results, including wins, losses, draws,
    and the computed percentage score against an opponent
    """
    
    def __init__(self, player_id: str, opponent_id: str):
        """
        Initializes a Summary instance with zeroed statistics.
        """
        self.pid: str = player_id
        self.oid: str = opponent_id
        self._games: int = 0
        self._wins: int = 0
        self._losses: int = 0
        self._draws: int = 0
        self._pct: float = 0.0
    
    def invert(self):
        """
        Inverts the summary by swapping wins and losses.
        Updates the percentage accordingly.
        """
        self.pid, self.oid = self.oid, self.pid
        self.wins, self.losses = self.losses, self.wins
        self._update_pct()
    
    def __str__(self) -> str:
        """
        Returns a string representation of the summary.

        Returns:
            str: A formatted summary string containing games, wins, losses, draws, and percentage.
        """
        parts = [
            f'pid="{self.pid}"',
            f'oid="{self.oid}"',
            f'games="{self.games}"',
            f'wins="{self.wins}"',
            f'losses="{self.losses}"',
            f'draws="{self.draws}"',
            f'pct="{self.pct:.2f}%"'
        ]
        return f"Summary({','.join(parts)})"
    
    def update_with(self, game: Game):
        """
        Updates the summary with a new game result.

        Args:
            game (Game): A game object containing the result.
        """
        if game.result == "W":
            self.wins += 1
        elif game.result == "L":
            self.losses += 1
        elif game.result == "D":
            self.draws += 1
    
    @property
    def games(self) -> int:
        """
        Computes the total number of games played.
        
        Returns:
            int: The sum of wins, losses, and draws.
        """
        return self.wins + self.losses + self.draws

    @property
    def wins(self) -> int:
        """
        Returns the number of wins.
        
        Returns:
            int: The number of wins
        """
        return self._wins

    @wins.setter
    def wins(self, value: int):
        """
        Sets the number of wins and updates the percentage variable.
        
        Args:
            value (int): The number of wins.
        """
        self._wins = value
        self._update_pct()

    @property
    def losses(self) -> int:
        """
        Returns the number of losses

        Returns:
            int: The number of losses
        """
        return self._losses

    @losses.setter
    def losses(self, value: int):
        """
        Sets the number of losses and updates the percentage variable.
        """
        self._losses = value
        self._update_pct()

    @property
    def draws(self) -> int:
        """
        Returns the number of draws.
        Returns:
            int: _description_
        """
        return self._draws

    @draws.setter
    def draws(self, value: int):
        """
        Sets the number of draws
        
        Args:
            value (int): The number of draws.
        """
        self._draws = value
        self._update_pct()

    @property
    def pct(self) -> float:
        """
        Returns the player's score percentage.
        
        Returns:
            float: The calculated percentage score.
        """
        return self._pct

    def _update_pct(self):
        """
        Updates the percentage score based on current win, loss, and draw counts.
        Percentage is represented as a number from zero to 100.
        """
        total = self.games
        if total > 0:
            self._pct = 100.0 * (self._wins + 0.5 * self._draws) / total
        else:
            self._pct = 0.0
