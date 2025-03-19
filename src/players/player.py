from name_formatter import FormattedName


class Player:
    """ A player in this club """

    def __init__(self, id: str, name: str = None):
        self._id: str = id
        if not name:
            from players import player_name_from_id
            name = player_name_from_id(id)
        formatted = FormattedName(name)
        self._name: str = formatted.get_first_last()

    @property
    def id(self) -> str:
        """Returns the unique identifier of the player."""
        return self._id

    @property
    def name(self) -> str:
        """Returns the name of the player."""
        return self._name

    def __str__(self) -> str:
        return f"Player({self.id}:{self.name})"
