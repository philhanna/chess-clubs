from datetime import datetime
import os
import sqlite3

from bs4 import BeautifulSoup
from chess_clubs import get_head_to_head_url, get_page, is_game_row
from chess_clubs.club import Club, Player
from chess_clubs.game import Game
from chess_clubs.game_factory import GameFactory
from chess_clubs.summary import Summary


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

            for i in range(len(players)-1):
                player = players[i]
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"LOG: {current_time} {str(player)}")

                # Add this player to the Players table in the database
                self.add_player(con, player)

                # Do the head-to-head matchup between this player and
                # all others
                for j in range(1, len(players)):
                    opponent = players[j]

                    # Start tracking the summary for this pair
                    summary = Summary(player.id, opponent.id)

                    # Get the HTML of the head-to-head matchup page
                    url = get_head_to_head_url(player.id, opponent.id)
                    html = get_page(url)
                    soup = BeautifulSoup(html, 'html.parser')

                    # From the head-to-head page, retrieve all the games
                    # played by this pair
                    th = soup.find(
                        "th", string=lambda text: text and "Event Name" in text)
                    if th is not None:

                        # Skip the headings row
                        tr = th.find_parent("tr")

                        # Process each game row
                        while True:
                            tr = tr.find_next_sibling("tr")
                            if not tr or not is_game_row(tr):
                                break

                            # Parse the game and assign player details
                            game = GameFactory.from_soup(tr)
                            game.player_id = player.id
                            game.player_name = player.name

                            # Update the summary
                            summary.update_with(game)

                            # Store the game data
                            self.add_game(con, game)

                            # Invert the game and store that
                            game.invert()
                            self.add_game(con, game)

                    # Write the summary to the database
                    self.add_summary(con, summary)

                    # Invert the summary and store that
                    summary.invert()
                    self.add_summary(con, summary)

        # Execution complete
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
        Adds this game to the database if it is not already there
        """
        cur = con.cursor()

        # Check whether the game already exists in the database
        sql = """ SELECT 1 FROM games WHERE pid == ? AND oid == ? """
        cur.execute(sql, (game.player_id, game.opponent_id))
        if cur.fetchone() is not None:
            return

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

    def add_summary(self, con: sqlite3.Connection, summary: Summary):
        """
        Adds the summary to the database if it is not already there
        """
        cur = con.cursor()

        # Check whether the summary already exists in the database
        sql = """ SELECT 1 from summaries WHERE pid=? AND oid=? """
        cur.execute(sql, (summary.pid, summary.oid))
        if cur.fetchone() is not None:
            return

        # Insert summary details into the database
        sql = """
        
        INSERT INTO summaries (pid, oid, )
        """

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
            pid         TEXT NOT NULL,  -- Unique ID of player 1
            oid         TEXT NOT NULL,  -- Unique ID of player 2
            tid         TEXT,       -- Tournament ID
            sname       TEXT,       -- Section name
            rnumber     INT,        -- Round number
            color       TEXT,       -- Color played ("W" for White, "B" for Black)
            result      TEXT,       -- Result ("W" for win, "L" for loss, "D" for draw)
            PRIMARY KEY (pid, oid)                  
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
