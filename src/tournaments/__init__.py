
from bs4 import BeautifulSoup

from util import get_page


def tournament_name_from_id(tid: str) -> str:
    url = f"https://www.uschess.org/msa/XtblMain.php?{tid}"
    html = get_page(url)
    soup = BeautifulSoup(html, 'html.parser')