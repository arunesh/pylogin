from flask import Flask, render_template, request, redirect, url_for, session
import re

import outlook
import requests

import sys

from dblayer import DbLayer 

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'coachai'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'coachai'

FLASK_AWS_SERVER="http://demo.coach.ai:5001/token_tunnel"

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

##### Outlook calendar work

@app.route('/outlook')
def outlook_main():
    return render_template('outlook.html', message="Use this to schedule an event")

# This is the redirect_uri that Microsoft Graph would call via the client browser.
@app.route('/outlook_redirect')
def outlook_redirect():
    print("Request URL: " + request.url)
    acc = outlook.auth_complete("default", request.url, callback=url_for('outlook_redirect', _external=True))
    user = acc.get_current_user()
    email = user.user_principal_name
    full_name = user.full_name
    user = user or "default"
    email = email or "default"
    full_name = full_name or "default"
    full_url = request.url
    requests.post(FLASK_AWS_SERVER, data={'token': full_url})

    return render_template('outlook_auth_result.html', email=email, full_name=full_name,
                result = "Authorization successful !",
                message="Authorization process with Outlook was successful")

@app.route('/outlook_get_auth')
def outlook_get_auth():
    print("URL = " + url_for('login') + ' ' + url_for('outlook_redirect', _external=True));
    sys.stdout.flush()
    url = outlook.get_auth_url("default", callback=url_for('outlook_redirect', _external=True))
    print("URL =" + url)
    return redirect(url)

@app.route('/api_schedule', methods=['GET', 'POST'])
def api_schedule():
    if request.method == 'POST':
        req = request.form
        print(str(req))
        for key in req:
            print('form key '+req[key])
        email = req.get("email")
        startTime = req.get("startTime")
        endTime = req.get("endTime")
        subject = req.get("eventTitle")
        if outlook.schedule_event(email, startTime, endTime, subject):
            return "SUCCESS"
        else:
            return "FAILURE"
            
    sys.stdout.flush()
    return render_template('outlook_schedule.html', message="Use this to schedule an event")

@app.route('/outlook_schedule', methods=['GET', 'POST'])
def outlook_schedule():
    if request.method == 'POST':
        req = request.form
        print(str(req))
        for key in req:
            print('form key '+req[key])
        email = req.get("email")
        startTime = req.get("startTime")
        endTime = req.get("endTime")
        subject = req.get("eventTitle")
        if outlook.schedule_event(email, startTime, endTime, subject):
            return render_template('outlook_result.html',
                result="Event successfully scheduled",
                message="Event successfully scheduled on your Outlook calendar.",
                startTime=startTime, endTime=endTime, eventTitle=subject, email=email)
        else:
            return render_template('outlook_result.html',
                result="Event scheduling failure",
                message="Failed to schedule event ! Check auth token.",
                startTime=startTime, endTime=endTime, eventTitle=subject, email=email)
            
    sys.stdout.flush()
    return render_template('outlook_schedule.html', message="Use this to schedule an event")

@app.route('/api_schedule_weekly', methods=['GET', 'POST'])
def api_schedule_weekly():
    if request.method == 'POST':
        req = request.form
        print(str(req))
        for key in req:
            print('form key '+req[key])
        email = req.get("email")
        startTime = req.get("startTime")
        endTime = req.get("endTime")
        subject = req.get("eventTitle")
        days_of_week = req.get("days_of_week").split(",")
        first_day_of_week = req.get("first_day_of_week")
        startDate = req.get("startDate")
        endDate = req.get("endDate")
        print(f"days_list = {days_of_week}")
        sys.stdout.flush()
        result = outlook.schedule_event_weekly(user_email=email,
                interval=1, days_of_week=days_of_week,
                first_day_of_week=first_day_of_week,
                startTime = startTime,
                endTime=endTime,
                subject=subject,
                startDate=startDate,
                endDate=endDate)
 
        if result:
            return "SUCCESS"
        else:
            return "FAILURE"
            
    sys.stdout.flush()
    return render_template('outlook_schedule.html', message="Use this to schedule an event")


