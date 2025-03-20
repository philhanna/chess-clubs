import os
import sqlite3
from clubs.club import Club


def main(clubid: str, dbname: str):
    """ Application mainline """

    # Delete the database if it already exists
    if os.path.exists(dbname):
        os.remove(dbname)

    # Create the empty database and connect to it
    with sqlite3.connect(dbname) as con:
        cur = con.cursor()

        # SQL to create the tables:
        sql = """
        
    CREATE TABLE clubs (
        id          TEXT NOT NULL PRIMARY KEY, -- Club id
        name        TEXT,       -- Club name
        url         TEXT        -- Source URL for club information
    );

    CREATE TABLE players (
        id          TEXT NOT NULL PRIMARY KEY, -- Player id
        name        TEXT,       -- Player name
        state       TEXT,       -- State
        date        TEXT,       -- Date of rating
        rating      INT,        -- USCF rating
        event_count INT,        -- Number of tournaments this club
        last_event  TEXT        -- Last tournament played
    );
"""
        cur.executescript(sql)

        # Create the Club object and write it to the database
        club = Club(clubid)
        sql = """ INSERT INTO clubs (id, name, url) VALUES(?, ?, ?) """
        cur.execute(sql, (club.id, club.name, club.url))
        con.commit()

        # Write the active players into the database
        for player in club.get_active_players():
            cur.execute(""" SELECT 1 FROM players WHERE id=? """,
                        (player.id, ))
            if cur.fetchone() is None:
                sql = """
    INSERT INTO players (id, name, state, date, rating, event_count, last_event)
                VALUES(?, ?, ?, ?, ?, ?, ?)
"""
                cur.execute(sql, (player.id,
                                  player.name,
                                  player.state,
                                  player.date,
                                  player.rating,
                                  player.event_count,
                                  player.last_event))
                con.commit()

    # Done
    return
