# need to start virtual env named venv 
# by this commands:
# 1.enter project folder via cmd and enter this:``` python -m venv venv ``` 
# 2. in linux/mac :``` source venv/scripts/activate ``` 
# in windows:``` venv\Scripts\activate ``` or this ``` .\venv\Scripts\activate```
# 3.install pip: ``` pip install flask ```
# 4. saving dependencies ``` pip freeze > requirements.txt ```
# 5. runnin g the file is ``` python app_back_front.py ``` 
# if we want to take dependencies from other project : ``` pip install -r requirements.txt ``` 
from flask import Flask, render_template, request, redirect, url_for, session, flash
import db_functions

app = Flask(__name__)
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
        
        # בדיקת שם משתמש וסיסמה במסד הנתונים
        if db_functions.authenticate_user(username, password):
            user = db_functions.get_user_by_username(username)
            session['user_id'] = user['user_id']
            session['username'] = username
            session['is_admin'] = user['is_admin']
            
            # אם המשתמש הוא מנהל
            if user['is_admin']:
                flash('Welcome, Admin!', 'success')
                return redirect(url_for('admin_dashboard'))
            
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('profile'))
        
        # במקרה של התחברות לא מוצלחת
        flash('Invalid username or password', 'danger')
        return render_template('login.html')
    
    return render_template('login.html')

# דף הרשמה
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # יצירת משתמש חדש
        if db_functions.create_user(username, password):
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))
        
        flash('User already exists. Please choose a different username.', 'warning')
    return render_template('register.html')

# דף פרופיל
@app.route('/profile')
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
    users = db_functions.get_all_users()
    return render_template('admin_dashboard.html', tasks=tasks, users=users)

# פונקציה להוספת משימה חדשה
@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    task_name = request.form.get('task_name')
    task_description = request.form.get('task_description')
    task_due_date = request.form.get('task_due_date')
    task_priority = request.form.get('task_priority')
    
    db_functions.add_task(session['user_id'], task_name, task_description, task_due_date, task_priority)
    flash('Task added successfully!', 'success')
    return redirect(url_for('user_tasks'))

# פונקציה למחיקת משימה
@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db_functions.delete_task(task_id)
    flash('Task deleted successfully!', 'info')
    return redirect(url_for('user_tasks'))

# פונקציה לעדכון פרטי המשתמש
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    new_username = request.form.get('username')
    new_password = request.form.get('password')
    
    db_functions.update_user(session['user_id'], new_username, new_password)
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

# יציאה מהמערכת
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
