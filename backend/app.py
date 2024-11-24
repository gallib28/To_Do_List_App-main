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
    if not isinstance(user_id, int):  # Ensure user_id is an integer
        print(f"Invalid user_id: {user_id}")
        return redirect(url_for('login'))

    username = session.get('username', 'User')
    unfinished_tasks = db_functions.count_unfinished_tasks(user_id)
    completed_tasks = db_functions.get_total_completed_tasks(user_id)
    average_tasks_per_month = db_functions.get_average_monthly_completed(user_id)

    stats = {
    'average_monthly_completed': average_tasks_per_month,
    'total_completed': completed_tasks,
    }

    return render_template(
        'profile.html',
        username=username,
        unfinished_tasks=unfinished_tasks,
        stats=stats
    )

@app.route('/get_task_details/<int:task_id>', methods=['GET'])
def get_task_details(task_id):
    task = db_functions.get_task_by_id(task_id)
    if task:
        return jsonify(task)
    else:
        return jsonify({'error': 'Task not found'}), 404


@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('settings.html')

# דף המשימות של המשתמש
@app.route('/user_tasks')
def user_tasks():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    tasks = db_functions.get_user_tasks(session['user_id'])
    return render_template('user_tasks.html', tasks=tasks)

# פונקציה להוספת משימה חדשה
@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    data = request.json
    task_name = data.get('task_name')
    task_description = data.get('task_description')
    task_due_date = data.get('task_due_date')
    task_priority = data.get('task_priority')

    # Save task to database
    db_functions.create_task(
        name=task_name,
        description=task_description,
        due_date=task_due_date,
        task_type="todo",
        task_status="to-do",
        user_id=session['user_id'],
        parent_task_id=None,
        task_priority=task_priority
    )

    # Get GPT subtask suggestions
    subtasks = db_functions.get_subtasks(task_name, task_description)
    return jsonify({"success": True, "suggestions": subtasks})

# יציאה מהמערכת
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/update_task_status/<int:task_id>', methods=['POST'])
def update_task_status(task_id):
    data = request.json
    new_status = data.get('status')

    print(f"New status received: {new_status}")  # Debug log

    # Normalize status values
    valid_statuses = {"to-do": "To-do", "in-progress": "in progress", "done": "done"}
    if new_status not in valid_statuses:
        print("Invalid status received!")  # Debug invalid status
        return jsonify({'error': 'Invalid status'}), 400

    # Convert the status to match database constraints
    new_status = valid_statuses[new_status]

    # Update the task status in the database
    success = db_functions.set_task_status(new_status, task_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to update task status'}), 500


@app.route('/update_password', methods=['POST'])
def update_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    new_password = request.form.get('new_password')

    if not new_password:
        flash('Password cannot be empty.', 'error')
        return redirect(url_for('profile'))

    username = session.get('username')
    updated = db_functions.update_existing_password(username, new_password)

    if updated:
        flash('Password updated successfully!', 'success')
    else:
        flash('Error updating password. Please try again.', 'danger')

    return redirect(url_for('profile'))




if __name__ == '__main__':
    print(app.url_map)
    app.run(host='0.0.0.0', port=5000, debug=True)
 