# ...existing code...
import sqlite3
from typing import List, Optional
from models import Game, GameCreate

def create_connection():
    connection = sqlite3.connect("games.db")
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price FLOAT NOT NULL,
            genre TEXT NOT NULL,
            release_date TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

create_table()

def create_game(game: GameCreate) -> int:
    connection = create_connection()
    cursor = connection.cursor()
    # fixed column name 'release_date'
    cursor.execute(
        "INSERT INTO games(name, description, price, genre, release_date) VALUES (?,?,?,?,?)",
        (game.name, game.description, game.price, game.genre, game.release_date)
    )
    connection.commit()
    game_id = cursor.lastrowid
    connection.close()
    return game_id

def read_games() -> List[Game]:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM games")
    rows = cursor.fetchall()
    connection.close()
    games = [
        Game(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            price=row["price"],
            genre=row["genre"],
            release_date=row["release_date"]
        )
        for row in rows
    ]
    return games

def read_game(game_id: int) -> Optional[Game]:
    connection = create_connection()
    cursor = connection.cursor()
    # pass parameter as tuple
    cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return Game(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        price=row["price"],
        genre=row["genre"],
        release_date=row["release_date"]
    )

def update_game(game_id: int, game: GameCreate) -> bool:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE games SET name = ?, description = ?, price = ?, genre = ?, release_date = ? WHERE id = ?",
        (game.name, game.description, game.price, game.genre, game.release_date, game_id)
    )
    connection.commit()
    updated = cursor.rowcount
    connection.close()
    return updated > 0

def delete_game(game_id: int) -> bool:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM games WHERE id = ?", (game_id,))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()
    return deleted > 0
# ...existing code...