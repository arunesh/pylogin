from flask import Flask, render_template, request, redirect, url_for, session
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
import re

from dblayer import DbLayer 

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
dblayer = DbLayer()

# http://localhost:5000/login/ - the following will be our login page, which will use both GET and POST requests
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        req = request.form
        email = req.get("email")
        password = req.get("password")
        users = dblayer.get_users()
        if not email in users:
            return render_template('index.html', msg='Login failed !')
        user = users[email]
        if password != user['password']:
            return render_template('index.html', msg='Login failed !')

        # fetch account and verify. 
        session['email'] = user["email"]
        session['loggedin'] = True
        session['id'] = user['id']
        return redirect(url_for('home'))

    return render_template('index.html', msg='')

# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        dblayer.register(email, password)
        print("request.form = ", request.form)
        msg = 'Successfully registered ! Please login to continue.'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/login/logout - this will be the logout page
@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/login/home')
def home():
    # Check if user is logged in
    if 'loggedin' in session:
        return render_template('home.html', email=session['email'])
    return render_template(url_for('login'))

@app.route('/login/profile')
def profile():
    # Check if user is logged in
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        user = dblayer.get_user(session['email'])
        # Show the profile page with account info
        return render_template('profile.html', user=user)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
