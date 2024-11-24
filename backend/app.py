# need to start virtual env named venv 
# by this commands:
# 1.enter project folder via cmd and enter this:``` python -m venv venv ``` 
# 2. in linux/mac :``` source venv/scripts/activate ``` 
# in windows:``` venv\Scripts\activate ``` or this ``` .\venv\Scripts\activate```
# 3.install pip: ``` pip install flask ```
# 4. saving dependencies ``` pip freeze > requirements.txt ```
# 5. runnin g the file is ``` python app_back_front.py ``` 
# if we want to take dependencies from other project : ``` pip install -r requirements.txt ``` 
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import db_functions
import os 
import bcrypt
from dotenv import load_dotenv
load_dotenv()

app = Flask(
    __name__,
    template_folder='../templates',  # מיקום תיקיית התבניות
    static_folder='../static'       # מיקום תיקיית הקבצים הסטטיים
)

app.secret_key = os.urandom(24)
# דף הבית – מפנה לדף ההתחברות
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Use the login_user function
        user = db_functions.login_user(username, password)
        if user:
            session['user_id'] = user['user_id']  # Extract the integer user_id
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('register.html', error="Both fields are required")

        print(f"Attempting to register user: {username}")

        # Check if the username already exists
        conn = db_functions.connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_username = %s", (username,))
        existing_user = cursor.fetchone()
        cursor.close()

        if existing_user:
            print("Username already exists.")
            return render_template('register.html', error="Username already exists")

        # Create a new user
        created = db_functions.create_user(username, password)
        if created:
            print("User created successfully.")
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            print("Error creating user.")
            return render_template('register.html', error="An error occurred. Please try again.")

    return render_template('register.html')


@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')  # ניתוב להתחברות אם אין משתמש מחובר

    username = session.get('username', 'User')

    # קבלת משימות דחופות בפחות מ-5 ימים
    urgent_tasks = db_functions.check_u5(user_id)
    urgent_task_count = len(urgent_tasks) if urgent_tasks else 0  # ספירת משימות דחופות

    # קבלת מספר המטלות הלא גמורות
    unfinished_task_count = db_functions.count_unfinished_tasks(user_id)

    # העברת הנתונים לעמוד ה-HTML
    return render_template(
        'profile.html',
        username=username,
        urgent_task_count=urgent_task_count,
        unfinished_task_count=unfinished_task_count
    )

@app.route('/delete_completed_tasks', methods=['POST'])
def delete_completed_tasks():
    # בדיקת אם המשתמש מחובר
    if 'user_id' not in session:
        return redirect(url_for('login'))

    success = db_functions.delete_completed_tasks()
    if success:
        flash("All completed tasks have been deleted successfully!", "success")
    else:
        flash("Failed to delete completed tasks. Please try again.", "error")

    return redirect(url_for('profile'))


@app.route('/task/<int:task_id>', methods=['GET'])
def task_details(task_id):
    # שליפת פרטי המשימה לפי מזהה המשימה
    task = db_functions.get_task_by_id(task_id)
    
    # אם המשימה לא נמצאה, מחזירים שגיאת 404
    if not task:
        return abort(404, description="Task not found")
    
    # בדיקה אם יש מפתח 'parent_task_id' במשימה
    if 'parent_task_id' in task:
        sub_tasks = db_functions.get_sub_tasks_by_parent_id(task_id)  # שליפת תתי-משימות
    else:
        sub_tasks = []  # אם אין תתי-משימות, מחזירים רשימה ריקה

    # מחזירים את דף פרטי המשימה עם המשימה ותתי-המשימות
    return render_template('task_details.html', task=task, sub_tasks=sub_tasks)

@app.route('/update_theme', methods=['POST'])
def update_theme():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')  # אם אין משתמש מחובר, להפנות להתחברות

    theme_color = request.form.get('theme_color')
    if not theme_color:
        return "Theme color not provided", 400

    success = db_functions.update_user_theme(user_id, theme_color)
    if success:
        return redirect('/settings')  # חזרה לעמוד ההגדרות
    else:
        return "Failed to update theme", 500

@app.route('/settings')
def settings():
    user_id = session.get('user_id')  # נניח שאתה משתמש ב-session
    if not user_id:
        return redirect('/login')  # נשלח לדף התחברות אם אין משתמש מחובר

    user = db_functions.get_user_by_id(user_id)  # שלוף את פרטי המשתמש
    if not user:
        return "User not found", 404

    return render_template('settings.html', user=user)

@app.route('/user_tasks')
def user_tasks():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    tasks = db_functions.get_user_tasks(session['user_id'])  # Updated function
    if tasks is False:
        flash("Error fetching tasks", "danger")
        return redirect('/profile')
    
    return render_template('user_tasks.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging log
        
        # Validate required fields
        required_fields = ['task_name', 'task_description', 'task_type', 'task_status']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "error": f"Missing or invalid field: {field}"}), 400

        # Insert task into the database
        success = db_functions.create_task(
            name=data['task_name'],
            description=data['task_description'],
            due_date=data.get('task_due_date'),  # Optional field
            task_type=data.get('task_type', 'p'),  # Default to 'p'
            task_status=data.get('task_status', 'to-do'),  # Default to 'to-do'
            user_id=session['user_id'],  # Get from session
            parent_task_id=data.get('parent_task_id'),  # Optional field
            task_priority=data.get('task_priority')  # Optional field
        )

        if success:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Failed to add task"}), 500

    except Exception as e:
        print("Error in /add_task:", e)  # Debugging log
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/add_subtasks', methods=['POST'])
def add_subtasks():
    try:
        data = request.get_json()
        subtasks = data.get('subtasks', [])

        for subtask in subtasks:
            db_functions.create_task(
                name=subtask['task_name'],
                description=subtask['task_description'],
                due_date=subtask.get('task_due_date'),
                task_type=subtask['task_type'],
                task_status=subtask['task_status'],
                user_id=session['user_id'],
                parent_task_id=subtask['parent_task_id'],
                task_priority=subtask.get('task_priority')
            )

        return jsonify({"success": True})
    except Exception as e:
        print("Error in /add_subtasks:", e)
        return jsonify({"success": False, "error": str(e)}), 500



@app.route('/get_gpt_assistance', methods=['POST'])
def get_gpt_assistance():
    try:
        data = request.get_json()
        task_name = data.get('task_name')
        task_description = data.get('task_description')

        # Call your GPT function here
        suggestions = db_functions.get_subtasks(task_name, task_description)

        return jsonify({"success": True, "suggestions": suggestions})
    except Exception as e:
        print("Error in /get_gpt_assistance:", e)
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/delete_account', methods=['POST'])
def delete_account():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    if db_functions.delete_user_db(user_id):
        session.clear()
        flash("Account deleted successfully!", "success")
        return redirect('/register')
    else:
        flash("Error deleting account.", "error")
        return redirect('/settings')

# יציאה מהמערכת
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # ניקוי session
    return redirect('/login')






VALID_STATUSES = ["to-do", "in progress", "done"] 

@app.route('/update_task_status/<int:task_id>', methods=['POST'])
def update_task_status(task_id):
    data = request.get_json()
    new_status = data.get("status")
    if new_status not in VALID_STATUSES:
        return jsonify({"error": "Invalid status"}), 400

    # Call the function to update the task status
    result = db_functions.set_task_status(new_status, task_id)

    if result:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to update task status'}), 500

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'GET':
        # Fetch the task details to populate the form
        task = db_functions.get_task_by_id(task_id)
        if not task:
            return f"Task with ID {task_id} not found", 404

        return render_template('edit_task.html', task=task)

    elif request.method == 'POST':
        # Handle the form submission and update the task
        task_name = request.form.get('task_name')
        description = request.form.get('description')
        due_date = request.form.get('due_date')
        priority = request.form.get('priority')
        status = request.form.get('status')

        try:
            db_functions.update_task_in_db(task_id, task_name, description, due_date, priority, status)
            print(f"Task {task_id} updated successfully.")
            return redirect(f'/task/{task_id}')  # Redirect to the task details page
        except Exception as e:
            print(f"Error updating task: {e}")
            return "Failed to update task", 500


@app.route('/update_username', methods=['POST'])
def update_username():
    username = request.form['username']
    user_id = session.get('user_id')
    if db_functions.update_username_in_db(user_id, username):  # Implement this function
        flash("Username updated successfully!")
    else:
        flash("Error updating username.")
    return redirect('/settings')

@app.route('/update_password', methods=['POST'])
def update_password():
    username = session.get('username')  # השם משתמש מתוך session
    old_password = request.form.get('old_password')  # סיסמה ישנה
    new_password = request.form.get('new_password')  # סיסמה חדשה

    if not username or not old_password or not new_password:
        flash("All fields are required.", "error")
        return redirect('/settings')

    try:
        # קריאה לפונקציה לעדכון סיסמה
        success = db_functions.update_existing_password(username, old_password, new_password)
        if success:
            flash("Password updated successfully.", "success")
        else:
            flash("Old password does not match or error occurred.", "error")
    except Exception as e:
        flash(f"Error updating password: {e}", "error")

    return redirect('/settings')


@app.route('/admin', methods=['GET'])
def admin_dashboard():
    user_id = session.get('user_id')
    # בדוק אם המשתמש הוא מנהל
    if not user_id or not session.get('is_admin'):
        return redirect('/login')

    # שלוף את כל המשתמשים והמשימות
    users = db_functions.get_all_users()
    tasks = db_functions.get_all_tasks()
    return render_template('admin_dashboard.html', users=users, tasks=tasks)




@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    # שליפת הנתונים מהטופס
    task_name = request.form.get('task_name')
    description = request.form.get('description')
    due_date = request.form.get('due_date')
    priority = request.form.get('priority')
    status = request.form.get('status')
    
    # עדכון המשימה בבסיס הנתונים
    db_functions.update_task_in_db(task_id, task_name, description, due_date, priority, status)
    return redirect(url_for('task_details', task_id=task_id))


if __name__ == '__main__':
    print(app.url_map)
    app.run(host='0.0.0.0', port=5000, debug=True)
 