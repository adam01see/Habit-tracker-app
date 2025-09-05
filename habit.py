from db import add_habit, delete_habit, complete_habit
from analyse import get_streak


class Habit:
  
    def __init__(self, name: str, description: str, period: str):
        """
        Class for a habit
    
        :param self: self instance
        :param name: name of the habit
        :param description: description of the habit
        :param period: Periodicity of the habit (daily/weekly)
        """
        self.name = name
        self.description = description
        self.period = period 

    def create_habit(self, db):
        """
        Function that adds new habit to the database

        :param self: self instance
        :param db: an initialized sqlite3 database connection
        """
        add_habit(db, self.name, self.description, self.period)

    def delete_habit(self, db):
        """
        Function that deletes habit from the database

        :param self: self instance
        :param db: an initialized sqlite3 database connection
        """
        delete_habit(db, self.name)

    def complete(self, db):
        """Record completion for today for this habit."""
        complete_habit(db, self.name)

    def streak(self, db) -> int:
        """Return current streak length for this habit."""
        return get_streak(db, self.name)




    
