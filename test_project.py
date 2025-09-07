import pytest
from db import get_db, create_tables
from analyse import (
    get_all_habits,
    get_all_daily_habits,
    get_all_weekly_habits,
    get_streak,
    get_longest_streak,
    get_longest_daily_streak,
    get_longest_weekly_streak,
    get_all_streaks,
    get_all_daily_streaks,
    get_all_weekly_streaks,
    get_longest_historical_streak,
)
"""
This file contains tests of the analyse functions for the project.
"""

DAILY = ["morning_jog", "meditation", "read_books", "drink_water", "code_practice"]
WEEKLY = ["gym_workout", "meal_prep", "family_time", "house_cleaning", "hobby_project"]

"""
with scope="module" making sure to run tear down after the tests are done
"""
@pytest.fixture(scope="module")
def db():
    conn = get_db("test.db")
    create_tables(conn)
    yield conn
    conn.close()

def test_get_all_habits(db):
    """
    Test that the get_all_habits function returns a list of habits

    :param db: an initialized sqlite3 database connection
    :return: a list of all habits
    """
    habits = get_all_habits(db)
    assert isinstance(habits, list)
    assert len(habits) >= 0

def test_get_all_daily_habits(db):
    """
    Test that the get_all_daily_habits function returns a list of daily habits

    :param db: an initialized sqlite3 database connection
    :return: a list of all daily habits
    """
    habits = get_all_daily_habits(db)
    assert isinstance(habits, list)
    assert len(habits) >= 0

def test_get_all_weekly_habits(db):
    """
    Test that the get_all_weekly_habits function returns a list of weekly habits

    :param db: an initialized sqlite3 database connection
    :return: a list of all weekly habits
    """
    habits = get_all_weekly_habits(db)
    assert isinstance(habits, list)

def test_get_streak(db):
    """
    Test that the get_streak function returns the streak for a habit

    :param db: an initialized sqlite3 database connection
    :return: the streak for a habit
    """
    streak = get_streak(db, "morning_jog")
    assert isinstance(streak, int)
    assert streak >= 0
    
def test_get_all_streaks(db):
    """
    Test that the get_all_streaks function returns a list of streaks

    :param db: an initialized sqlite3 database connection
    :return: a list of all streaks
    """
    streaks = get_all_streaks(db)
    assert isinstance(streaks, list)
    assert len(streaks) >= 0

def test_get_all_daily_streaks(db):
    """
    Test that the get_all_daily_streaks function returns a list of daily streaks

    :param db: an initialized sqlite3 database connection
    :return: a list of all daily streaks
    """
    streaks = get_all_daily_streaks(db)
    assert isinstance(streaks, list)
    assert len(streaks) >= 0

def test_get_all_weekly_streaks(db):
    """
    Test that the get_all_weekly_streaks function returns a list of weekly streaks

    :param db: an initialized sqlite3 database connection
    :return: a list of all weekly streaks
    """
    streaks = get_all_weekly_streaks(db)
    assert isinstance(streaks, list)
    assert len(streaks) >= 0

def test_get_longest_streak(db):
    """
    Test that the get_longest_streak function returns the longest streak

    :param db: an initialized sqlite3 database connection
    :return: the longest streak
    """
    name, s = get_longest_streak(db)
    assert (name is None) or isinstance(name, str)
    assert isinstance(s, int)
    assert s >= 0

def test_get_longest_daily_streak(db):
    """
    Test that the get_longest_daily_streak function returns the longest daily streak

    :param db: an initialized sqlite3 database connection
    :return: the longest daily streak
    """
    name, s = get_longest_daily_streak(db)
    assert (name is None) or isinstance(name, str)
    assert isinstance(s, int)
    assert s >= 0

def test_get_longest_weekly_streak(db):
    """
    Test that the get_longest_weekly_streak function returns the longest weekly streak

    :param db: an initialized sqlite3 database connection
    :return: the longest weekly streak
    """
    name, s = get_longest_weekly_streak(db)
    assert (name is None) or isinstance(name, str)
    assert isinstance(s, int)
    assert s >= 0

def test_get_longest_historical_streak(db):
    """
    Test that the get_longest_historical_streak function returns the longest historical streak

    :param db: an initialized sqlite3 database connection
    :return: the longest historical streak
    """
    name, s = get_longest_historical_streak(db)
    assert (name is None) or isinstance(name, str)
    assert isinstance(s, int)
    assert s >= 0
