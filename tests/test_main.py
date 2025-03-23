import pytest

from chess_clubs.core import Main
from tests import config

@pytest.mark.mainline
def test_main():        
    club_id = config["club_id"]
    dbname = f"{club_id}.db"
    app = Main(club_id, dbname)
    app.run()