import mysql.connector
import bcrypt
from dotenv import load_dotenv
import os
import openai





# Load environment variables from .env file
load_dotenv()


# הגדרת מפתח API
openai.api_key = os.getenv("OPENAI_ADMIN_API_KEY")
def get_subtasks(task_name, task_description):
    prompt = f"""
    You must not give a response with more than 100 tokens.

    You are given a primary task called '{task_name}'. The task description is as follows:
    "{task_description}"

    Please break it down into several smaller, manageable sub-tasks.
    Keep it in this format:
    1.
    2.
    3.
    4.
    5.
    """

    try:
        # שימוש בפונקציה הנכונה לפי הגרסה החדשה
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        # גישה לטקסט של התשובה ישירות
        text_output = response.choices[0].text.strip()
        return text_output.split("\n")
    except Exception as e:
        print(f"Error in API request: {e}")
        return None


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

def create_user(username, password):
    conn = connect_to_db()
    if conn is False:
        return False

    cursor = conn.cursor(dictionary=True)
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO users (user_username, user_password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
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
    try:
        cursor.execute("SELECT * FROM users WHERE user_username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            print("User not found.")
            return False

        hashed_password = user['user_password']

        # Check the entered password against the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return {'user_id': int(user['user_id'])}  # Explicitly convert user_id to integer
        else:
            print("Password does not match.")
            return False
    finally:
        cursor.close()
        conn.close()

def update_existing_password(username, plain_password):
    conn = connect_to_db()
    if conn is False:
        return False

    cursor = conn.cursor(dictionary=True)
    try:
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("UPDATE users SET user_password = %s WHERE user_username = %s", (hashed_password, username))
        conn.commit()
        print(f"Password updated successfully for {username}!")
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False
    finally:
        cursor.close()
        conn.close()






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

def get_task_by_id(task_id):
    conn = connect_to_db()
    if conn is False:
        return None  # Return None if the database connection fails

    cursor = conn.cursor(dictionary=True)  # Use dictionary=True for easy JSON conversion
    try:
        cursor.execute("""
            SELECT task_id, task_name, task_description, task_dueDate, task_status, task_priority, task_type, user_id, parent_task_id
            FROM tasks
            WHERE task_id = %s;
        """, (task_id,))
        task = cursor.fetchone()  # Fetch the task
        return task
    except Exception as e:
        print(f"Error fetching task by ID: {e}")  # Log the error
        return None
    finally:
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
        SELECT task_id, task_name, task_status 
        FROM tasks 
        WHERE task_status != 'done' AND user_id = %s;
        """, (user_id,))
        tasks = cursor.fetchall()
        return tasks
    except mysql.connector.Error as err:
        print(f"Error fetching unfinished tasks: {err}")
        return False
    finally:
        cursor.close()
        conn.close()
# returns int count for unfinished 
def count_unfinished_tasks(user_id):
    print(f"user_id: {user_id}, type: {type(user_id)}")
    conn = connect_to_db()
    if conn is False:
        return 0  # Default to 0 if the connection fails

    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM tasks 
        WHERE user_id = %s AND task_status != 'completed'
    """, (int(user_id),))

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result[0] if result else 0

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

def set_task_status(new_status, task_id):
    conn = connect_to_db()
    if conn is False:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE tasks
            SET task_status = %s
            WHERE task_id = %s;
        """, (new_status, task_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating task status: {e}")  # Debug
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

def get_average_monthly_completed(user_id):
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT AVG(monthly_counts.completed_count) AS avg_monthly_completed
            FROM (
                SELECT COUNT(*) AS completed_count
                FROM tasks
                WHERE user_id = %s AND task_status = 'done'
                GROUP BY YEAR(task_dueDate), MONTH(task_dueDate)
            ) AS monthly_counts;
        """, (user_id,))
        result = cursor.fetchone()
        return result['avg_monthly_completed'] or 0
    except Exception as e:
        print(f"Error fetching average monthly completed tasks: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()


def mark_task_as_completed(task_id, user_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Update the task's status to 'completed'
        cursor.execute("""
        UPDATE tasks
        SET task_status = 'completed'
        WHERE task_id = %s AND user_id = %s
        """, (task_id, user_id))

        # Increment the user's completed task count
        cursor.execute("""
        UPDATE users
        SET completed_tasks = completed_tasks + 1
        WHERE user_id = %s
        """, (user_id,))

        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating task status: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def mark_task_as_done(task_id, user_id):
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # עדכון מצב המשימה
        cursor.execute("UPDATE tasks SET task_status = 'done' WHERE task_id = %s AND user_id = %s", (task_id, user_id))

        # הגדלת מספר המשימות שהושלמו עבור המשתמש
        cursor.execute("UPDATE users SET completed_tasks_count = completed_tasks_count + 1 WHERE user_id = %s", (user_id,))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating task status: {e}")
        return False
    finally:
        cursor.close()
        conn.close()




def get_total_completed_tasks(user_id):
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT COUNT(*) AS total_completed 
            FROM tasks 
            WHERE user_id = %s AND task_status = 'done';
        """, (user_id,))
        result = cursor.fetchone()
        return result['total_completed']
    except Exception as e:
        print(f"Error fetching total completed tasks: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()













