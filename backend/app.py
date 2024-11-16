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

app = Flask(__name__)

@app.route('/')
def loginPage():
    return render_template("")



@app.route('/userPage/<username>',)
def userPage(username):
    return render_template("/user_homepage",username=username)

@app.route('/userPage/userTasks')
@app.route('/')
@app.route('/')
@app.route('/')
@app.route('/')
@app.route('/')
@app.route('/')





if __name__ == "__main__":
    app.run(debug=True)