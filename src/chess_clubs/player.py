from name_formatter import FormattedName

from chess_clubs import player_name_from_id


class Player:
    """ A player in this club """

    def __init__(self, id: str, name: str = None):
        self._id: str = id
        if not name:
            name = player_name_from_id(id)
        formatter = FormattedName(name)
        self._name: str = str(formatter)

    @property
    def id(self) -> str:
        """Returns the unique identifier of the player."""
        return self._id

    @property
    def name(self) -> str:
        """Returns the name of the player."""
        return self._name

    def __str__(self) -> str:
        return f"{self.id}:{self.name}"

    def get_head_to_head(opponent: str):
        """ A generator for lifetime statistics for two players
        Args:
            opponent: str    The USCF 8-digit id of the second player

        Returns:
            (games, wins, losses, draws), a tuple of integers

        https://www.uschess.org/datapage/gamestats.php?memid=<player1>&ptype=O&rs=R&drill=<player2>

        """
        pass
