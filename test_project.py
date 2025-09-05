import pytest
from datetime import date, timedelta

from db import get_db, create_tables, complete_habit
from habit import Habit
from analyse import get_streak


def setup_db():
    db = get_db(":test:")
    create_tables(db)
    return db


def test_daily_streak_two_consecutive_days():
    db = setup_db()
    h = Habit("daily_habit", "desc", "daily")
    h.create_habit(db)

    today = date.today()
    yesterday = today - timedelta(days=1)

    # complete yesterday and today
    complete_habit(db, h.name, when=yesterday.isoformat())
    complete_habit(db, h.name, when=today.isoformat())

    assert get_streak(db, h.name) == 2


def test_daily_streak_does_not_increase_with_gap():
    db = setup_db()
    h = Habit("daily_gap", "desc", "daily")
    h.create_habit(db)

    today = date.today()
    two_days_ago = today - timedelta(days=2)

    complete_habit(db, h.name, when=two_days_ago.isoformat())
    complete_habit(db, h.name, when=today.isoformat())

    # Gap breaks streak; only the most recent run counts
    assert get_streak(db, h.name) == 1


def test_daily_multiple_completions_same_day_count_once():
    db = setup_db()
    h = Habit("daily_dup", "desc", "daily")
    h.create_habit(db)

    today = date.today().isoformat()
    complete_habit(db, h.name, when=today)
    complete_habit(db, h.name, when=today)  # ignored by UNIQUE(date, habitName)

    assert get_streak(db, h.name) == 1


def test_weekly_streak_two_consecutive_weeks():
    db = setup_db()
    h = Habit("weekly_habit", "desc", "weekly")
    h.create_habit(db)

    # Find a date in current ISO week and one in the previous ISO week
    today = date.today()
    this_monday = today - timedelta(days=(today.isoweekday() - 1))
    last_monday = this_monday - timedelta(days=7)

    # Complete once in each week
    complete_habit(db, h.name, when=last_monday.isoformat())
    complete_habit(db, h.name, when=this_monday.isoformat())

    assert get_streak(db, h.name) == 2

