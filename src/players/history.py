class History:
    """ Contains the lifetime history of games played by a player vs. another """

    def __init__(self, player1: str, player2: str):
        """ Creates a history object from the USCF ids of two players """
        self.player1: str = player1
        self.player2: str = player2
        self.games: int = 0
        self.wins: int = 0
        self.losses: int = 0
        self.draws: int = 0
