"""
Task Manager (Capstone Project)

This program allows users to log in and manage tasks stored in tasks.txt and
users stored in user.txt.

Admin user (default):
    username: admin
    password: password

Features:
- Register users (admin only) with duplicate-username prevention
- Add tasks
- View all tasks
- View tasks assigned to the current user (with task selection)
  - Mark task complete
  - Edit task assignee or due date (only if not completed)
- Generate reports (task_overview.txt and user_overview.txt)
- Display statistics by reading the generated reports (auto-generate if missing)

Make sure you open/run this program from the folder that contains:
- task_manager.py
- user.txt
- tasks.txt
"""

# ===== importing libraries =====
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


# ----------------------------
# File helpers / data loading
# ----------------------------
def ensure_default_files_exist():
    """Create tasks.txt and user.txt if they do not exist."""
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w", encoding="utf-8") as f:
            pass

    if not os.path.exists("user.txt"):
        with open("user.txt", "w", encoding="utf-8") as f:
            f.write("admin;password")


def load_users():
    """Load users from user.txt into a dict: {username: password}."""
    username_password = {}
    with open("user.txt", "r", encoding="utf-8") as user_file:
        lines = [line.strip() for line in user_file.readlines() if line.strip()]

    for line in lines:
        username, password = line.split(";")
        username_password[username] = password
    return username_password


def save_users(username_password):
    """Write users dict back to user.txt."""
    user_lines = [f"{u};{p}" for u, p in username_password.items()]
    with open("user.txt", "w", encoding="utf-8") as out_file:
        out_file.write("\n".join(user_lines))


def load_tasks():
    """Load tasks from tasks.txt into a list of dicts."""
    with open("tasks.txt", "r", encoding="utf-8") as task_file:
        task_data = [t for t in task_file.read().split("\n") if t.strip()]

    task_list = []
    for task in task_data:
        task_components = task.split(";")
        current_task = {
            "username": task_components[0],
            "title": task_components[1],
            "description": task_components[2],
            "due_date": datetime.strptime(task_components[3], DATETIME_STRING_FORMAT),
            "assigned_date": datetime.strptime(task_components[4], DATETIME_STRING_FORMAT),
            "completed": task_components[5] == "Yes",
        }
        task_list.append(current_task)

    return task_list


def save_tasks(task_list):
    """Write tasks list back to tasks.txt."""
    task_list_to_write = []
    for task in task_list:
        str_attrs = [
            task["username"],
            task["title"],
            task["description"],
            task["due_date"].strftime(DATETIME_STRING_FORMAT),
            task["assigned_date"].strftime(DATETIME_STRING_FORMAT),
            "Yes" if task["completed"] else "No",
        ]
        task_list_to_write.append(";".join(str_attrs))

    with open("tasks.txt", "w", encoding="utf-8") as task_file:
        task_file.write("\n".join(task_list_to_write))


# ----------------------------
# Display helpers
# ----------------------------
def format_task(task, task_number=None):
    """Return a nicely formatted task string."""
    num_line = f"Task Number: \t {task_number}\n" if task_number is not None else ""
    return (
        f"{num_line}"
        f"Task: \t\t {task['title']}\n"
        f"Assigned to: \t {task['username']}\n"
        f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        f"Task Complete: \t {'Yes' if task['completed'] else 'No'}\n"
        f"Task Description: \n {task['description']}\n"
    )


# ----------------------------
# Required functions
# ----------------------------
def reg_user(username_password):
    """Register a new user (admin only). Prevent duplicate usernames."""
    while True:
        new_username = input("New Username: ").strip()
        if new_username in username_password:
            print("That username already exists. Please choose a different username.")
            continue

        new_password = input("New Password: ").strip()
        confirm_password = input("Confirm Password: ").strip()

        if new_password != confirm_password:
            print("Passwords do not match. Please try again.")
            continue

        username_password[new_username] = new_password
        save_users(username_password)
        print("New user added.")
        break


def add_task(task_list, username_password):
    """Add a new task to tasks.txt."""
    task_username = input("Name of person assigned to task: ").strip()
    if task_username not in username_password:
        print("User does not exist. Please enter a valid username.")
        return

    task_title = input("Title of Task: ").strip()
    task_description = input("Description of Task: ").strip()

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ").strip()
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    current_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": current_date,
        "completed": False,
    }

    task_list.append(new_task)
    save_tasks(task_list)
    print("Task successfully added.")


def view_all(task_list):
    """View all tasks."""
    if not task_list:
        print("No tasks found.")
        return

    for task in task_list:
        print(format_task(task))
        print("-" * 40)


def view_mine(task_list, current_user, username_password):
    """
    View tasks assigned to the current user.
    Allow selecting a task number to mark complete or edit.
    """
    my_tasks = [t for t in task_list if t["username"] == current_user]

    if not my_tasks:
        print("You have no tasks assigned to you.")
        return

    # Display tasks with numbers (based on their index in the full task_list)
    my_task_indices = []
    print("\nYour Tasks")
    print("-" * 40)
    for idx, task in enumerate(task_list):
        if task["username"] == current_user:
            my_task_indices.append(idx)
            display_number = len(my_task_indices)  # 1..n for user's view
            print(format_task(task, task_number=display_number))
            print("-" * 40)

    while True:
        choice = input("Enter a task number to select a task, or -1 to return to the menu: ").strip()

        if choice == "-1":
            return

        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        task_choice_num = int(choice)
        if task_choice_num < 1 or task_choice_num > len(my_task_indices):
            print("That task number is not valid.")
            continue

        # Map user's selection number to actual index in task_list
        task_index_in_task_list = my_task_indices[task_choice_num - 1]
        selected_task = task_list[task_index_in_task_list]

        print("\nSelected Task")
        print("-" * 40)
        print(format_task(selected_task, task_number=task_choice_num))
        print("-" * 40)

        action = input("Choose an option:\n"
                       "mc - mark complete\n"
                       "ed - edit task\n"
                       "b  - back\n"
                       ": ").lower().strip()

        if action == "b":
            continue

        if action == "mc":
            if selected_task["completed"]:
                print("This task is already marked as complete.")
                continue
            selected_task["completed"] = True
            save_tasks(task_list)
            print("Task marked as complete.")
            continue

        if action == "ed":
            if selected_task["completed"]:
                print("You cannot edit a task that has been completed.")
                continue

            edit_choice = input("Edit:\n"
                                "u - change assigned user\n"
                                "d - change due date\n"
                                "b - back\n"
                                ": ").lower().strip()

            if edit_choice == "b":
                continue

            if edit_choice == "u":
                new_user = input("Enter the new username to assign this task to: ").strip()
                if new_user not in username_password:
                    print("That user does not exist.")
                    continue
                selected_task["username"] = new_user
                save_tasks(task_list)
                print("Task reassigned successfully.")
                continue

            if edit_choice == "d":
                while True:
                    new_due = input("Enter the new due date (YYYY-MM-DD): ").strip()
                    try:
                        selected_task["due_date"] = datetime.strptime(new_due, DATETIME_STRING_FORMAT)
                        save_tasks(task_list)
                        print("Due date updated successfully.")
                        break
                    except ValueError:
                        print("Invalid date format. Please use YYYY-MM-DD.")
                continue

            print("Invalid edit option.")
            continue

        print("Invalid option. Please choose again.")


# ----------------------------
# Reports and statistics
# ----------------------------
def generate_reports(task_list, username_password):
    """Generate task_overview.txt and user_overview.txt."""
    total_tasks = len(task_list)
    total_completed = sum(1 for t in task_list if t["completed"])
    total_uncompleted = total_tasks - total_completed

    today = date.today()
    overdue_uncompleted = sum(
        1 for t in task_list
        if (not t["completed"]) and (t["due_date"].date() < today)
    )

    pct_incomplete = (total_uncompleted / total_tasks * 100) if total_tasks else 0
    pct_overdue = (overdue_uncompleted / total_tasks * 100) if total_tasks else 0

    # --- task_overview.txt ---
    task_overview_lines = [
        "TASK OVERVIEW",
        "-" * 40,
        f"Total tasks:\t\t\t {total_tasks}",
        f"Completed tasks:\t\t {total_completed}",
        f"Uncompleted tasks:\t\t {total_uncompleted}",
        f"Overdue uncompleted tasks:\t {overdue_uncompleted}",
        f"Percentage incomplete:\t\t {pct_incomplete:.2f}%",
        f"Percentage overdue:\t\t {pct_overdue:.2f}%",
        "-" * 40,
    ]
    with open("task_overview.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(task_overview_lines))

    # --- user_overview.txt ---
    users = list(username_password.keys())
    total_users = len(users)

    user_overview_lines = [
        "USER OVERVIEW",
        "-" * 40,
        f"Total users:\t\t {total_users}",
        f"Total tasks:\t\t {total_tasks}",
        "-" * 40,
    ]

    for user in users:
        user_tasks = [t for t in task_list if t["username"] == user]
        user_task_count = len(user_tasks)

        pct_of_all_tasks = (user_task_count / total_tasks * 100) if total_tasks else 0

        user_completed = sum(1 for t in user_tasks if t["completed"])
        user_uncompleted = user_task_count - user_completed

        pct_completed = (user_completed / user_task_count * 100) if user_task_count else 0
        pct_uncompleted = (user_uncompleted / user_task_count * 100) if user_task_count else 0

        user_overdue_uncompleted = sum(
            1 for t in user_tasks
            if (not t["completed"]) and (t["due_date"].date() < today)
        )
        pct_overdue_uncompleted = (user_overdue_uncompleted / user_task_count * 100) if user_task_count else 0

        user_overview_lines.extend([
            f"User: {user}",
            f"  Tasks assigned:\t\t {user_task_count}",
            f"  % of all tasks:\t\t {pct_of_all_tasks:.2f}%",
            f"  % completed:\t\t\t {pct_completed:.2f}%",
            f"  % to complete:\t\t {pct_uncompleted:.2f}%",
            f"  % overdue (uncompleted):\t {pct_overdue_uncompleted:.2f}%",
            "-" * 40,
        ])

    with open("user_overview.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(user_overview_lines))

    print("Reports generated: task_overview.txt and user_overview.txt")


def display_statistics(task_list, username_password):
    """
    Display statistics by reading task_overview.txt and user_overview.txt.
    If they do not exist, generate them first.
    """
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports(task_list, username_password)

    print("\n" + "=" * 50)
    print("STATISTICS")
    print("=" * 50)

    with open("task_overview.txt", "r", encoding="utf-8") as f:
        print("\n" + f.read())

    with open("user_overview.txt", "r", encoding="utf-8") as f:
        print(f.read())

    print("=" * 50 + "\n")


# ----------------------------
# Login and main program
# ----------------------------
def login(username_password):
    """Prompt the user to log in. Returns the username."""
    while True:
        print("LOGIN")
        current_user = input("Username: ").strip()
        current_pass = input("Password: ").strip()

        if current_user not in username_password:
            print("User does not exist")
            continue
        if username_password[current_user] != current_pass:
            print("Wrong password")
            continue

        print("Login Successful!")
        return current_user


def main():
    ensure_default_files_exist()

    username_password = load_users()
    task_list = load_tasks()

    current_user = login(username_password)

    while True:
        print()
        if current_user == "admin":
            menu = input(
                "please select one of the following options\n"
                "r - register user\n"
                "a - add task\n"
                "va - view all tasks\n"
                "vm - view my tasks\n"
                "gr - generate reports\n"
                "ds - display statistics\n"
                "e - exit\n"
                ": "
            ).lower().strip()
        else:
            menu = input(
                "Select one of the following Options below:\n"
                "a - Adding a task\n"
                "va - View all tasks\n"
                "vm - View my task\n"
                "e - Exit\n"
                ": "
            ).lower().strip()

        if menu == "r":
            if current_user != "admin":
                print("Only admin can register users.")
                continue
            reg_user(username_password)
            # reload users dict (optional, but keeps it consistent)
            username_password = load_users()

        elif menu == "a":
            add_task(task_list, username_password)
            # reload tasks list (optional, but keeps it consistent)
            task_list = load_tasks()

        elif menu == "va":
            view_all(task_list)

        elif menu == "vm":
            view_mine(task_list, current_user, username_password)
            # reload tasks after edits/completions
            task_list = load_tasks()

        elif menu == "gr":
            if current_user != "admin":
                print("Only admin can generate reports.")
                continue
            generate_reports(task_list, username_password)

        elif menu == "ds":
            if current_user != "admin":
                print("Only admin can display statistics.")
                continue
            display_statistics(task_list, username_password)

        elif menu == "e":
            print("Goodbye!!!")
            break

        else:
            print("You have made a wrong choice, Please Try again")


if __name__ == "__main__":
    main()
