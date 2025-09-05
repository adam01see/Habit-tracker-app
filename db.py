import sqlite3
from datetime import date


def get_db(name = "main.db"):
    """
    Creates a connection to the database

    :param name: name of the database
    :return db: returns the database connection
    """
    db = sqlite3.connect(name)
    return db


def create_tables(db):
    """
    Creates tables in the database

    :param db: an initialized sqlite3 database connection
    """
    cur = db.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS habit_list (
                name TEXT PRIMARY KEY,
                description TEXT,
                period TEXT
        )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS streak (
                date TEXT,
                habitName TEXT,
                FOREIGN KEY (habitName) REFERENCES habit_list(name)
        )"""
    )
    # Ensure one completion per day per habit
    cur.execute(
        """CREATE UNIQUE INDEX IF NOT EXISTS idx_streak_unique
            ON streak(date, habitName)
        """
    )
    db.commit()


def add_habit(db, name, description, period):
    """
    Function that adds new habit to the database

    :param db: an initialized sqlite3 database connection
    :param name: name of the habit
    :param description: description of the habit
    :param period: period of the habit (daily/weekly)
    """
    cur = db.cursor()
    cur.execute(
        "INSERT INTO habit_list (name, description, period) VALUES (?, ?, ?)",
        (name, description, period),
    )
    db.commit()


def delete_habit(db, name):
    """
    Function that deletes habit and its streak history from the database

    :param db: an initialized sqlite3 database connection
    :param name: name of the habit
    """
    cur = db.cursor()
    cur.execute("DELETE FROM streak WHERE habitName = ?", (name,))
    cur.execute("DELETE FROM habit_list WHERE name = ?", (name,))
    db.commit()


def complete_habit(db, name, when: str | None = None):
    """
    Record a completion for the habit on the given date (YYYY-MM-DD).
    If no date is provided, uses today's date.
    """
    completion_date = when or date.today().isoformat()
    cur = db.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO streak (date, habitName) VALUES (?, ?)",
        (completion_date, name),
    )
    db.commit()