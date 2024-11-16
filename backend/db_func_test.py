def test_all_functions():
    # יצירת משתמש
    username = "test_user"
    password = "test_password"

    print("Testing create_user function:")
    if create_user(username, password):
        print("User created successfully.")
    else:
        print("Failed to create user.")
        return
    # בדיקת התחברות
    print("Testing login_user function:")
    if login_user(username, password):
        print("Login successful.")
    else:
        print("Login failed.")
        return
        # יצירת משימה
    task_name = "Test Task"
    task_description = "This is a test task."
    due_date = "2024-12-31"
    task_type = "w"
    user_id = 3  # assuming you have a user with id 1
    parent_task_id = None
    task_priority = '1'
    task_status="To-do"



    print("Testing create_task function: \n ")
    if create_task(task_name, task_description, due_date, task_type,task_status, user_id, parent_task_id, task_priority):
        print("Task created successfully. \n ")

    else:
        print("Failed to create task.")
        return
    # קבלת כל המשימות
    print("Testing get_tasks function: \n ")
    tasks = get_tasks()
    if tasks:
        print("Tasks retrieved successfully: \n ", tasks)
    else:
        print("Failed to retrieve tasks.")
        return
    # קבלת משימות של משתמש מסוים
    print("Testing get_user_tasks function: \n ")
    user_tasks = get_user_tasks(user_id)
    if user_tasks:
        print("User tasks retrieved successfully: \n", user_tasks)
    else:
        print("Failed to retrieve user tasks.")
        return
    # עדכון מצב משימה
    task_id = 1  # assuming task_id is 1
    new_status = "in progress"
    print("Testing set_task_status function: \n ")
    if set_task_status(new_status, task_id):
        print("Task status updated successfully. \n ")
    else:
        print("Failed to update task status.")
        return
    # עדכון שם משימה
    new_name = "Updated Test Task"
    print("Testing set_task_name function: \n ")
    if set_task_name(new_name, task_id):
        print("Task name updated successfully. \n ")
    else:
        print("Failed to update task name.")
        return
    # בדיקת משימות שלא הושלמו של משתמש
    print("Testing get_unfinished_user_tasks function:")
    unfinished_tasks = get_unfinished_user_tasks(user_id)
    if unfinished_tasks:
        print("Unfinished tasks retrieved successfully: \n ", unfinished_tasks)
    else:
        print("Failed to retrieve unfinished tasks.")
        return
    # # בדיקת משימות שתאריך הסיום שלהן בעוד פחות מ-5 ימים
    print("Testing check_u5 function: \n ")
    u5_tasks = check_u5()
    if u5_tasks:
        print("Tasks due in less than 5 days retrieved successfully: \n ", u5_tasks)
    else:
        print("Failed to retrieve tasks due in less than 5 days.")
        return
    # # מחיקת משימה
    print("Testing delete_task function: \n ")
    if delete_task(task_id):
        print("Task deleted successfully.")
    else:
        print("Failed to delete task.")
        return
    # מחיקת משתמש
    print("Testing delete_user function: \n ")
    if delete_user(user_id):
        print("User deleted successfully.")
    else:
        print("Failed to delete user.")
        return

# קריאת הסנריו
test_all_functions()
