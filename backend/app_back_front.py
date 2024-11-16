# need to start virtual env named venv 
# by this commands:
# 1.enter project folder via cmd and enter this:``` python -m venv venv ``` 
# 2. in linux/mac :``` source venv/scripts/activate ``` 
# in windows:``` venv\Scripts\activate ``` or this ``` .\venv\Scripts\activate```
# 3.install pip: ``` pip install flask ```
# 4. saving dependencies ``` pip freeze > requirements.txt ```
# 5. runnin g the file is ``` python app_back_front.py ``` 
# if we want to take dependencies from other project : ``` pip install -r requirements.txt ``` 
import db_functions 
from flask import Flask, request, jsonify, render_template, redirect, url_for


## link for flask tot https://www.youtube.com/watch?v=Qr4QMBUPxWo



app = Flask(__name__, static_folder='static', template_folder='templates')

# נתיב לדף ההתחברות
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        if db_functions.authenticate_user(username, password):
            return redirect(url_for('user_tasks'))
        else:
            return render_template('login.html', message='Invalid credentials')
    return render_template('login.html')

# נתיב לדף המשימות של המשתמש
@app.route('/user_tasks')
def user_tasks():
    tasks = db_functions.get_all_tasks()
    return render_template('user_tasks.html', tasks=tasks)

# יצירת משימה חדשה
@app.route('/create_task', methods=['POST'])
def create_task():
    data = request.form
    name = data.get('taskName')
    description = data.get('taskDescription')
    if not name or not description:
        return 'Name and description cannot be empty', 400
    db_functions.add_task(name, description, None, None, 1, None, 1)
    return redirect(url_for('user_tasks'))

# נתיב לפרטי משימה
@app.route('/task/<int:task_id>', methods=['GET', 'POST'])
def task_detail(task_id):
    task = db_functions.get_task(task_id)
    if request.method == 'POST':
        status = request.form.get('taskStatus')
        db_functions.update_task_status(task_id, status)
        return redirect(url_for('user_tasks'))
    return render_template('task_detail.html', task=task)

# דף ראשי לאדמין
@app.route('/admin_dashboard')
def admin_dashboard():
    tasks = db_functions.get_all_tasks()
    return render_template('admin_dashboard.html', tasks=tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
