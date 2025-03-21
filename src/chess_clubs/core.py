import os
import sqlite3
from chess_clubs.club import Club


class Main():

    def __init__(self, clubid: str, dbname: str):
        """
        Initializes class to create and populate a SQLite database with
        club and player data.

        Args:
            clubid (str): The unique identifier for the club.
            dbname (str): The name of the SQLite database file.
        """
        self.clubid = clubid
        self.dbname = dbname
        return

    def run(self):
        """
        Runs the main function that creates the database.
        """
        # Delete the database if it already exists to ensure a fresh start
        if os.path.exists(self.dbname):
            os.remove(self.dbname)

        # Create and connect to the new SQLite database
        with sqlite3.connect(self.dbname) as con:
            self.create_tables(con)

            # Create a Club object using the given club ID and write it
            # to the database
            club = Club(self.clubid)
            self.add_club(con, club)

            # Insert active players associated with the club into the database
            for player in club.get_active_players():
                self.add_player(con, player)

        # Execution complete
        return

    def add_club(self, con, club):
        """ 
        Inserts club details into the database
        """
        sql = """ INSERT INTO clubs (id, name, url) VALUES(?, ?, ?) """
        cur = con.cursor()
        cur.execute(sql, (club.id, club.name, club.url))
        con.commit()
        return

    def add_player(self, con, player):
        """
        Adds the player to the database if it is not already there
        """
        cur = con.cursor()

        # Check whether the player already exists in the database """
        sql = """ SELECT 1 FROM players WHERE id=? """
        cur.execute(sql, (player.id,))
        if cur.fetchone() is not None:
            return

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

    def create_tables(self, con):
        """
        Creates the database and tables
        """
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
        cur = con.cursor()
        cur.executescript(sql)  # Execute the SQL script to create tables
        return
