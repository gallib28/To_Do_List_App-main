import db_functions
import requests
import pytest

BASE_URL = "http://localhost:5000"

# בדיקת חיבור למסד הנתונים
def test_db_connection():
    conn = db_functions.connect_to_db()
    assert conn is not False, "Database connection failed"

# בדיקת יצירת משתמש חדש
def test_create_user():
    result = db_functions.create_user("testuser", "testpassword")
    assert result is True, "Failed to create user"

# בדיקת התחברות משתמש
def test_login_user():
    result = db_functions.login_user("testuser", "testpassword")
    assert result is True, "Failed to login user"

# בדיקת הוספת משימה חדשה
def test_create_task():
    result = db_functions.create_task(
        name="Test Task",
        description="This is a test task",
        due_date="2024-12-31",
        task_type="todo",
        task_status="to-do",
        user_id=1,
        parent_task_id=None,
        task_priority="High"
    )
    assert result is True, "Failed to create task"

# בדיקת קבלת משימות משתמש
def test_get_user_tasks():
    tasks = db_functions.get_user_tasks(1)
    assert len(tasks) > 0, "No tasks found for the user"

# בדיקת קבלת משימות לא גמורות
def test_get_unfinished_tasks():
    tasks = db_functions.get_unfinished_user_tasks(1)
    assert len(tasks) > 0, "No unfinished tasks found"

# בדיקת תתי-משימות באמצעות API של ChatGPT
def test_get_subtasks():
    subtasks = db_functions.get_subtasks("Test Task", "This is a test task description")
    assert len(subtasks) > 0, "No subtasks were suggested"

# בדיקת API: התחברות משתמש דרך Flask
def test_api_login():
    response = requests.post(f"{BASE_URL}/login", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200, "Failed to login via API"

# בדיקת API: יצירת משימה דרך Flask
def test_api_create_task():
    response = requests.post(f"{BASE_URL}/add_task", json={
        "task_name": "API Test Task",
        "task_description": "This is a test task from API",
        "task_due_date": "2024-12-31",
        "task_priority": "Medium"
    })
    assert response.status_code == 200, "Failed to create task via API"
    assert response.json().get("success") is True, "Task creation failed via API"

# בדיקת מחיקת משימה
def test_delete_task():
    result = db_functions.delete_task(1)
    assert result is True, "Failed to delete task"

# בדיקת מחיקת משתמש
def test_delete_user():
    result = db_functions.delete_user(1)
    assert result is True, "Failed to delete user"

# בדיקת שאילתות ישירות למסד הנתונים
def test_direct_db_query():
    conn = db_functions.connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS count FROM tasks")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    assert result["count"] > 0, "No tasks found in the database"

if __name__ == "__main__":
    pytest.main()
