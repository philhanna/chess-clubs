class Game:
    def __init__(self):
        self.player_id: str = None      # Player ID
        self.player_name: str = None    # Player name
        self.tname: str = None          # Tournament name
        self.tid: str = None            # Tournament ID
        self.tdate: str = None          # Tournament date
        self.sname: str = None          # Section name
        self.rnumber: int = None        # Round number
        self.color: str = None          # Color played
        self.opponent_id: str = None    # Opponent ID
        self.opponent_name: str = None  # Opponent name
        self.result: str = None         # Result
        
    def __str__(self) -> str:
        parts = []
        parts.append(f'player_id="{self.player_id}"')
        parts.append(f'player_name="{self.player_name}"')
        parts.append(f'tname="{self.tname}"')
        parts.append(f'tid="{self.tid}"')
        parts.append(f'tdate="{self.tdate}"')
        parts.append(f'sname="{self.sname}"')
        parts.append(f'rnumber="{self.rnumber}"')
        parts.append(f'color="{self.color}"')
        parts.append(f'opponent_id="{self.opponent_id}"')
        parts.append(f'opponent_name="{self.opponent_name}"')
        parts.append(f'result="{self.result}"')
        output = ",".join(parts)
        return output
