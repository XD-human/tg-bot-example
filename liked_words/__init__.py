import sqlite3
from sqlite3 import Connection, Cursor
from typing import Optional

DEFAULT_PATH = "../liked_words.db"


def connect(path=DEFAULT_PATH) -> tuple[Connection, Cursor]:
    con = sqlite3.connect(DEFAULT_PATH)
    cur = con.cursor()
    return con, cur


def initialize():
    con, cur = connect()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "liked_words"  (
            "chatId"	INTEGER UNIQUE,
            "words"	TEXT,
            PRIMARY KEY("chatId")
        );
    """)

    con.commit()
    con.close()


def add_word(chat_id: int, word: str):
    con, cur = connect()
    current_words = get_words(chat_id)
    if current_words is None:
        cur.execute("INSERT INTO liked_words (chatId, words) VALUES (?, ?)", (chat_id, word))
    else:
        current_words.append(word)
        string_repr = "&".join(current_words)
        cur.execute("UPDATE liked_words SET words=(?) WHERE chatId=(?)", (string_repr, chat_id))
    con.commit()
    con.close()


def remove_word(word: str):
    con, cur = connect()
    cur.execute("DELETE FROM liked_words WHERE words=(?)", (word,))
    con.commit()
    con.close()


def get_words(chat_id: int) -> Optional[list[str]]:
    con, cur = connect()
    cur.execute("SELECT words FROM liked_words WHERE chatId=(?)", (chat_id,))
    data = cur.fetchone()

    if data is None:
        return None

    words = data[0].split("&")
    return words


if __name__ == "__main__":
    initialize()
    add_word(2, "что-то")
