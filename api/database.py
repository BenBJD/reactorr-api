import sqlite3


def create_db():
    db = sqlite3.connect("db.sqlite")
    cursor = db.cursor()
    table_create_script = [
        """
            create table config
            (
                key string
                    constraint settings_pk
                        primary key,
                value string
            );
        """,
        """
            INSERT INTO config (key, value) VALUES ("jackett_url", "");
        """,
        """
            INSERT INTO config (key, value) VALUES ("jackett_apikey", "");
        """,
        """
            CREATE TABLE recent
            (
                id integer
                    constraint recent_pk
                        primary key autoincrement,
                search text
            )
        """
    ]
    for i in table_create_script:
        cursor.execute(i)
    db.commit()
    db.close()


def get_config(key: str):
    db = sqlite3.connect("db.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT value FROM config WHERE key = '{key}'")
    config = cursor.fetchone()[0]
    db.close()
    return config


def set_config(key: str, value: str):
    db = sqlite3.connect("db.sqlite")
    cursor = db.cursor()
    cursor.execute(f"UPDATE config SET value = '{value}' WHERE key = '{key}'")
    db.commit()
    db.close()
    return "success"


def get_recents(number: int):
    db = sqlite3.connect("db.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM recent ORDER BY id LIMIT {number}")
    recents = cursor.fetchall()
    db.close()
    return recents


def add_recent(search: str):
    db = sqlite3.connect("db.sqlite")
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO recent (search) VALUES ('{search}')")
    db.commit()
    db.close()
    return "success"


def remove_recent(id: str, all: bool):
    db = sqlite3.connect("db.sqlite")
    cursor = db.cursor()
    if all:
        cursor.execute(f"DELETE FROM recent")
    else:
        cursor.execute(f"DELETE FROM recent WHERE id = {id}")
    db.commit()
    db.close
    return "success"
