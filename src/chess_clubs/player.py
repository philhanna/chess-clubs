from name_formatter import FormattedName


class Player:
    """ 
    A player in this club.

    Attributes:
        _id (str): The unique identifier of the player.
        _name (str): The formatted name of the player (Last, First).
        _state (str): The state in which the player resides.
        _rating (int): The player's rating as of the last recorded date.
        _date (str): The date the rating was recorded.
        _event_count (int): The number of tournaments the player has participated in.
        _last_event (str): The ID of the last tournament the player participated in.
    """

    def __init__(self,
                 id: str,
                 name: str = None,
                 state: str = None,
                 rating: int = None,
                 date: str = None,
                 event_count: int = None,
                 last_event: str = None):
        """
        Initializes a Player object.

        Args:
            id (str): The unique identifier for the player.
            name (str, optional): The player's name. If not provided, it is looked up using the player ID.
            state (str, optional): The state in which the player resides.
            rating (int, optional): The player's rating.
            date (str, optional): The date the rating was recorded.
            event_count (int, optional): The number of tournaments the player has participated in.
            last_event (str, optional): The ID of the last tournament the player played in.
        """
        self._id: str = id

        # If no name is provided, attempt to retrieve it from an external module
        if not name:
            # Import here to avoid circular dependency issues
            from chess_clubs import player_name_from_id
            name = player_name_from_id(id)

        # Format the name in "Last, First" order
        formatted = FormattedName(name)
        self._name: str = formatted.get_last_first()

        self._state: str = state
        self._rating: int = rating
        self._date: str = date
        self._event_count: int = event_count
        self._last_event: str = last_event

    def __str__(self) -> str:
        """
        Returns a string representation of the Player.

        Returns:
            str: A string in the format "Player(id:name)".
        """
        return f"Player({self.id}:{self.name} {self.rating})"

    @property
    def id(self) -> str:
        """Returns the unique identifier of the player."""
        return self._id

    @property
    def name(self) -> str:
        """Returns the name of the player."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Sets the name of the player and ensures it's formatted."""
        formatted = FormattedName(value)
        self._name = formatted.get_last_first()

    @property
    def state(self) -> str:
        """Returns the state in which the player resides."""
        return self._state

    @state.setter
    def state(self, value: str):
        """Sets the state of the player."""
        self._state = value

    @property
    def rating(self) -> int:
        """Returns the player's rating as of the date specified."""
        return self._rating

    @rating.setter
    def rating(self, value: int):
        """Sets the player's rating."""
        self._rating = value

    @property
    def date(self) -> str:
        """Returns the as-of date."""
        return self._date

    @date.setter
    def date(self, value: str):
        """Sets the as-of date."""
        self._date = value

    @property
    def event_count(self) -> int:
        """Returns the number of tournaments this player has played in this club."""
        return self._event_count

    @event_count.setter
    def event_count(self, value: int):
        """Sets the number of tournaments this player has played in this club."""
        self._event_count = value

    @property
    def last_event(self) -> str:
        """Returns the id of the last tournament played in this club."""
        return self._last_event

    @last_event.setter
    def last_event(self, value: str):
        """Sets the id of the last tournament played in this club."""
        self._last_event = value
