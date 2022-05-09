from flask import Flask, render_template, request, redirect, url_for, session
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
import re

from dblayer import users

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'coachai'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
# mysql = MySQL(app)

# http://localhost:5000/login/ - the following will be our login page, which will use both GET and POST requests
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        req = request.form
        username = req.get("username")
        password = req.get("password")
        if not username in users:
            return render_template('index.html', msg='Login failed !')
        user = users[username]

        # fetch account and verify. 
        session['username'] = user["username"]
        session['loggedin'] = True
        session['id'] = user['id']
        return 'Logged in successfully !'

    return render_template('index.html', msg='')

# http://localhost:5000/login/logout - this will be the logout page
@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
