import pytest
from bs4 import BeautifulSoup

from chess_clubs import get_main_table

def test_get_main_table_returns_third():
    html = """
    <html>
        <body>
            <table id="table1"></table>
            <table id="table2"></table>
            <table id="target"></table>
            <table id="table4"></table>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    table = get_main_table(soup)
    assert table.get("id") == "target"

def test_get_main_table_with_exactly_three_tables():
    html = """
    <html>
        <body>
            <table id="first"></table>
            <table id="second"></table>
            <table id="third"></table>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    table = get_main_table(soup)
    assert table.get("id") == "third"

def test_get_main_table_raises_on_less_than_three():
    html = """
    <html>
        <body>
            <table id="one"></table>
            <table id="two"></table>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    with pytest.raises(AssertionError, match="Expected at least 3 tables, found 2"):
        get_main_table(soup)
