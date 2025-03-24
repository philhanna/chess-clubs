from dataclasses import dataclass
import re
from bs4 import BeautifulSoup


@dataclass
class Tournament:
    """
    Represents the details of a single tournament
    """
    id: str
    name: str
    location: str
    date: str
    club_id: str
    chief_td_id: str
    n_sections: int
    n_players: int


class TournamentFactory:
    def from_soup(soup: BeautifulSoup) -> Tournament:

        # Locate the summary table by finding the <b> tag with text
        # 'Event Summary', then navigating to its parent <table>
        # element. Assert that the table exists.

        b = soup.find('b', string=lambda s: s and s.strip() == 'Event Summary')
        assert b is not None
        
        summary_table = b.find_parent('table')
        assert summary_table is not None
        
        # Define a helper method

        def get_text_after_label(label: str) -> str:
            """
            Extracts the text content of the first <b> (bold) element
            that follows a <td> element containing the specified label.

            Args:
                label (str): The string to search for within <td>
                    elements of the summary_table.

            Returns:
                str: The stripped text of the first <b> element found
                    after the matching <td>, or None if either the
                    <td> or <b> element is not found.
            """
            td = summary_table.find('td', string=lambda s: s and s.strip() == label.strip())
            if td:
                b = td.find_next("b")
                return b.get_text(strip=True) if b else None
            return None

        # Extract the tournament name and ID from the 'Event' row.  The
        # text is expected in the format: "Tournament Name (1234567)"

        name_and_tid = get_text_after_label('Event')
        name_part, tid_part = name_and_tid.split('(')
        name = name_part.strip()
        tid = tid_part.strip(')')
        
        # Extract the tournament location and date from the
        # corresponding rows in the summary table.
        
        location = get_text_after_label('Location')
        date = get_text_after_label('Event Date(s)')

        # Extract the sponsoring club name and club ID from the
        # 'Sponsoring Affiliate' row.  The club name is in a <b> tag,
        # and the club ID is inside a <small> tag that follows the <b>.

        club_td = summary_table.find('td', string='Sponsoring Affiliate')
        club_b = club_td.find_next('b') if club_td else None
        club_id = club_b.find_next('small').text.strip('()') if club_b else None
        
        # Extract the Chief Tournament Director's name and ID.
        # The name is retrieved using a helper function, and the ID is inside a <small> tag
        # that follows the 'Chief  TD' label in the summary table.
        
        chief_td = get_text_after_label('Chief TD')
        chief_td_small = summary_table.find('td', string='Chief TD').find_next('small')
        chief_td_id = chief_td_small.get_text(strip='()') if chief_td_small else None

        # Extract the number of sections and players from the 'Stats'
        # row.  Expected format: "X Section(s), Y Players" Use a regular
        # expression to parse the numbers; default to 0 if the pattern
        # isn't found.

        stats_text = get_text_after_label('Stats')
        match = re.search(r'(\d+) Section\(s\),\s*(\d+) Players', stats_text)
        n_sections = int(match.group(1)) if match else 0
        n_players = int(match.group(2)) if match else 0

        # Construct the tournament object and return it
        
        tournament = Tournament(
                id=tid,
                name=name,
                location=location,
                date=date,
                club_id=club_id,
                chief_td_id=chief_td_id,
                n_sections=n_sections,
                n_players=n_players)
        
        return tournament