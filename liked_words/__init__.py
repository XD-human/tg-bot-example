import sqlite3


class LikedWordsManager:
    path = "../liked_words.db"
    con = sqlite3.connect(path)
    cur = con.cursor()

    @classmethod
    def initialize(cls):
        cls.cur.execute("""
            CREATE TABLE "liked_words" (
                "index"	INTEGER UNIQUE,
                "word"	TEXT,
                PRIMARY KEY("index" AUTOINCREMENT)
            );
        """)
        cls.con.commit()

    @classmethod
    def add_word(cls, word: str):
        cls.cur.execute("INSERT INTO liked_words (word) VALUES (?)", (word,))
        cls.con.commit()

    @classmethod
    def remove_word(cls, word: str):
        cls.cur.execute("DELETE FROM liked_words WHERE word=(?)", (word,))
        cls.con.commit()


if __name__ == "__main__":
    LikedWordsManager.remove_word("слово")
    LikedWordsManager.con.close()
