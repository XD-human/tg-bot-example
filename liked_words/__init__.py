import sqlite3
from sqlite3 import Connection, Cursor
from typing import Optional

import liked_words.sql_result

DEFAULT_PATH = "./liked_words.db"


def connect(path=DEFAULT_PATH) -> tuple[Connection, Cursor]:
    con = sqlite3.connect(path)
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


def try_add_word(chat_id: int, word: str):
    con, cur = connect()
    current_words = get_words(chat_id)

    if current_words is None:
        cur.execute("INSERT INTO liked_words (chatId, words) VALUES (?, ?)", (chat_id, word))
        result = sql_result.AdditionResult.success()

    else:
        if word not in current_words:
            current_words.append(word)
            string_repr = "&".join(current_words)
            cur.execute("UPDATE liked_words SET words=(?) WHERE chatId=(?)", (string_repr, chat_id))
            result = sql_result.AdditionResult.success()
        else:
            result = sql_result.AdditionResult.error(f"Слово уже находится в избранных пользователя")

    con.commit()
    con.close()
    return result


def try_remove_word(chat_id: int, word: str):
    con, cur = connect()
    current_words = get_words(chat_id)

    if current_words is not None:
        if word in current_words:
            current_words.remove(word)
            string_repr = "&".join(current_words)
            cur.execute("UPDATE liked_words SET words=(?) WHERE chatId=(?)", (string_repr, chat_id))
            result = sql_result.RemovingResult.success()
        else:
            result = sql_result.RemovingResult.error("Слово не находится в избранных у пользователя")
    else:
        result = sql_result.RemovingResult.error("Пользователь ещё не сохранял в избранных ни одного слова")

    con.commit()
    con.close()
    return result


def get_words(chat_id: int) -> Optional[list[str]]:
    con, cur = connect()
    cur.execute("SELECT words FROM liked_words WHERE chatId=(?)", (chat_id,))
    data = cur.fetchone()

    if data is None:
        return None

    words = data[0].split("&")
    return words
