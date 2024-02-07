import sqlite3
from sqlite3 import Connection, Cursor

PATH = "./liked_words.db"


def connect() -> tuple[Connection, Cursor]:
    con = sqlite3.connect(PATH)
    cur = con.cursor()
    return con, cur


def initialize():
    con, cur = connect()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "liked_words"  (
            "index"	INTEGER UNIQUE,
            "word"	TEXT,
            PRIMARY KEY("index" AUTOINCREMENT)
        );
    """)

    con.commit()
    con.close()


def add_word(word: str):
    con, cur = connect()
    cur.execute("INSERT INTO liked_words (word) VALUES (?)", (word,))
    con.commit()
    con.close()


def remove_word(word: str):
    con, cur = connect()
    cur.execute("DELETE FROM liked_words WHERE word=(?)", (word,))
    con.commit()
    con.close()
