import mysql.connector
import bcrypt
from dotenv import load_dotenv
import os
import openai





# Load environment variables from .env file
load_dotenv()


# הגדרת מפתח API
openai.api_key = os.getenv("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")
def get_subtasks(task_name, task_description):
    prompt = prompt = f"""
    You are given a primary task called '{task_name}'. The task description is as follows:
    "{task_description}"

    Please break it down into several smaller, manageable sub-tasks that, when completed, will collectively achieve the main objective. Follow these steps:

    1. **Analyze the main task:** Understand the overall goal and desired outcome of the task based on the given description.
    2. **Divide into sub-tasks:** Decompose the main task '{task_name}' into a series of clear and specific sub-tasks, each addressing a part of the problem or a specific step towards the solution.
    3. **Logical order:** Arrange the sub-tasks in a logical sequence to ensure a structured and efficient process.
    4. **Provide execution guidelines:** For each sub-task, include clear instructions or actions required to complete it.

    Use the following structure:
    - Sub-task 1: [Sub-task name]
      - Objective: [Objective of the sub-task]
      - Instructions: [Step-by-step actions for the sub-task]

    Continue this process until the entire main task is fully decomposed.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Your prompt here"}]
        )
        # הפקת רשימת תתי-משימות מהתגובה
        subtasks = response['choices'][0]['message']['content']
        return subtasks.split("\n")
    except Exception as e:
        print(f"Error in API request: {e}")
        return []



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























