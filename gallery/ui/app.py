from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import flash

from gallery.data.user import User
from gallery.data.postgres_user_dao import PostgresUserDAO
from gallery.data.db import connect
from gallery.tools.ig_secrets import get_session_secret

app = Flask(__name__)
app.secret_key = get_session_secret()

def user_dao():
    return PostgresUserDAO()

@app.route("/")
def  main_menu():
    return render_template('main_menu.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        connect()
        user = user_dao().get_user(request.form["username"])
        if user is None or user.password != request.form["password"]:
             error = 'Invalid credentials'
        else:
            session['username'] = request.form['username']
            flash('You were successfully logged in')
            return redirect('/')
        return render_template('login.html', error=error)
    else:
        return render_template("login.html")

def check_admin():
    return 'username' in session and session['username'] == 'admin'

@app.route("/admin")
def admin_home():
    if not check_admin():
        error = 'You must be logged in as the admin to access this page';
        return render_template('login.html', error=error)
    connect()
    users = user_dao().list_users()
    return render_template('admin_home.html', users=users)

@app.route("/admin/modify/<username>")
def modify_user(username):
    if not check_admin():
        error = 'You must be logged in as the admin to access this page';
        return render_template('login.html', error=error)
    connect()
    user = user_dao().get_user(username)
    if user:
        return render_template('modify_form.html', full_name=user.full_name, username=username)
    else:
        return username + " does not exist.<br/><a href='/admin'>Return to Menu</a>"

@app.route("/admin/modified", methods = ['POST'])
def modified():
    if not check_admin():
        error = 'You must be logged in as the admin to access this page';
        return render_template('login.html', error=error)
    connect()
    username = request.form['username'] 
    full_name = request.form['full_name'] if request.form['full_name'] else ""
    password = request.form['password'] if request.form['password'] else ""
    user_dao().edit_user(username,password,full_name)
    return full_name + " has been modified.<br/><a href='/admin'>Return to Menu</a>"

@app.route("/admin/delete/<username>")
def delete(username):
    if not check_admin():
        error = 'You must be logged in as the admin to access this page';
        return render_template('login.html', error=error)
    return render_template('areyousure.html', username=username)

@app.route("/admin/deleted/<username>")
def deleted(username):
    if not check_admin():
        error = 'You must be logged in as the admin to access this page';
        return render_template('login.html', error=error)
    connect()
    user_dao().delete_user(username)
    return username + " has been deleted.<br/><a href='/admin'>Return to Menu</a>"

@app.route("/admin/addUser")
def new_user_form():
    if not check_admin():
        error = 'You must be logged in as the admin to access this page';
        return render_template('login.html', error=error)
    return render_template('add_form.html')

@app.route("/admin/added", methods = ['POST'])
def added():
    if not check_admin():
        error = 'You must be logged in as the admin to access this page';
        return render_template('login.html', error=error)
    connect()
    username = request.form['username']
    full_name = request.form['full_name'] if request.form['full_name'] else ""
    password = request.form['password'] if request.form['password'] else ""
    if user_dao().add_user(username,password,full_name):
        return username + " has been created.<br/><a href='/admin'>Return to Menu</a>"
    else:
        return "Could not create " + username + ".<br/><a href='/admin'>Return to Menu</a>"


