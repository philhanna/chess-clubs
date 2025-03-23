from datetime import datetime
import os
import sqlite3

from chess_clubs.club import Club, Player
from chess_clubs.game import Game
from chess_clubs.head_to_head import HeadToHead


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
            players = list(club.get_active_players())

            # First, add all the players to the database
            for player in players:
                self.add_player(con, player)

            # Now do the head-to-head matchups
            for i in range(len(players)-1):
                player = players[i]
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"LOG: {current_time} {str(player)}")

                # Do the head-to-head matchup between this player and
                # all others
                for j in range(1, len(players)):
                    opponent = players[j]

                    # Parse the head-to-head matchup page
                    head_to_head = HeadToHead(player.id, opponent.id)
                    for game in head_to_head.games:
                        
                        # Store the game and its inversion
                        self.add_game(con, game)
                        game.invert()
                        self.add_game(con, game)

        # Create the summaries table from the games table
        self.create_summaries(con)
        
        
        return

    #   ========================================================
    #   Database methods
    #   ========================================================

    def add_club(self, con: sqlite3.Connection, club: Club):
        """ 
        Adds the club to the database if it is not already there
        """
        cur = con.cursor()

        # Check whether the club already exists in the database
        sql = """ SELECT 1 FROM clubs WHERE id=? """
        cur.execute(sql, (club.id,))
        if cur.fetchone() is not None:
            return

        # Insert club details into database
        sql = """ INSERT INTO clubs (id, name, url) VALUES(?, ?, ?) """
        cur.execute(sql, (club.id, club.name, club.url))
        con.commit()
        return

    def add_game(self, con: sqlite3.Connection, game: Game):
        """
        Adds this game to the database
        """
        cur = con.cursor()

        # Insert game details into the database
        sql = """
        
        INSERT INTO games (pid, oid, tid, sname, rnumber, color, result)
        VALUES(?, ?, ?, ?, ?, ?, ?)
        
        """
        cur.execute(sql, (game.player_id,
                          game.opponent_id,
                          game.tid,
                          game.sname,
                          game.rnumber,
                          game.color,
                          game.result))
        con.commit()
        return

    def add_player(self, con: sqlite3.Connection, player: Player):
        """
        Adds the player to the database if it is not already there
        """
        cur = con.cursor()

        # Check whether the player already exists in the database
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
        return

    def create_summaries(self, con:sqlite3.Connection):
        """
        Creates the summaries table from the games table
        """
        sql = """
        
        INSERT INTO summaries (pid, oid, wins, losses, draws)
        SELECT
            pid,
            oid,
            SUM(CASE WHEN result = 'W' THEN 1 ELSE 0 END) AS wins,
            SUM(CASE WHEN result = 'L' THEN 1 ELSE 0 END) AS losses,
            SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) AS draws
        FROM        games
        GROUP BY    pid, oid;
        
        """
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        return

    def create_tables(self, con: sqlite3.Connection):
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

        CREATE TABLE games (
            pid         TEXT,       -- Player id
            oid         TEXT,       -- Opponent id
            tid         TEXT,       -- Tournament ID
            sname       TEXT,       -- Section name
            rnumber     INT,        -- Round number
            color       TEXT,       -- Color played ("W" for White, "B" for Black)
            result      TEXT        -- Result ("W" for win, "L" for loss, "D" for draw)
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
        
        CREATE TABLE summaries (
            pid         TEXT NOT NULL,  -- Unique ID of player 1
            oid         TEXT NOT NULL,  -- Unique ID of player 2
            wins        INT,        -- Number of wins
            losses      INT,        -- Number of losses
            draws       INT,        -- Number of draws
            PRIMARY KEY (pid, oid)
        );
        
        CREATE TABLE tournaments (
            id          TEXT NOT NULL PRIMARY KEY, -- Unique Tournament ID
            name        TEXT,       -- Tournament name
            location    TEXT,       -- Location
            date        TEXT,       -- Date
            club_id     TEXT,       -- Club ID 
            chief_td_id TEXT,       -- ID of chief tournament director
            n_sections  INT,        -- Number of sections
            n_players   INT         -- Number of players
        );
        
        """
        cur = con.cursor()
        cur.executescript(sql)  # Execute the SQL script to create tables
        return
