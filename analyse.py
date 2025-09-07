from datetime import date, datetime, timedelta


def get_all_habits(db):
    """
    Function that gets all habits from the database

    :param db: an initialized sqlite3 database connection
    :return: a list of all habits
    """
    cursor = db.cursor()
    cursor.execute("SELECT * FROM habit_list")
    return cursor.fetchall()


def get_all_daily_habits(db):
    """
    Function that gets all daily habits from the database

    :param db: an initialized sqlite3 database connection
    :return: a list of all daily habits
    """
    cursor = db.cursor()
    cursor.execute("SELECT * FROM habit_list WHERE period = 'daily'")
    return cursor.fetchall()


def get_all_weekly_habits(db):
    """
    Function that gets all weekly habits from the database

    :param db: an initialized sqlite3 database connection
    :return: a list of all weekly habits
    """
    cursor = db.cursor()
    cursor.execute("SELECT * FROM habit_list WHERE period = 'weekly'")
    return cursor.fetchall()


def _get_habit_period(db, name: str) -> str | None:
    """
    Function that gets the period of a habit from the database

    :param db: an initialized sqlite3 database connection
    :param name: the name of the habit
    :return: the period of the habit
    """
    cur = db.cursor()
    cur.execute("SELECT period FROM habit_list WHERE name = ?", (name,))
    row = cur.fetchone()
    return row[0] if row else None


def get_streak(db, name: str) -> int:
    """
    Function that gets the streak of a habit from the database

    :param db: an initialized sqlite3 database connection
    :param name: the name of the habit
    :return: the streak of the habit
    """
    # Selects all dates from the table "streak" of a habit and orders them by date in ascending order
    period = _get_habit_period(db, name)
    if not period:
        return 0

    cur = db.cursor()
    cur.execute(
        "SELECT date FROM streak WHERE habitName = ? ORDER BY date ASC",
        (name,)
    )
    rows = cur.fetchall()
    if not rows:
        return 0

    # Loops through the list of dates and converts them from string to date object
    dates: list[date] = []
    for (date_str,) in rows:
        try:
            dates.append(datetime.strptime(date_str, "%Y-%m-%d").date())
        except ValueError:
            continue

    if not dates:
        return 0

    # Removes duplicates by making a sorted list of unique dates
    dates = sorted(set(dates))

    # Calculates the streak for daily habits by going through the list of dates and checking if the difference between the current date and the previous date is 1 day
    if period == "daily":
        streak = 1
        for i in range(len(dates) - 1, 0, -1):  
            if dates[i] - dates[i-1] == timedelta(days=1):
                streak += 1
            else:
                break
        return streak

    # Calculates the streak for weekly habits by going through the list of dates and checking if the difference between the current date and the previous date is 7 days
    if period == "weekly":
        # Converts each date to the Monday of that ISO week
        weeks = [d - timedelta(days=d.weekday()) for d in dates]
        weeks = sorted(set(weeks))

        streak = 1
        for i in range(len(weeks) - 1, 0, -1):  
            if weeks[i] - weeks[i-1] == timedelta(days=7):
                streak += 1
            else:
                break
        return streak

    return 0


def get_all_streaks(db):
    """
    Return a list of (name, streak) for all habits.
    """
    cur = db.cursor()
    cur.execute("SELECT name FROM habit_list")
    names = [row[0] for row in cur.fetchall()]
    return [(name, get_streak(db, name)) for name in names]


def get_longest_streak(db):
    """
    Return (name, streak) for the habit with the longest current streak.
    Returns (None, 0) if there are no habits.
    """
    all_streaks = get_all_streaks(db)
    if not all_streaks:
        return (None, 0)
    return max(all_streaks, key=lambda x: x[1])


def get_all_daily_streaks(db):
    """
    Return a list of (name, streak) for all daily habits.
    """
    cur = db.cursor()
    cur.execute("SELECT name FROM habit_list WHERE period = 'daily'")
    names = [row[0] for row in cur.fetchall()]
    return [(name, get_streak(db, name)) for name in names]


def get_all_weekly_streaks(db):
    """
    Return a list of (name, streak) for all weekly habits.
    """
    cur = db.cursor()
    cur.execute("SELECT name FROM habit_list WHERE period = 'weekly'")
    names = [row[0] for row in cur.fetchall()]
    return [(name, get_streak(db, name)) for name in names]


def get_longest_daily_streak(db):
    """
    Return (name, streak) for the daily habit with the longest current streak.
    Returns (None, 0) if there are no daily habits.
    """
    streaks = get_all_daily_streaks(db)
    if not streaks:
        return (None, 0)
    return max(streaks, key=lambda x: x[1])


def get_longest_weekly_streak(db):
    """
    Return (name, streak) for the weekly habit with the longest current streak.
    Returns (None, 0) if there are no weekly habits.
    """
    streaks = get_all_weekly_streaks(db)
    if not streaks:
        return (None, 0)
    return max(streaks, key=lambda x: x[1])

def get_longest_historical_streak(db):
    """
    Return (name, streak) for the habit with the longest historical streak.
    Returns (None, 0) if there are no habits.
    """
    all_streaks = get_all_streaks(db)
    if not all_streaks:
        return (None, 0)
    return max(all_streaks, key=lambda x: x[1])