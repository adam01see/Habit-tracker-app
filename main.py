import questionary
from db import get_db, create_tables, delete_habit
from habit import Habit
from analyse import get_all_habits, get_all_daily_habits, get_all_weekly_habits, get_longest_streak, get_longest_daily_streak, get_longest_weekly_streak, get_all_streaks, get_all_daily_streaks, get_all_weekly_streaks


def cli():
    db = get_db("main.db")
    
    create_tables(db)

    questionary.confirm("Start the app?").ask()

    stop = False
    while not stop:

        choice = questionary.select(
            "What do you want to do?",
            choices=["create habit", "delete habit", "complete habit", "analyse habits", "exit"]
        ).ask()

        if choice == "create habit":
            name = questionary.text("What is the name of the habit?").ask()
            description = questionary.text("What is the description of the habit?").ask()
            period = questionary.select(
                "What is the period of the habit?",
                choices=["daily", "weekly"]
            ).ask()
            habit = Habit(name, description, period)
            habit.create_habit(db)

        elif choice == "delete habit":
            # Get list of available habit names
            all_habits = get_all_habits(db)
            available_names = [habit[0] for habit in all_habits]
            
            if not available_names:
                print("No habits found in the database.")
                continue
            
            # Keep asking until valid habit name is entered
            while True:
                name = questionary.text("Name of the habit to delete?").ask()
                
                if name in available_names:
                    delete_habit(db, name)
                    print(f"Habit '{name}' deleted successfully.")
                    break
                else:
                    print(f"Habit '{name}' does not exist.")
                    print("Available habits:")
                    for i, habit_name in enumerate(available_names, 1):
                        print(f"  {i}. {habit_name}")
                    print()  # Empty line for readability

        elif choice == "complete habit":
            # Get list of available habit names
            all_habits = get_all_habits(db)
            available_names = [habit[0] for habit in all_habits]
            
            if not available_names:
                print("No habits found in the database.")
                continue
            
            # Keep asking until valid habit name is entered
            while True:
                name = questionary.text("Name of the habit to complete today?").ask()
                
                if name in available_names:
                    habit = Habit(name, "", "daily")
                    habit.complete(db)
                    print(f"Recorded completion for '{name}'.")
                    break
                else:
                    print(f"Habit '{name}' does not exist.")
                    print("Available habits:")
                    for i, habit_name in enumerate(available_names, 1):
                        print(f"  {i}. {habit_name}")
                    print()  # Empty line for readability

        elif choice == "exit":
            print("exiting...")
            stop = True 

        elif choice == "analyse habits":
            choice = questionary.select(
                "What do you want to analyse?",
                choices=["get all habits", "get all daily habits", "get all weekly habits", "show streak of a habit", "get longest streak", "get longest daily streak", "get longest weekly streak", "get all streaks", "get all daily streaks", "get all weekly streaks", "back"]
            ).ask()
            if choice == "get all habits":
                habits = get_all_habits(db)
                print(habits)
            elif choice == "get all daily habits":
                habits = get_all_daily_habits(db)
                print(habits)
            elif choice == "get all weekly habits":
                habits = get_all_weekly_habits(db)
                print(habits)
            elif choice == "get longest streak":
                longest_streak = get_longest_streak(db)
                print(longest_streak)
            elif choice == "get longest daily streak":
                longest_daily_streak = get_longest_daily_streak(db)
                print(longest_daily_streak)
            elif choice == "get longest weekly streak":
                longest_weekly_streak = get_longest_weekly_streak(db)
                print(longest_weekly_streak)
            elif choice == "get all streaks":
                streaks = get_all_streaks(db)
                print(streaks)
            elif choice == "get all daily streaks":
                daily_streaks = get_all_daily_streaks(db)
                print(daily_streaks)
            elif choice == "get all weekly streaks":
                weekly_streaks = get_all_weekly_streaks(db)
                print(weekly_streaks)
            elif choice == "back":
                continue
            elif choice == "show streak of a habit":
                # Get list of available habit names
                all_habits = get_all_habits(db)
                available_names = [habit[0] for habit in all_habits]
                
                if not available_names:
                    print("No habits found in the database.")
                    continue
                # Keep asking until valid habit name is entered
                while True:
                    name = questionary.text("Name of the habit to show streak for?").ask()
                    
                    if name in available_names:
                        habit = Habit(name, "", "daily")
                        streak = habit.streak(db)
                        print(f"Current streak for '{name}': {streak}")
                        break
                    else:
                        print(f"Habit '{name}' does not exist.")
                        print("Available habits:")
                        for i, habit_name in enumerate(available_names, 1):
                            print(f"  {i}. {habit_name}")
                        print()  # Empty line for readability

        

if __name__ == '__main__':
    cli()
