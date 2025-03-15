from name_formatter import FormattedName


class Player:
    """ A player in this club """

    def __init__(self, id: str, name: str):
        self._id: str = id
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
