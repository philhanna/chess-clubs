from bs4 import BeautifulSoup

from chess_clubs import parse_player
from chess_clubs.player import Player


def test_parse_player():
    """Test parse_player function with a valid input HTML row."""
    html = """
    <tr>
        <td> 1 </td>
        <td> <a href="http://msa.uschess.org/MbrDtlMain.php?30420180"> 30420180 </a> </td>
        <td> <center> 2026-12-31 </center> </td>
        <td> AVANNI RICHARDSON </td>
        <td> <center> NC </center> </td>
        <td> <center> 2020 </center> </td>
        <td> 2025-03-01 </td>
        <td> <center> 21 </center> </td>
        <td> <a href="http://msa.uschess.org/XtblMain.php?202502076302"> 202502076302 </a> </td>
    </tr>
    """
    
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    tr = soup.find("tr")
    
    # Run the function
    player = parse_player(tr)
    
    # Expected output
    expected_player = Player(
        id="30420180",
        name="AVANNI RICHARDSON",
        state="NC",
        rating="2020",
        date="2025-03-01",
        event_count="21",
        last_event="202502076302",
    )
    
    # Assertions
    assert player.id == expected_player.id
    assert player.name == expected_player.name
    assert player.state == expected_player.state
    assert player.rating == expected_player.rating
    assert player.date == expected_player.date
    assert player.event_count == expected_player.event_count
    assert player.last_event == expected_player.last_event
