from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import flash

from functools import wraps

from gallery.data.user import User
from gallery.data.postgres_user_dao import PostgresUserDAO
from gallery.data.db import connect
from gallery.tools.ig_secrets import get_session_secret
from gallery.data.s3_tools import upload_image, download_images

app = Flask(__name__)
app.secret_key = get_session_secret()

def user_dao():
    return PostgresUserDAO()


def check_admin():
    return 'username' in session and session['username'] == 'admin'

@app.template_global()
def check_logged_in():
    return 'username' in session

def requires_admin(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_admin():
            error = 'You must be logged in as the admin to access this page';
            return render_template('login.html', error=error)
        return view(**kwargs)
    return decorated

def requires_login(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_logged_in():
            error = 'Please log in';
            return render_template('login.html', error=error)
        return view(**kwargs)
    return decorated

@app.route("/")
def  main_menu():
    return render_template('main_menu.html')

@app.route("/logout")
def logout():
    session.pop('username', None)
    flash('You have been logged out')
    return redirect('/')
    return

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

@app.route("/uploadImage", methods=['GET', 'POST'])
@requires_login
def upload():
    if request.method == 'POST':
        content_type = request.mimetype
        image_file = request.files['image']
        owner = session['username']
        response = upload_image(image_file, owner, content_type)
        if response:
            flash('Upload was successful')
        else:
            flash('Upload was unsuccessful')
        return render_template("upload.html")
    else:
        return render_template("upload.html")

@app.route("/viewImages")
@requires_login
def view_images():
    images = download_images(session[username])
    return render_template("view_images.html")


@app.route("/viewImages")
@requires_login
def view_images():
    return

@app.route("/admin/users")
@requires_admin
def admin_home():
    connect()
    users = user_dao().list_users()
    return render_template('admin_home.html', users=users)

@app.route("/admin/users/modify/<username>")
@requires_admin
def modify_user(username):
    connect()
    user = user_dao().get_user(username)
    if user:
        return render_template('modify_form.html', full_name=user.full_name, username=username)
    else:
        return username + " does not exist.<br/><a href='/admin/users'>Return to Menu</a>"

@app.route("/admin/users/modified", methods = ['POST'])
@requires_admin
def modified():
    connect()
    username = request.form['username'] 
    full_name = request.form['full_name'] if request.form['full_name'] else ""
    password = request.form['password'] if request.form['password'] else ""
    user_dao().edit_user(username,password,full_name)
    return full_name + " has been modified.<br/><a href='/admin/users'>Return to Menu</a>"

@app.route("/admin/users/delete/<username>")
@requires_admin
def delete(username):
    return render_template('areyousure.html', username=username)

@app.route("/admin/users/deleted/<username>")
@requires_admin
def deleted(username):
    connect()
    user_dao().delete_user(username)
    return username + " has been deleted.<br/><a href='users/admin'>Return to Menu</a>"

@app.route("/admin/users/addUser")
@requires_admin
def new_user_form():
    return render_template('add_form.html')

@app.route("/admin/users/added", methods = ['POST'])
@requires_admin
def added():
    connect()
    username = request.form['username']
    full_name = request.form['full_name'] if request.form['full_name'] else ""
    password = request.form['password'] if request.form['password'] else ""
    if user_dao().add_user(username,password,full_name):
        return username + " has been created.<br/><a href='/admin/users'>Return to Menu</a>"
    else:
        return "Could not create " + username + ".<br/><a href='/admin/users'>Return to Menu</a>"


