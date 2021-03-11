import sqlite3


def create_db():
    db = sqlite3.connect("db.sqlite")
    cursor = db.cursor()
    table_create_script = [
        """
            CREATE TABLE config (
                key STRING NOT NULL PRIMARY KEY,
                value STRING
            );
        """,
        """
            INSERT INTO config (key, value) VALUES ("jackett_url", "")
        """,
        """
            INSERT INTO config (key, value) VALUES ("jackett_apikey", "")
        """
        ]
    for i in table_create_script:
        cursor.execute(i)
    db.commit()
    db.close()


def read_config(key):
    db = sqlite3.connect("db.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT value FROM config WHERE key = '{key}'")
    config = cursor.fetchone()[0]
    db.close()
    return config


def update_config(key, value):
    db = sqlite3.connect("db.sqlite")
    cursor = db.cursor()
    cursor.execute(f"UPDATE config SET value = '{value}' WHERE key = '{key}'")
    db.commit()
    db.close()
    print("success")