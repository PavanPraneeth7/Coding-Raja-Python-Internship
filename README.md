# Coding-Raja-Python-Internship

# To-Do List Application

This is a simple To-Do List application written in Python. It allows users to add tasks, remove tasks, mark tasks as completed, display tasks, and delete completed tasks.

## Usage

To run the application, execute the following command in your terminal:

```bash
python3 todo.py
```


# Functionality
Add Task: Users can add a new task to the to-do list. They need to provide the task name, priority (high/medium/low), and due date (YYYY-MM-DD).

Remove Task: Users can remove a task from the to-do list by entering the task name.

Mark Task as Completed: Users can mark a task as completed by entering the task name.

Display Tasks: Users can view all tasks in the to-do list, sorted by priority and due date. Overdue tasks are highlighted in red.

Delete Completed Tasks: Users can delete all completed tasks from the to-do list.


# Configuration
The application uses a configuration file named config.ini for customization. Follow these steps to create the config.ini file:

Create a new file named config.ini in the same directory as the todo.py script.

Open the config.ini file in a text editor.

Add the following content to the config.ini file:

```bash
 [colors]
overdue_color = \033[91m
```


In this configuration, overdue_color specifies the color code for highlighting overdue tasks. The default value is \033[91m, which represents red color.

Dependencies
The application requires the following dependencies:

Python 3.x
sqlite3 (Python Standard Library)


Author
Praneeth

Contact
praneethkatakam143@gmail.com




