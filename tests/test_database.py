import sqlite3
import pytest

from tests import config

"""
    This module contains a suite of tests to check for database
    integrity.  All tests should be decorated with
    
    @pytest.mark.db
    
    so that they can be run only when a complete database exists.
"""

#   ============================================================
#   Fixtures
#   ============================================================

@pytest.fixture
def clubid():
    clubid = config["club_id"]
    return clubid

@pytest.fixture
def nplayers():
    nplayers = config["nplayers"]
    return nplayers

@pytest.fixture
def dbname(clubid):
    value = f"{clubid}.db"
    return value

#   ============================================================
#   Tests
#   ============================================================

@pytest.mark.db
def test_clubs(dbname):
    """ Verifies that only one club is in the database """
    with sqlite3.connect(dbname) as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM clubs")
        row = cur.fetchone()
        n_clubs = row[0]
        expected = 1
        assert n_clubs == expected
        
@pytest.mark.db
def test_players(dbname, nplayers):
    """ Verifies that the expected count of players are in the database """
    with sqlite3.connect(dbname) as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM players")
        row = cur.fetchone()
        n_players = row[0]
        expected = nplayers
        assert n_players == expected
        
@pytest.mark.db
def test_summary_inversions(dbname):
    """ Verifies that all summaries in the table also exist in inverted form """
    with sqlite3.connect(dbname) as con:
        cur = con.cursor()
        rows = cur.execute(""" SELECT pid, oid, wins, losses, draws FROM summaries""")
        for row in rows.fetchall():            
            pid, oid, wins, losses, draws = row
            cur.execute("""
                SELECT  COUNT(*)
                FROM    summaries
                WHERE   pid=? AND oid=?
                """, (oid, pid))
                       
            # There should be exactly one inverted summary for this one
            expected_count = 1
            actual_count = len(cur.fetchall())
            assert expected_count == actual_count
            
            # and the values should be inverted
            cur.execute("""
                SELECT  pid, oid, wins, losses, draws
                FROM    summaries
                WHERE   pid=? and oid=?
                """, (oid, pid))
            ipid, ioid, iwins, ilosses, idraws = cur.fetchone()
            
            assert ipid == oid
            assert ioid == pid
            assert iwins == losses
            assert ilosses == wins
            assert idraws == draws
