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
from flask import Flask, request, jsonify, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # החלף במפתח סודי משלך



@app.route('/')
def home():
    return redirect(url_for('login'))


# דף התחברות
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if db_functions.authenticate_user(username, password):
            user = db_functions.get_user_by_username(username)
            session['user_id'] = user['user_id']
            session['username'] = username
            session['is_admin'] = user['is_admin']
            
            if user['is_admin']:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('profile'))
        
        return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')

# דף הרשמה
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # יצירת משתמש חדש
        if db_functions.create_user(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', message='User already exists')
    return render_template('register.html')

# דף פרופיל
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db_functions.get_user_by_id(session['user_id'])
    tasks_analysis = db_functions.get_task_analysis(session['user_id'])
    return render_template('profile.html', user=user, analysis=tasks_analysis)

# דף המשימות של המשתמש
@app.route('/user_tasks')
def user_tasks():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    tasks = db_functions.get_tasks_by_user(session['user_id'])
    return render_template('user_tasks.html', tasks=tasks)

# דף המנהל
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    tasks = db_functions.get_all_tasks()
    return render_template('admin_dashboard.html', tasks=tasks)

# יציאה מהמערכת
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
