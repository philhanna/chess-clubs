class Summary:
    def __init__(self):
        self._games: int = 0
        self._wins: int = 0
        self._losses: int = 0
        self._draws: int = 0
        self._pct: float = 0.0
    
    def __str__(self) -> str:
        parts = []
        parts.append(f'games="{self.games}"')
        parts.append(f'wins="{self.wins}"')
        parts.append(f'losses="{self.losses}"')
        parts.append(f'draws="{self.draws}"')
        parts.append(f'pct="{self.pct:.2f}%"')
        inner = ",".join(parts)
        output = f"Summary({inner})"
        return output
    
    @property
    def games(self) -> int:
        return self._games

    @games.setter
    def games(self, value: int):
        if value < 0:
            raise ValueError("Games cannot be negative")
        self._games = value

    @property
    def wins(self) -> int:
        return self._wins

    @wins.setter
    def wins(self, value: int):
        if value < 0:
            raise ValueError("Wins cannot be negative")
        self._wins = value
        self._update_pct()

    @property
    def losses(self) -> int:
        return self._losses

    @losses.setter
    def losses(self, value: int):
        if value < 0:
            raise ValueError("Losses cannot be negative")
        self._losses = value
        self._update_pct()

    @property
    def draws(self) -> int:
        return self._draws

    @draws.setter
    def draws(self, value: int):
        if value < 0:
            raise ValueError("Draws cannot be negative")
        self._draws = value
        self._update_pct()

    @property
    def pct(self) -> float:
        return self._pct

    def _update_pct(self):
        total = self._wins + self._losses + self._draws
        if total > 0:
            self._pct = 100.0 * (self._wins + 0.5 * self._draws) / total
        else:
            self._pct = 0.0
