import argparse
import configparser
import datetime
import sqlite3
from collections import defaultdict
from sqlite3 import register_adapter

# Register an adapter for date objects
def adapt_date(date):
    return date.isoformat()

register_adapter(datetime.date, adapt_date)

# Load configuration
config = configparser.ConfigParser()
config.read("config.ini")
overdue_color = config.get("colors", "overdue_color", fallback="\033[91m")  # Red color by default

conn = sqlite3.connect("tasks.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, priority TEXT, due_date TEXT, completed INTEGER)""")

priorities = ["high", "medium", "low"]

def validate_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return None

def validate_task_name(name):
    if not name.strip():
        print("Task name cannot be empty.")
        return False
    return True

def add_task(name, priority, due_date):
    if not validate_task_name(name):
        return

    if priority not in priorities:
        print(f"Invalid priority. Please use one of: {', '.join(priorities)}")
        return

    due_date = validate_date(due_date)
    if due_date is None:
        return

    try:
        c.execute("INSERT INTO tasks (name, priority, due_date, completed) VALUES (?, ?, ?, 0)", (name, priority, due_date))
        conn.commit()
        print("Task added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding task: {e}")

def remove_task(name):
    try:
        c.execute("DELETE FROM tasks WHERE name = ?", (name,))
        conn.commit()
        if c.rowcount == 0:
            print("Task not found.")
        else:
            print("Task removed successfully.")
    except sqlite3.Error as e:
        print(f"Error removing task: {e}")

def mark_completed(name):
    try:
        c.execute("UPDATE tasks SET completed = 1 WHERE name = ?", (name,))
        conn.commit()
        if c.rowcount == 0:
            print("Task not found.")
        else:
            print("Task marked as completed.")
    except sqlite3.Error as e:
        print(f"Error marking task as completed: {e}")

def delete_completed_tasks():
    try:
        c.execute("DELETE FROM tasks WHERE completed = 1")
        conn.commit()
        print("Completed tasks deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting completed tasks: {e}")

def display_tasks():
    tasks = defaultdict(list)
    try:
        for row in c.execute("SELECT * FROM tasks ORDER BY priority, due_date"):
            task = {"id": row[0], "name": row[1], "priority": row[2], "due_date": row[3], "completed": bool(row[4])}
            tasks[row[2]].append(task)
    except sqlite3.Error as e:
        print(f"Error fetching tasks: {e}")
        return

    if not any(tasks.values()):
        print("No tasks found.")
        return

    overdue_tasks = []
    for priority, task_list in tasks.items():
        print(f"\n{priority.capitalize()} priority tasks:")
        for task in sorted(task_list, key=lambda x: x["due_date"]):
            status = "Completed" if task["completed"] else "Pending"
            due_date_str = task["due_date"]
            if not task["completed"] and datetime.datetime.strptime(task["due_date"], "%Y-%m-%d").date() < datetime.date.today():
                overdue_tasks.append(task)
                due_date_str = f"{overdue_color}{due_date_str}\033[0m"
            print(f"- {task['name']} (Due: {due_date_str}) - {status}")

    if overdue_tasks:
        print(f"\n\033[93mOverdue tasks ({overdue_color}overdue dates\033[0m\033[93m):\033[0m")
        for task in overdue_tasks:
            print(f"- {task['name']} (Due: {overdue_color}{task['due_date']}\033[0m)")

def main():
    while True:
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Mark Task as Completed")
        print("4. Display Tasks")
        print("5. Delete Completed Tasks")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            name = input("Enter task name: ")
            priority = input("Enter task priority (high/medium/low): ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            add_task(name, priority, due_date)
        elif choice == '2':
            name = input("Enter task name to remove: ")
            remove_task(name)
        elif choice == '3':
            name = input("Enter task name to mark as completed: ")
            mark_completed(name)
        elif choice == '4':
            display_tasks()
        elif choice == '5':
            delete_completed_tasks()
        elif choice == '6':
            print("Exiting the To-Do List Application.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
 
