import mysql.connector
import bcrypt
from dotenv import load_dotenv
import os
import openai
import pymysql




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
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        text_output = response.choices[0].text.strip()
        return text_output.split("\n")
    except Exception as e:
        print(f"Error in API request: {e}")
        return None






password = os.getenv('PASSWORD')

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



def create_task(name, description, due_date, task_type, task_status, user_id, parent_task_id, task_priority):
    conn = connect_to_db()
    if conn is False:
        print("Database connection failed.")
        return False

    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            INSERT INTO tasks (task_name, task_description, task_dueDate, task_type, task_status, user_id, parent_task_id, task_priority)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (name, description, due_date, task_type, task_status, user_id, parent_task_id, task_priority)
        print("Executing query:", query, "With params:", params)
        cursor.execute(query, params)
        conn.commit()
        print("Task successfully inserted into the database.")
        return True
    except Exception as e:
        print(f"Error creating task: {e}")
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

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return {'user_id': int(user['user_id'])}  
        else:
            print("Password does not match.")
            return False
    finally:
        cursor.close()
        conn.close()

def update_existing_password(username, old_password, new_password):
    conn = connect_to_db()
    if not conn:
        return False

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_password FROM users WHERE user_username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            print(f"User '{username}' not found.")
            return False

        hashed_password = user['user_password']
        if not bcrypt.checkpw(old_password.encode('utf-8'), hashed_password.encode('utf-8')):
            print("Old password does not match.")
            return False

        hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute("UPDATE users SET user_password = %s WHERE user_username = %s", (hashed_new_password, username))
        conn.commit()
        print(f"Password updated successfully for {username}.")
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False
    finally:
        cursor.close()
        conn.close()









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




def get_user_tasks(user_id):
    conn = connect_to_db()
    if conn is False:
        return False

    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT * FROM tasks
        WHERE user_id = %s AND parent_task_id IS NULL;
        """  # Ensure this is a single valid query
        cursor.execute(query, (user_id,))
        tasks = cursor.fetchall()  # Fetch all rows to consume the result
        cursor.close()  # Close the cursor before returning data
        return tasks
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        if conn.is_connected():
            conn.close()  # Ensure connection is closed



def get_sub_tasks_by_parent_id(parent_task_id):
    conn = connect_to_db()
    if conn is False:
        return False
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT * FROM tasks
        WHERE parent_task_id = %s;
        """
        cursor.execute(query, (parent_task_id,))
        sub_tasks = cursor.fetchall()
        return sub_tasks
    except Exception as e:
        print(f"Error fetching subtasks: {e}")
        return []
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


def delete_user_db(user_id):
    conn = connect_to_db()
    if not conn:
        return False

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        print(f"User {user_id} deleted successfully.")
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


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
def count_unfinished_tasks(user_id):
    print(f"user_id: {user_id}, type: {type(user_id)}")
    conn = connect_to_db()
    if conn is False:
        return 0  

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
    # Define the hierarchy of statuses
    status_hierarchy = {"to-do": 1, "in progress": 2, "done": 3}

    conn = connect_to_db()
    if conn is False:
        print("Database connection failed.")
        return False

    cursor = conn.cursor(dictionary=True)
    try:
        # Update the parent task's status
        update_query = """
            UPDATE tasks 
            SET task_status = %s 
            WHERE task_id = %s
        """
        cursor.execute(update_query, (new_status, task_id))

        # Get all subtasks for this parent task
        fetch_subtasks_query = """
            SELECT task_id, task_status 
            FROM tasks 
            WHERE parent_task_id = %s
        """
        cursor.execute(fetch_subtasks_query, (task_id,))
        subtasks = cursor.fetchall()

        # Iterate over subtasks and update them if necessary
        for subtask in subtasks:
            subtask_id = subtask['task_id']
            subtask_status = subtask['task_status']

            # Update subtask status only if it is "less advanced" than the parent's status
            if status_hierarchy[subtask_status] < status_hierarchy[new_status]:
                update_subtask_query = """
                    UPDATE tasks 
                    SET task_status = %s 
                    WHERE task_id = %s
                """
                cursor.execute(update_subtask_query, (new_status, subtask_id))

        conn.commit()
        print(f"Task {task_id} and relevant subtasks updated to status {new_status}.")
        return True
    except Exception as e:
        print(f"Error updating task status: {e}")
        conn.rollback()
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


def update_username_in_db(user_id, username):
    conn = connect_to_db()
    if not conn:
        return False

    cursor = conn.cursor(dictionary=True)
    try:
        query = "UPDATE users SET user_username = %s WHERE user_id = %s"
        cursor.execute(query, (username, user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating username: {e}")
        return False
    finally:
        cursor.close()
        conn.close()




def get_sub_tasks_by_parent_id(parent_id):
    conn= connect_to_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM tasks WHERE parent_task_id = %s"
    cursor.execute(query, (parent_id,))
    return cursor.fetchall()


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
        return result['total_completed'] if result else 0
    except Exception as e:
        print(f"Error fetching total completed tasks: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()


def get_user_by_id(user_id):
    conn = connect_to_db()
    if conn is False:
        return None  

    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT user_id, user_username AS username FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Error fetching user by ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_user_theme(user_id, theme_color):
    conn = connect_to_db()
    if conn is False:
        return False

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            UPDATE users
            SET theme_color = %s
            WHERE user_id = %s
        """, (theme_color, user_id))
        conn.commit()
        print(f"Theme updated successfully to {theme_color} for user {user_id}.")
        return True
    except Exception as e:
        print(f"Error updating theme: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def set_user_block_status(user_id, is_blocked):
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "UPDATE users SET is_blocked = %s WHERE user_id = %s"
        cursor.execute(query, (is_blocked, user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating block status: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def get_all_tasks():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM tasks"
        cursor.execute(query)
        tasks = cursor.fetchall()
        return tasks
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_task_by_id(task_id):
    conn= connect_to_db()
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM tasks WHERE task_id = %s"
        cursor.execute(query, (task_id,))
        task = cursor.fetchone()  
        return task
    finally:
        cursor.close()
        conn.close()


def update_task_in_db(task_id, task_name, description, due_date, priority, status):
    conn = connect_to_db()  
    if not conn:
        raise Exception("Database connection failed.")

    try:
        
        cursor = conn.cursor(dictionary=True)
        query = """
            UPDATE tasks
            SET task_name = %s, task_description = %s, task_dueDate = %s, task_priority = %s, task_status = %s
            WHERE task_id = %s
        """
        cursor.execute(query, (task_name, description, due_date, priority, status, task_id))
        conn.commit()  
        print(f"Task {task_id} updated successfully.")
    except Exception as e:
        print(f"Error updating task in database: {e}")
        conn.rollback()  
        raise
    finally:
        cursor.close()  
        conn.close() 


def get_sub_tasks_by_parent_id(parent_task_id):
    conn= connect_to_db()
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM tasks WHERE parent_task_id = %s"
        cursor.execute(query, (parent_task_id,))
        sub_tasks = cursor.fetchall() 
        return sub_tasks
    finally:
        cursor.close()
        conn.close()

def delete_completed_tasks():
    conn = connect_to_db()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        query = "DELETE FROM tasks WHERE task_status = 'done'"
        cursor.execute(query)
        conn.commit()
        print("All completed tasks have been deleted.")
        return True
    except Exception as e:
        print(f"Error deleting completed tasks: {e}")
        return False
    finally:
        cursor.close()
        conn.close()



