from name_formatter import format_name

class Player:
    """ A player in this club """
    def __init__(self, id: str, name: str):
        self._id: str = id
        self._name: str = name
        
    @property
    def id(self) -> str:
        """Returns the unique identifier of the player."""
        return self._id

    @property
    def name(self) -> str:
        """Returns the name of the player."""
        return self._name
    
    def __str__(self) -> str:
        formatter = format_name(self.name)
        name = str(formatter)
        
        return f"{self.id}:{name}"
