import mysql.connector
import bcrypt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# CONVERTING THE DATA 
def convert_to_dict(result):
    columns = ['task_id', 'task_name', 'task_description', 'task_status', 'user_id']
    data = [dict(zip(columns, row)) for row in result]
    return data



# Access the PASSWORD variable
password = os.getenv('PASSWORD')

# connection established
def connect_to_db():
    try:
        db = mysql.connector.connect(
            host="192.168.11.90",
            user="root",
            passwd="Gs-24072000",
            database="todolist"
        )
        print("DB connection is successful")
        return db
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

def create_user(un,password):
    conn = connect_to_db()
    if conn is False:
        return False
    cursor = conn.cursor(dictionary=True)
    try :
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("insert into users(user_username,user_password) values (%s,%s) ",(un,hashed_password.decode('utf-8')))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"error: {err} ")
        return False
    finally:
        cursor.close()
        conn.close()



def create_task(name, description, due_date, task_type,task_status, user_id,parent_task_id,task_priority):
    conn = connect_to_db()
    if conn is False:
        return False
    cursor = conn.cursor(dictionary=True)
    try :
        cursor.execute("""
        INSERT INTO tasks (task_name, task_description, task_dueDate, task_type,task_status, user_id,parent_task_id,task_priority)
        VALUES ( %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s);
        """, (name, description, due_date, task_type,task_status,user_id,parent_task_id,task_priority))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"error : {err}")
        return False
    finally:
        cursor.close()
        conn.close()





def login_user(username, password):
    conn = connect_to_db()
    if conn is False:
        return False

    cursor = conn.cursor(dictionary=True)

    # בדיקת שם משתמש והבאת הסיסמה
    cursor.execute("""
    SELECT user_password FROM users WHERE user_username = %s;
    """, (username,))
    result = cursor.fetchone()

    conn.close()

    if result is None:
        return False  # משתמש לא נמצא

    hashed_password = result[0]  # הסיסמה המוצפנת

    # בדיקת התאמה של הסיסמה
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return True  # התחברות הצליחה
    else:
        return False  # התחברות נכשלה


# getting all tasks created for admin user 
def get_tasks():
    conn = connect_to_db()
    if conn is False:
        return False
    cursor = conn.cursor(dictionary=True)
    try :
        cursor.execute("select * from tasks")
        tasks = cursor.fetchall()
        return tasks
    except mysql.connector.Error as err:
        print(f"error : {err}")
        return False
    finally :
        cursor.close()
        conn.close()



# get specific user tasks
def get_user_tasks(user_id):
    conn = connect_to_db()
    if conn is False:
        return False
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        select * from tasks
        where user_id = %s ;
        """,(user_id,))
        tasks = cursor.fetchall()
        return tasks
    except mysql.connector.Error as err:
        print(f"error : {err}")
        return False
    finally:
        cursor.close()
        conn.close()


def delete_task(task_id):
    conn = connect_to_db()
    if conn is False:
        return False
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        delete from tasks 
        where task_id = %s ;
        """,(task_id,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"error : {err}")
    finally:
        cursor.close()
        conn.close()


def delete_user(user_id):
    conn = connect_to_db()
    if conn is False:
        return False
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        delete from users 
        where user_id = %s ;
        """, (user_id,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"error: {err} ")
        return False
    finally :
        cursor.close()
        conn.close()
# getting all user unfinished tasks
def get_unfinished_user_tasks(user_id):
    conn = connect_to_db()
    if conn is False:
        return False
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        select task_id,task_name,task_status 
        from tasks 
        where task_status != "done" and user_id= %s ;
        """,(user_id,))
        tasks = cursor.fetchall()
        return tasks
    except mysql.connector.Error as err:
        print(f"error is {err}")
        return False
    finally :
        cursor.close()
        conn.close()


# check due under five days
def check_u5(user_id):
    conn = connect_to_db()
    if conn is False:
        return False
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        select task_id, task_dueDate, task_status, DATEDIFF(task_dueDate, CURRENT_DATE) AS days_until_due
        from tasks
        where
        DATEDIFF(task_dueDate, CURRENT_DATE) <= 5 and task_status != "done" and user_id = %s ;
        """,(user_id,))
        tasks = cursor.fetchall()
        return tasks
    except mysql.connector.Error as err:
        print(f"error: {err} ")
        return False
    finally :
        cursor.close()
        conn.close()

def set_task_status(status,task_id):
    conn = connect_to_db()
    if conn is False:
        return False
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        update tasks 
        set task_status = %s  
        where task_id = %s ;
        """,(status,task_id))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"error : {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def set_task_description(string,task_id):
    conn = connect_to_db()
    if conn is False:
        return False
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        update tasks 
        set task_description =%s
        where task_id = %s;
        """,(string,task_id))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"error : {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def set_task_name(name,task_id):
    conn = connect_to_db()
    if conn is False:
        return False
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            update tasks 
            set task_name = %s 
            where task_id = %s;
            """,(name,task_id))
        conn.commit()
        return True
    except mysql.connector.Error  as err:
        print(f"error : {err}")
        return False
    finally:
        cursor.close()
        conn.close()


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





























