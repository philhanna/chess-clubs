import os
import sqlite3
from clubs.club import Club

def main(clubid: str, dbname: str):
    """
    Main function to create and populate a SQLite database with club and player data.
    
    Args:
        clubid (str): The unique identifier for the club.
        dbname (str): The name of the SQLite database file.
    """

    # Delete the database if it already exists to ensure a fresh start
    if os.path.exists(dbname):
        os.remove(dbname)

    # Create and connect to the new SQLite database
    with sqlite3.connect(dbname) as con:
        cur = con.cursor()

        # SQL script to create necessary tables for clubs and players
        sql = """
        
    CREATE TABLE clubs (
        id          TEXT NOT NULL PRIMARY KEY, -- Unique Club ID
        name        TEXT,       -- Name of the club
        url         TEXT        -- Source URL for club information
    );

    CREATE TABLE players (
        id          TEXT NOT NULL PRIMARY KEY, -- Unique Player ID
        name        TEXT,       -- Player's name
        state       TEXT,       -- Player's state of residence
        date        TEXT,       -- Date of rating
        rating      INT,        -- USCF rating
        event_count INT,        -- Number of tournaments played
        last_event  TEXT        -- Last tournament played
    );
    
"""
        cur.executescript(sql)  # Execute the SQL script to create tables

        # Create a Club object using the given club ID
        club = Club(clubid)
        
        # Insert club details into the database
        sql = """
        
    INSERT INTO clubs (id, name, url) VALUES(?, ?, ?)

"""
        cur.execute(sql, (club.id, club.name, club.url))
        con.commit()

        # Insert active players associated with the club into the database
        for player in club.get_active_players():
            
            # Check if the player already exists in the database
            sql = """
            
    SELECT 1 FROM players WHERE id=?

"""
            cur.execute(sql, (player.id,))
            
            if cur.fetchone() is None:
                # Insert player details into the database
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

    # Execution complete
    return
