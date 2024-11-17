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

app = Flask(
    __name__,
    template_folder='../templates',  # מיקום תיקיית התבניות
    static_folder='../static'       # מיקום תיקיית הקבצים הסטטיים
)

app.secret_key = 'your_secret_key_here'

# דף הבית – מפנה לדף ההתחברות
@app.route('/')
def home():
    return redirect(url_for('login'))

# דף התחברות
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if db_functions.login_user(username, password):
            user_id = db_functions.get_user_id_by_username(username)
            session['user_id'] = user_id
            session['username'] = username

            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('profile'))
        
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

# דף פרופיל
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    tasks = db_functions.get_user_tasks(session['user_id'])
    return render_template('profile.html', tasks=tasks)

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

    # יצירת המשימה בבסיס הנתונים
    db_functions.create_task(task_name, task_description, task_due_date, "todo", "to-do", session['user_id'], None, task_priority)

    # הצעת תתי-משימות
    subtasks = db_functions.get_subtasks(task_name, task_description)
    return jsonify({"success": True, "suggestions": subtasks})

# יציאה מהמערכת
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
