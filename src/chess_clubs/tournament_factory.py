from dataclasses import dataclass


@dataclass
class Tournament:
    id: str
    name: str
    location: str
    date: str
    club_id: str
    chief_td_id: str
    n_sections: int
    n_players: int
    
class TournamentFactory:
    def __init__(self, html):
        return